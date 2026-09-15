from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False
    )

    topic = Column(
        String(200),
        nullable=False
    )

    difficulty = Column(
        String(50),
        nullable=False
    )

    question_type = Column(
        String(50),
        nullable=False
    )

    question_count = Column(
        Integer,
        nullable=False
    )

    teacher_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )