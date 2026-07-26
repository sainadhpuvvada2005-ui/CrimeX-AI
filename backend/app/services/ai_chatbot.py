import re
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.official import OFFICIAL_TABLES


CRIME_KEYWORDS = {
    "robbery": ["robbery", "ಸುಲಿಗೆ", "ದೋಪಡಿ"],
    "murder": ["murder", "homicide", "ಕೊಲೆ"],
}


@dataclass
class AiChatResult:
    answer: str
    intent: str
    generated_sql: str | None
    rows: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    explanation: dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.72


class LanguageService:
    def detect(self, text_value: str, requested: str) -> str:
        if requested in {"en", "kn"}:
            return requested
        return "kn" if any("\u0c80" <= char <= "\u0cff" for char in text_value) else "en"

    def render(self, answer: str, language: str) -> str:
        if language == "kn":
            return (
                "CrimeX AI ಉತ್ತರ: "
                + answer
                + " ಅಧಿಕೃತ FIR ಡೇಟಾಬೇಸ್ ಮತ್ತು ಅನುಮತಿಸಲಾದ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ ಈ ಫಲಿತಾಂಶ ಸಿದ್ಧವಾಗಿದೆ."
            )
        return answer


class RagService:
    def retrieve(self, question: str) -> list[dict[str, Any]]:
        docs = [
            {
                "source": "official_erd",
                "content": "CrimeX AI must query only official KSP FIR tables and must not redesign the database.",
            },
            {
                "source": "sql_guardrail",
                "content": "Generated SQL is SELECT-only, limited, and constrained to official FIR tables.",
            },
            {
                "source": "xai_policy",
                "content": "Responses include intent, SQL trace, evidence references, confidence, and limitations.",
            },
        ]
        terms = {term.lower() for term in re.findall(r"[A-Za-z]+", question)}
        return [doc for doc in docs if terms.intersection(set(doc["content"].lower().split()))] or docs[:2]


class Llama3Service:
    def generate(self, prompt: str) -> str | None:
        try:
            from langchain_ollama import ChatOllama
            from langchain_core.messages import HumanMessage, SystemMessage
        except ModuleNotFoundError:
            return None

        try:
            llm = ChatOllama(
                model=settings.llm_model,
                base_url=settings.ollama_base_url,
                temperature=0.1,
            )
            response = llm.invoke(
                [
                    SystemMessage(content="You are CrimeX AI. Be precise, evidence-based, and security conscious."),
                    HumanMessage(content=prompt),
                ]
            )
            return str(response.content)
        except Exception:
            return None


class SqlGuardrail:
    forbidden = re.compile(
        r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|copy|call|execute)\b",
        re.IGNORECASE,
    )

    def validate(self, sql: str) -> str:
        statement = sql.strip().rstrip(";")
        if not statement.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")
        if self.forbidden.search(statement):
            raise ValueError("Generated SQL contains a forbidden operation.")
        mentioned = {name for name in OFFICIAL_TABLES if f'"{name}"' in statement or name.lower() in statement.lower()}
        if not mentioned:
            raise ValueError("Generated SQL must reference at least one official FIR table.")
        if " limit " not in f" {statement.lower()} ":
            statement = f"{statement} LIMIT {settings.chatbot_max_sql_rows}"
        return statement


class KspSqlAgent:
    def __init__(self, db: Session):
        self.db = db
        self.guardrail = SqlGuardrail()

    def generate_sql(self, question: str) -> tuple[str, str]:
        lowered = question.lower()
        case_table = self._quoted_table("CaseMaster")
        accused_table = self._quoted_table("Accused")

        if "repeat offender" in lowered or "repeat offenders" in lowered:
            return (
                "repeat_offenders",
                (
                    f"SELECT * FROM {accused_table} "
                    f"LIMIT {settings.chatbot_max_sql_rows}"
                ),
            )

        if "similar fir" in lowered or "similar case" in lowered:
            return (
                "similar_fir",
                (
                    f"SELECT * FROM {case_table} "
                    f"LIMIT {settings.chatbot_max_sql_rows}"
                ),
            )

        crime_filter = self._crime_filter(lowered)
        district_filter = self._district_filter(lowered)
        filters = [item for item in [crime_filter, district_filter] if item]
        where_clause = f" WHERE {' AND '.join(filters)}" if filters else ""
        intent = "case_summary" if "summary" in lowered else "crime_search"
        sql = f"SELECT * FROM {case_table}{where_clause} LIMIT {settings.chatbot_max_sql_rows}"
        return intent, sql

    def execute(self, sql: str) -> list[dict[str, Any]]:
        safe_sql = self.guardrail.validate(sql)
        try:
            rows = self.db.execute(text(safe_sql)).mappings().fetchmany(settings.chatbot_max_sql_rows)
            return [dict(row) for row in rows]
        except SQLAlchemyError:
            return []

    def _quoted_table(self, table_name: str) -> str:
        return f'public."{table_name}"'

    def _column_exists(self, table_name: str, preferred: list[str]) -> str | None:
        try:
            columns = {column["name"] for column in inspect(self.db.bind).get_columns(table_name, schema="public")}
        except SQLAlchemyError:
            return None
        for name in preferred:
            if name in columns:
                return name
        return None

    def _crime_filter(self, lowered: str) -> str | None:
        crime = None
        for label, terms in CRIME_KEYWORDS.items():
            if any(term in lowered for term in terms):
                crime = label
                break
        if not crime:
            return None
        column = self._column_exists("CaseMaster", ["CrimeHeadName", "CrimeHead", "crime_head", "crime_type"])
        if not column:
            return None
        return f'CAST("{column}" AS TEXT) ILIKE \'%{crime}%\''

    def _district_filter(self, lowered: str) -> str | None:
        if "mysore" not in lowered and "mysuru" not in lowered and "ಮೈಸೂರು" not in lowered:
            return None
        column = self._column_exists("CaseMaster", ["DistrictName", "District", "district_name", "district"])
        if not column:
            return None
        return f'CAST("{column}" AS TEXT) ILIKE \'%Mys%\''


class ExplainabilityService:
    def build(self, *, question: str, intent: str, sql: str | None, rows: list[dict[str, Any]], rag_docs: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "question": question,
            "intent": intent,
            "generated_sql": sql,
            "row_count": len(rows),
            "rag_sources": [doc["source"] for doc in rag_docs],
            "limits": [
                "SQL is read-only and constrained to official FIR tables.",
                "AI output is advisory and should be verified against official records.",
                "If official DB columns are unavailable, filters are omitted instead of inventing schema.",
            ],
        }


class AiChatbotEngine:
    def __init__(self, db: Session):
        self.db = db
        self.language = LanguageService()
        self.rag = RagService()
        self.llm = Llama3Service()
        self.sql_agent = KspSqlAgent(db)
        self.xai = ExplainabilityService()

    def answer(self, question: str, requested_language: str, execute_sql: bool) -> AiChatResult:
        language = self.language.detect(question, requested_language)
        rag_docs = self.rag.retrieve(question)
        intent, generated_sql = self.sql_agent.generate_sql(question)
        rows = self.sql_agent.execute(generated_sql) if execute_sql else []

        llm_answer = self.llm.generate(
            "\n".join(
                [
                    "Answer the police officer's question using the given SQL trace and RAG context.",
                    f"Question: {question}",
                    f"Intent: {intent}",
                    f"SQL: {generated_sql}",
                    f"Rows returned: {len(rows)}",
                    f"Context: {rag_docs}",
                ]
            )
        )
        fallback = self._fallback_answer(question, intent, rows, generated_sql)
        answer = self.language.render(llm_answer or fallback, language)
        explanation = self.xai.build(
            question=question,
            intent=intent,
            sql=generated_sql,
            rows=rows,
            rag_docs=rag_docs,
        )
        return AiChatResult(
            answer=answer,
            intent=intent,
            generated_sql=generated_sql,
            rows=rows[:10],
            evidence_refs=rag_docs,
            explanation=explanation,
            confidence_score=0.86 if rows else 0.68,
        )

    def _fallback_answer(self, question: str, intent: str, rows: list[dict[str, Any]], sql: str | None) -> str:
        if "prediction" in question.lower():
            return "The prediction explanation should be read as advisory. Review confidence, feature drivers, model version, and official FIR evidence before operational use."
        if intent == "repeat_offenders":
            return f"Repeat offender analysis is prepared from the Accused table. The SQL trace returned {len(rows)} authorized row(s)."
        if intent == "similar_fir":
            return f"Similar FIR search is prepared from official CaseMaster records. The SQL trace returned {len(rows)} authorized row(s)."
        if intent == "case_summary":
            return f"Case summary generation is ready. The SQL trace returned {len(rows)} authorized row(s) for summarization."
        return f"Crime search completed against the official FIR database. The SQL trace returned {len(rows)} authorized row(s)."

