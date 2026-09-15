from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("quiz_sessions.id"),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    score = Column(
        Integer,
        default=0
    )