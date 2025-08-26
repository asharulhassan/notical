from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import hashlib
import json

Base = declarative_base()

class FlashcardSet(Base):
    """Model for organizing flashcards into sets"""
    __tablename__ = "flashcard_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    subject = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_public = Column(Boolean, default=False)
    set_metadata = Column(JSON)  # Store additional info like tags, difficulty, etc.
    
    # Relationship to flashcards
    flashcards = relationship("Flashcard", back_populates="set", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject": self.subject,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_public": self.is_public,
            "metadata": self.set_metadata,
            "flashcard_count": len(self.flashcards)
        }

class Flashcard(Base):
    """Model for individual flashcards"""
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    
    # Core content
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    hint = Column(Text)
    
    # Metadata
    card_type = Column(String(50), nullable=False)  # definition, explanation, cloze, comparison, analysis
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    subject = Column(String(100), nullable=False)
    
    # AI generation metadata
    confidence_score = Column(Float, default=0.0)
    source_text_hash = Column(String(64), nullable=False)  # Hash of source content
    generation_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Study metadata
    times_studied = Column(Integer, default=0)
    last_studied = Column(DateTime(timezone=True))
    success_rate = Column(Float, default=0.0)
    
    # Content hash for deduplication
    content_hash = Column(String(64), unique=True, nullable=False)
    
    # Relationship to set
    set = relationship("FlashcardSet", back_populates="flashcards")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate content hash for deduplication
        if self.question and self.answer:
            self.content_hash = self._generate_content_hash()
    
    def _generate_content_hash(self):
        """Generate a unique hash for the flashcard content"""
        content_str = f"{self.question.lower().strip()}{self.answer.lower().strip()}"
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def to_dict(self):
        return {
            "id": self.id,
            "set_id": self.set_id,
            "question": self.question,
            "answer": self.answer,
            "hint": self.hint,
            "card_type": self.card_type,
            "difficulty": self.difficulty,
            "subject": self.subject,
            "confidence_score": self.confidence_score,
            "source_text_hash": self.source_text_hash,
            "generation_timestamp": self.generation_timestamp.isoformat() if self.generation_timestamp else None,
            "times_studied": self.times_studied,
            "last_studied": self.last_studied.isoformat() if self.last_studied else None,
            "success_rate": self.success_rate,
            "content_hash": self.content_hash
        }
    
    def update_study_stats(self, success: bool):
        """Update study statistics"""
        self.times_studied += 1
        self.last_studied = func.now()
        
        # Update success rate
        if self.times_studied == 1:
            self.success_rate = 1.0 if success else 0.0
        else:
            current_total = self.success_rate * (self.times_studied - 1)
            new_total = current_total + (1.0 if success else 0.0)
            self.success_rate = new_total / self.times_studied

class StudySession(Base):
    """Model for tracking study sessions"""
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    user_id = Column(String(100))  # For future user system
    
    # Session metadata
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    total_cards = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    
    # Session results
    session_data = Column(JSON)  # Store detailed results for each card
    
    def to_dict(self):
        return {
            "id": self.id,
            "set_id": self.set_id,
            "user_id": self.user_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "total_cards": self.total_cards,
            "correct_answers": self.correct_answers,
            "accuracy": (self.correct_answers / self.total_cards * 100) if self.total_cards > 0 else 0,
            "session_data": self.session_data
        }

class ContentSource(Base):
    """Model for tracking source content used to generate flashcards"""
    __tablename__ = "content_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    content_hash = Column(String(64), unique=True, nullable=False)
    content_type = Column(String(50), nullable=False)  # text, pdf, audio
    file_name = Column(String(255))
    subject = Column(String(100))
    
    # Content metadata
    word_count = Column(Integer)
    sentence_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # AI processing metadata
    processing_time = Column(Float)
    cards_generated = Column(Integer, default=0)
    
    def to_dict(self):
        return {
            "id": self.id,
            "content_hash": self.content_hash,
            "content_type": self.content_type,
            "file_name": self.file_name,
            "subject": self.subject,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processing_time": self.processing_time,
            "cards_generated": self.cards_generated
        }
