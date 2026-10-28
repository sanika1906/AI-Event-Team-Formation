# AI Event Team Formation System
# Using Constraint Satisfaction Problem (CSP)

REQUIRED_SKILLS = [
    "Coding",
    "Designing",
    "Management",
    "Presentation"
]

students = [
    {"name": "Aarav", "skills": ["Coding", "Testing"], "available": True},
    {"name": "Diya", "skills": ["Designing"], "available": True},
    {"name": "Kabir", "skills": ["Management"], "available": True},
    {"name": "Meera", "skills": ["Presentation"], "available": True},
    {"name": "Rohan", "skills": ["Coding", "Testing"], "available": True},
    {"name": "Isha", "skills": ["Designing", "Documentation"], "available": True},
    {"name": "Aditya", "skills": ["Coding", "Management"], "available": True},
    {"name": "Sneha", "skills": ["Presentation", "Designing"], "available": True}
]


def is_valid_team(team):
    team_skills = set()

    for student in team:
        if not student["available"]:
            return False

        team_skills.update(student["skills"])

    return all(skill in team_skills for skill in REQUIRED_SKILLS)


def find_team(student_list, index, team, team_size):
    if len(team) == team_size:
        if is_valid_team(team):
            return team.copy()
        return None

    if index >= len(student_list):
        return None

    # Try selecting the current student
    team.append(student_list[index])

    result = find_team(
        student_list, index + 1, team, team_size
    )

    if result is not None:
        return result

    # Backtrack: remove the student and try another choice
    team.pop()

    return find_team(
        student_list, index + 1, team, team_size
    )


def generate_teams(team_size=4):
    available_students = [
        student for student in students
        if student["available"]
    ]

    teams = []
    remaining = available_students.copy()

    while len(remaining) >= team_size:
        team = find_team(remaining, 0, [], team_size)

        if team is None:
            break

        teams.append(team)

        # A student cannot be assigned to two teams
        for student in team:
            remaining.remove(student)

    return teams