def calculate_score(
    selected_answer: str,
    correct_answer: str,
    time_taken: float
) -> int:

    selected_answer = selected_answer.upper()
    correct_answer = correct_answer.upper()

    if selected_answer != correct_answer:
        return 0

    base_points = 500

    if time_taken <= 5:
        speed_bonus = 500
    elif time_taken <= 10:
        speed_bonus = 400
    elif time_taken <= 20:
        speed_bonus = 300
    elif time_taken <= 30:
        speed_bonus = 200
    else:
        speed_bonus = 100

    return base_points + speed_bonus