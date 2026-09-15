import json

from app.config import settings


def generate_questions(
    topic: str,
    difficulty: str,
    question_type: str,
    count: int
):

    if not settings.openai_api_key:

        return generate_demo_questions(
            topic,
            difficulty,
            count
        )


    from openai import OpenAI


    try:

        client = OpenAI(
            api_key=settings.openai_api_key
        )


        prompt = f"""
You are an expert quiz question generator.

Generate exactly {count} multiple-choice questions.

Topic: {topic}

Difficulty: {difficulty}

Question type: {question_type}

Return ONLY valid JSON.

Use this structure:

{{
    "questions": [
        {{
            "question_text": "Question",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "explanation": "Explanation"
        }}
    ]
}}

Rules:

- Generate exactly {count} questions.
- Each question must have four options.
- Correct answer must be A, B, C, or D.
- Avoid duplicate questions.
- Questions must match the topic.
- Match the requested difficulty.
"""


        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                        "You generate high-quality quiz questions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )


        content = (
            response
            .choices[0]
            .message
            .content
        )


        data = json.loads(content)


        return data["questions"]


    except Exception as error:

        print(
            "OpenAI generation failed:"
        )

        print(error)

        print(
            "Using demo questions instead."
        )


        return generate_demo_questions(
            topic,
            difficulty,
            count
        )


# ------------------------------------------------
# DEMO QUESTIONS
# ------------------------------------------------

def generate_demo_questions(
    topic: str,
    difficulty: str,
    count: int
):

    questions = [

        {
            "question_text":
                f"What is commonly used to write programs in {topic}?",

            "option_a":
                "Python",

            "option_b":
                "HTML only",

            "option_c":
                "CSS only",

            "option_d":
                "SQL only",

            "correct_answer":
                "A",

            "explanation":
                "Python is a popular programming language."
        },

        {
            "question_text":
                f"Which concept is important when learning {topic}?",

            "option_a":
                "Variables",

            "option_b":
                "Only images",

            "option_c":
                "Only videos",

            "option_d":
                "None",

            "correct_answer":
                "A",

            "explanation":
                "Variables are fundamental programming concepts."
        },

        {
            "question_text":
                "Which of these is a programming language?",

            "option_a":
                "Python",

            "option_b":
                "JPEG",

            "option_c":
                "PNG",

            "option_d":
                "PDF",

            "correct_answer":
                "A",

            "explanation":
                "Python is a programming language."
        },

        {
            "question_text":
                "What does API commonly stand for?",

            "option_a":
                "Application Programming Interface",

            "option_b":
                "Application Program Internet",

            "option_c":
                "Advanced Python Input",

            "option_d":
                "Automated Program Installation",

            "correct_answer":
                "A",

            "explanation":
                "API stands for Application Programming Interface."
        },

        {
            "question_text":
                "Which protocol is commonly used for secure web traffic?",

            "option_a":
                "HTTPS",

            "option_b":
                "FTP only",

            "option_c":
                "SMTP only",

            "option_d":
                "SSH only",

            "correct_answer":
                "A",

            "explanation":
                "HTTPS secures HTTP communication using TLS."
        }

    ]


    return questions[:count]