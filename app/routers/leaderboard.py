from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import QuizSession
from app.models.participant import Participant


router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"]
)


@router.get("/{session_code}")
def get_leaderboard(
    session_code: str,
    db: Session = Depends(get_db)
):

    quiz_session = (
        db.query(QuizSession)
        .filter(
            QuizSession.session_code == session_code
        )
        .first()
    )

    if not quiz_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    participants = (
        db.query(Participant)
        .filter(
            Participant.session_id == quiz_session.id
        )
        .order_by(
            Participant.score.desc()
        )
        .all()
    )

    leaderboard = []

    for rank, participant in enumerate(
        participants,
        start=1
    ):

        leaderboard.append({
            "rank": rank,
            "name": participant.name,
            "score": participant.score
        })

    return {
        "session_code": session_code,
        "leaderboard": leaderboard
    }