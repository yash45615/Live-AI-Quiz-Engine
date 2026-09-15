from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.session import QuizSession
from app.models.participant import Participant
from app.services.session_service import generate_session_code
from app.websocket.manager import manager


router = APIRouter(
    prefix="/sessions",
    tags=["Quiz Sessions"]
)


# --------------------------------------------------
# CREATE SESSION
# --------------------------------------------------

@router.post("/create/{quiz_id}")
def create_session(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    question_count = db.query(
        Question
    ).filter(
        Question.quiz_id == quiz_id
    ).count()

    if question_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Generate questions before starting a session"
        )

    session_code = generate_session_code()

    while db.query(QuizSession).filter(
        QuizSession.session_code == session_code
    ).first():

        session_code = generate_session_code()

    quiz_session = QuizSession(
        quiz_id=quiz_id,
        session_code=session_code,
        status="waiting",
        current_question=0
    )

    db.add(quiz_session)
    db.commit()
    db.refresh(quiz_session)

    return {
        "message": "Quiz session created",
        "session_id": quiz_session.id,
        "session_code": quiz_session.session_code,
        "quiz_id": quiz_session.quiz_id,
        "status": quiz_session.status
    }


# --------------------------------------------------
# JOIN SESSION
# --------------------------------------------------

@router.post("/{session_code}/join")
def join_session(
    session_code: str,
    name: str,
    db: Session = Depends(get_db)
):

    quiz_session = db.query(
        QuizSession
    ).filter(
        QuizSession.session_code == session_code
    ).first()

    if not quiz_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if quiz_session.status != "waiting":
        raise HTTPException(
            status_code=400,
            detail="This quiz has already started"
        )

    existing = db.query(
        Participant
    ).filter(
        Participant.session_id == quiz_session.id,
        Participant.name == name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Name already taken"
        )

    participant = Participant(
        session_id=quiz_session.id,
        name=name,
        score=0
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return {
        "message": "Successfully joined quiz",
        "participant_id": participant.id,
        "name": participant.name,
        "session_code": session_code,
        "quiz_id": quiz_session.quiz_id
    }


# --------------------------------------------------
# START SESSION
# --------------------------------------------------

@router.post("/{session_code}/start")
async def start_session(
    session_code: str,
    db: Session = Depends(get_db)
):

    quiz_session = db.query(
        QuizSession
    ).filter(
        QuizSession.session_code == session_code
    ).first()

    if not quiz_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if quiz_session.status != "waiting":
        raise HTTPException(
            status_code=400,
            detail="Session cannot be started"
        )

    quiz_session.status = "active"
    quiz_session.current_question = 0

    db.commit()

    await manager.broadcast(
        session_code,
        {
            "type": "quiz_started",
            "question_number": 0
        }
    )

    return {
        "message": "Quiz started",
        "session_code": session_code,
        "status": "active",
        "current_question": 0
    }


# --------------------------------------------------
# NEXT QUESTION
# --------------------------------------------------

@router.post("/{session_code}/next")
async def next_question(
    session_code: str,
    db: Session = Depends(get_db)
):

    quiz_session = db.query(
        QuizSession
    ).filter(
        QuizSession.session_code == session_code
    ).first()

    if not quiz_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if quiz_session.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Quiz is not active"
        )

    question_count = db.query(
        Question
    ).filter(
        Question.quiz_id == quiz_session.quiz_id
    ).count()

    next_question_number = (
        quiz_session.current_question + 1
    )

    if next_question_number >= question_count:
        quiz_session.status = "finished"

        db.commit()

        await manager.broadcast(
            session_code,
            {
                "type": "quiz_finished"
            }
        )

        return {
            "message": "Quiz finished",
            "status": "finished"
        }

    quiz_session.current_question = (
        next_question_number
    )

    db.commit()

    await manager.broadcast(
        session_code,
        {
            "type": "question_update",
            "question_number": next_question_number
        }
    )

    return {
        "message": "Next question",
        "question_number": next_question_number,
        "status": quiz_session.status
    }


# --------------------------------------------------
# PREVIOUS QUESTION
# --------------------------------------------------

@router.post("/{session_code}/previous")
async def previous_question(
    session_code: str,
    db: Session = Depends(get_db)
):

    quiz_session = db.query(
        QuizSession
    ).filter(
        QuizSession.session_code == session_code
    ).first()

    if not quiz_session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if quiz_session.current_question <= 0:
        raise HTTPException(
            status_code=400,
            detail="Already at first question"
        )

    quiz_session.current_question -= 1

    db.commit()

    await manager.broadcast(
        session_code,
        {
            "type": "question_update",
            "question_number":
                quiz_session.current_question
        }
    )

    return {
        "message": "Previous question",
        "question_number":
            quiz_session.current_question
    }