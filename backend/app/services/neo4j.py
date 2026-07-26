from app.core.config import settings
from app.schemas.neo4j import NetworkResponse


class Neo4jService:
    def network(self, entity_id: str, depth: int) -> NetworkResponse:
        query = f"""
        MATCH path = (n {{id: $entity_id}})-[*1..{depth}]-(m)
        RETURN path
        LIMIT 50
        """
        try:
            from neo4j import GraphDatabase

            with GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)) as driver:
                with driver.session() as session:
                    session.run(query, entity_id=entity_id).consume()
        except Exception:
            return NetworkResponse(nodes=[], relationships=[])
        return NetworkResponse(nodes=[], relationships=[])
