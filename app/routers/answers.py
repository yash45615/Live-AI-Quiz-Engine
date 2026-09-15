from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.models.participant import Participant
from app.models.session import QuizSession
from app.services.scoring_service import calculate_score
from app.websocket.manager import manager


router = APIRouter(
    prefix="/answers",
    tags=["Answers"]
)


@router.post("/")
async def submit_answer(
    participant_id: int,
    question_id: int,
    selected_answer: str,
    time_taken: float,
    db: Session = Depends(get_db)
):

    # Find participant
    participant = db.query(Participant).filter(
        Participant.id == participant_id
    ).first()

    if not participant:
        raise HTTPException(
            status_code=404,
            detail="Participant not found"
        )

    # Find question
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    # Check whether answer was already submitted
    existing_answer = db.query(Answer).filter(
        Answer.participant_id == participant_id,
        Answer.question_id == question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Answer already submitted"
        )

    # Calculate score
    points = calculate_score(
        selected_answer,
        question.correct_answer,
        time_taken
    )

    is_correct = (
        selected_answer.upper()
        == question.correct_answer.upper()
    )

    # Save answer
    answer = Answer(
        participant_id=participant_id,
        question_id=question_id,
        selected_answer=selected_answer.upper(),
        is_correct=is_correct,
        points=points
    )

    # Update participant score
    participant.score += points

    db.add(answer)
    db.commit()
    db.refresh(answer)

    # Find quiz session
    quiz_session = db.query(QuizSession).filter(
        QuizSession.id == participant.session_id
    ).first()

    # Build leaderboard
    participants = db.query(Participant).filter(
        Participant.session_id == participant.session_id
    ).order_by(
        Participant.score.desc()
    ).all()

    leaderboard = []

    for rank, player in enumerate(
        participants,
        start=1
    ):
        leaderboard.append({
            "rank": rank,
            "name": player.name,
            "score": player.score
        })

    # Send leaderboard to everyone connected
    if quiz_session:
        await manager.broadcast(
            quiz_session.session_code,
            {
                "type": "leaderboard_update",
                "leaderboard": leaderboard
            }
        )

    return {
        "message": "Answer submitted",
        "correct": is_correct,
        "points": points,
        "total_score": participant.score
    }