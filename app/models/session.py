from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    session_code = Column(
        String(20),
        unique=True,
        index=True,
        nullable=False
    )

    status = Column(
        String(30),
        default="waiting"
    )

    current_question = Column(
        Integer,
        default=0
    )