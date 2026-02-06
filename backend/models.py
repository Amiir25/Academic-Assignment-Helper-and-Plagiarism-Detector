from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, func, Index
from sqlalchemy.orm import relationship
import datetime
from database import Base
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    filename = Column(String)
    original_text = Column(Text, nullable=True)
    topic = Column(String, nullable=True)
    academic_level = Column(String, nullable=True)
    word_count = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime, default=lambda: datetime.datetime.utcnow())

    student = relationship("Student", backref="assignments")

    # uploaded_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    suggested_sources = Column(JSONB)
    plagiarism_score = Column(Float)
    flagged_sections = Column(JSONB)
    research_suggestions = Column(Text)
    citation_recommendations = Column(Text)
    analyzed_at = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    
    # analyzed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class AcademicSource(Base):
    __tablename__ = "academic_sources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String)
    abstract = Column(Text, nullable=False)
    source_type = Column(String, index=True)
    embedding = Column(Vector(1536), nullable=False)

    __table_args__ = (
        Index(
            "ix_academic_sources_embedding",
            "embedding",
            postgresql_using="hnsw"
        ),
    )