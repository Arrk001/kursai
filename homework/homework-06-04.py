def weekly_workout_tracker(goal=150):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workouts = {}

    # Collect workout minutes for each day
    for day in days:
        while True:
            try:
                minutes = int(input(f"Minutes exercised on {day}: "))
                if minutes < 0:
                    raise ValueError("Minutes can't be negative.")
                workouts[day] = minutes
                break
            except ValueError as e:
                print(f"Invalid input: {e}")

    # Calculate summary
    total_minutes = sum(workouts.values())
    best_day = max(workouts, key=workouts.get)

    # Output results
    print("Total minutes exercised:", total_minutes, "\nBest workout day:", best_day, "\nGoal met!" if total_minutes >= goal else "Goal not met.")

# Run the tracker
weekly_workout_tracker()