from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quiz import Quiz
from app.models.question import Question
from app.services.ai_service import generate_questions


router = APIRouter(
    prefix="/questions",
    tags=["AI Questions"]
)


@router.post("/generate/{quiz_id}")
def generate_quiz_questions(
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

    existing_questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .count()
    )

    if existing_questions > 0:
        raise HTTPException(
            status_code=400,
            detail="Questions already generated for this quiz"
        )

    generated_questions = generate_questions(
        topic=quiz.topic,
        difficulty=quiz.difficulty,
        question_type=quiz.question_type,
        count=quiz.question_count
    )

    saved_questions = []

    for item in generated_questions:

        question = Question(
            quiz_id=quiz.id,
            question_text=item["question_text"],
            option_a=item["option_a"],
            option_b=item["option_b"],
            option_c=item["option_c"],
            option_d=item["option_d"],
            correct_answer=item["correct_answer"],
            explanation=item.get("explanation")
        )

        db.add(question)

        saved_questions.append(question)

    db.commit()

    for question in saved_questions:
        db.refresh(question)

    return {
        "message": "Questions generated successfully",
        "quiz_id": quiz.id,
        "count": len(saved_questions),
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation
            }
            for q in saved_questions
        ]
    }


@router.get("/{quiz_id}")
def get_questions(
    quiz_id: int,
    db: Session = Depends(get_db)
):

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .all()
    )

    return questions