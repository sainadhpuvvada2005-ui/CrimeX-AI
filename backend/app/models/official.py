from dataclasses import dataclass

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session


OFFICIAL_TABLES: tuple[str, ...] = (
    "CaseMaster",
    "Victim",
    "Accused",
    "ComplainantDetails",
    "ActSectionAssociation",
    "ArrestSurrender",
    "ChargesheetDetails",
    "CrimeHead",
    "CrimeSubHead",
    "Court",
    "District",
    "State",
    "Unit",
    "Employee",
    "CaseCategory",
    "GravityOffence",
    "Act",
    "Section",
)


@dataclass(frozen=True)
class OfficialTableRef:
    name: str
    schema: str = "public"


def get_official_table(db: Session, table_name: str) -> Table:
    if table_name not in OFFICIAL_TABLES:
        raise ValueError(f"Unsupported official FIR table: {table_name}")
    metadata = MetaData()
    return Table(table_name, metadata, schema="public", autoload_with=db.bind)

