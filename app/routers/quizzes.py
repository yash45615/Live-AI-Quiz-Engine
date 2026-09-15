from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quiz import Quiz
from app.models.user import User
from app.schemas.quiz import QuizCreate


router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


@router.post("/")
def create_quiz(
    request: QuizCreate,
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = (
        db.query(User)
        .filter(User.id == teacher_id)
        .first()
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    if teacher.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can create quizzes"
        )

    if request.question_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Question count must be greater than zero"
        )

    quiz = Quiz(
        title=request.title,
        topic=request.topic,
        difficulty=request.difficulty,
        question_type=request.question_type,
        question_count=request.question_count,
        teacher_id=teacher_id
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return {
        "message": "Quiz created successfully",
        "quiz_id": quiz.id,
        "title": quiz.title,
        "topic": quiz.topic,
        "difficulty": quiz.difficulty,
        "question_type": quiz.question_type,
        "question_count": quiz.question_count
    }


@router.get("/")
def get_quizzes(
    db: Session = Depends(get_db)
):

    quizzes = db.query(Quiz).all()

    return quizzes


@router.get("/{quiz_id}")
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    return quiz