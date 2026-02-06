import json
from sqlalchemy.orm import Session

from database import SessionLocal
from models import AcademicSource
from services.embedding_service import embed_text


JSON_PATH = "data/sample_academic_sources.json"


def seed_sources():
    db: Session = SessionLocal()

    with open(JSON_PATH, "r") as f:
        sources = json.load(f)

    for src in sources:
        combined_text = f"""
        {src['title']}
        {src['abstract']}
        {src.get('full_text', '')}
        """

        embedding = embed_text(combined_text)

        record = AcademicSource(
            title=src["title"],
            authors=src["authors"],
            abstract=src["abstract"],
            source_type=src["source_type"],
            embedding=embedding
        )

        db.add(record)

    db.commit()
    db.close()
    print("✅ Academic sources seeded successfully")


if __name__ == "__main__":
    seed_sources()
