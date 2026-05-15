from datetime import date, timedelta

def calculate_streak(completions):
    if not completions:
        return 0

    completion_dates = {
        completion.completed_date
        for completion in completions
    }

    streak = 0
    current_date = date.today()

    while current_date in completion_dates:
        streak += 1
        current_date -= timedelta(days=1)

    return streak