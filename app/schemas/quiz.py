from pydantic import BaseModel


class QuizCreate(BaseModel):
    title: str
    topic: str
    difficulty: str
    question_type: str
    question_count: int


class QuizResponse(BaseModel):
    id: int
    title: str
    topic: str
    difficulty: str
    question_type: str
    question_count: int

    class Config:
        from_attributes = True