from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from models import AcademicSource
from services.embedding_service import embed_text


class RAGService:
    def __init__(self, db: Session):
        self.db = db

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5
    ) -> List[AcademicSource]:
        """
        Vector similarity search using pgvector
        """

        query_embedding = embed_text(query)

        sql = text("""
            SELECT id, title, authors, abstract, source_type, embedding
            FROM academic_sources
            ORDER BY embedding <-> :query_embedding
            LIMIT :top_k
        """)

        results = self.db.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "top_k": top_k,
            }
        )

        return [
            AcademicSource(
                id=row.id,
                title=row.title,
                authors=row.authors,
                abstract=row.abstract,
                source_type=row.source_type,
                embedding=row.embedding,
            )
            for row in results.fetchall()
        ]
