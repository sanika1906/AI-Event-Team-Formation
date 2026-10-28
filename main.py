import tkinter as tk
from tkinter import ttk, messagebox

from csp_solver import students, generate_teams, REQUIRED_SKILLS

ALL_SKILLS = [
    "Coding",
    "Designing",
    "Management",
    "Presentation",
    "Testing",
    "Documentation"
]


def display(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)


def show_students():
    result = "REGISTERED STUDENTS\n"
    result += "=" * 55 + "\n\n"

    for student in students:
        status = "Available" if student["available"] else "Not Available"

        result += f"Name: {student['name']}\n"
        result += f"Skills: {', '.join(student['skills'])}\n"
        result += f"Status: {status}\n"
        result += "-" * 40 + "\n"

    display(result)


def add_student():
    name = name_entry.get().strip()

    selected_skills = [
        skill for skill, variable in skill_vars.items()
        if variable.get()
    ]

    if not name:
        messagebox.showerror(
            "Missing Name", "Please enter the student's name."
        )
        return

    if not selected_skills:
        messagebox.showerror(
            "Missing Skills", "Please select at least one skill."
        )
        return

    if any(s["name"].lower() == name.lower() for s in students):
        messagebox.showerror(
            "Duplicate Name", "This student is already registered."
        )
        return

    available = availability_var.get()

    students.append({
        "name": name,
        "skills": selected_skills,
        "available": available
    })

    name_entry.delete(0, tk.END)

    for variable in skill_vars.values():
        variable.set(False)

    availability_var.set(True)

    messagebox.showinfo(
        "Success", f"{name} has been registered successfully."
    )

    show_students()


def create_teams():
    try:
        team_size = int(team_size_box.get())

        if team_size < len(REQUIRED_SKILLS):
            messagebox.showerror(
                "Team Size Error",
                "Team size must be at least 4 because four main "
                "skills must be covered."
            )
            return

        teams = generate_teams(team_size)

        result = "AI-GENERATED EVENT TEAMS\n"
        result += "=" * 55 + "\n\n"

        if not teams:
            result += (
                "No valid team could be formed.\n\n"
                "Possible reasons:\n"
                "- Not enough available students.\n"
                "- Required skills are missing.\n"
                "- Some students are unavailable.\n"
            )
            display(result)
            return

        for number, team in enumerate(teams, start=1):
            team_skills = set()

            result += f"TEAM {number}\n"
            result += "-" * 40 + "\n"

            for student in team:
                result += (
                    f"{student['name']} - "
                    f"{', '.join(student['skills'])}\n"
                )
                team_skills.update(student["skills"])

            covered = [
                skill for skill in REQUIRED_SKILLS
                if skill in team_skills
            ]

            result += "\nAI Decision Explanation:\n"
            result += (
                "The team was selected because all members are "
                "available and the team covers the required skills.\n"
            )
            result += "Skills covered: " + ", ".join(covered) + "\n\n"

        result += "=" * 55 + "\n"
        result += f"Total teams formed: {len(teams)}\n"
        result += "AI Method: CSP with Backtracking\n"

        display(result)

    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Please select a valid team size."
        )


def show_csp_model():
    result = "CONSTRAINT SATISFACTION PROBLEM (CSP)\n"
    result += "=" * 55 + "\n\n"

    result += "1. Variables:\n"
    result += "   The team positions to be filled by students.\n\n"

    result += "2. Domains:\n"
    result += "   All registered students who are available.\n\n"

    result += "3. Constraints:\n"
    result += "   - Team size must match the selected size.\n"
    result += "   - Every team must cover the four required skills.\n"
    result += "   - Unavailable students cannot be selected.\n"
    result += "   - A student cannot belong to two teams.\n\n"

    result += "4. Backtracking:\n"
    result += (
        "   The algorithm tries a student selection. If it cannot "
        "form a valid team, it removes that choice and tries another.\n\n"
    )

    result += "5. Goal:\n"
    result += (
        "   Form valid event teams while satisfying all constraints.\n"
    )

    display(result)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("AI Event Team Formation System")
root.geometry("1000x750")
root.configure(bg="#eaf2f8")

heading = tk.Label(
    root,
    text="AI EVENT TEAM FORMATION SYSTEM",
    font=("Arial", 21, "bold"),
    bg="#eaf2f8",
    fg="#163a5f"
)
heading.pack(pady=(15, 5))

subtitle = tk.Label(
    root,
    text="Intelligent Team Allocation Using CSP and Backtracking",
    font=("Arial", 11),
    bg="#eaf2f8",
    fg="#34495e"
)
subtitle.pack(pady=(0, 10))


# Student registration area
registration = tk.LabelFrame(
    root,
    text="Student Registration",
    font=("Arial", 11, "bold"),
    bg="#eaf2f8",
    padx=10,
    pady=8
)
registration.pack(fill="x", padx=15, pady=5)

tk.Label(
    registration,
    text="Student Name:",
    bg="#eaf2f8"
).grid(row=0, column=0, sticky="w", padx=5, pady=5)

name_entry = tk.Entry(registration, width=22)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(
    registration,
    text="Select Skills:",
    bg="#eaf2f8"
).grid(row=1, column=0, sticky="nw", padx=5, pady=5)

skills_frame = tk.Frame(registration, bg="#eaf2f8")
skills_frame.grid(row=1, column=1, columnspan=3, sticky="w")

skill_vars = {}

for index, skill in enumerate(ALL_SKILLS):
    variable = tk.BooleanVar(value=False)
    skill_vars[skill] = variable

    tk.Checkbutton(
        skills_frame,
        text=skill,
        variable=variable,
        bg="#eaf2f8"
    ).grid(row=index // 3, column=index % 3, sticky="w", padx=4)

availability_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    registration,
    text="Available for event",
    variable=availability_var,
    bg="#eaf2f8"
).grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Button(
    registration,
    text="Add Student",
    command=add_student,
    bg="#198754",
    fg="white",
    width=15
).grid(row=2, column=2, padx=10, pady=5)


# Team controls
controls = tk.Frame(root, bg="#eaf2f8")
controls.pack(pady=10)

tk.Label(
    controls,
    text="Team Size:",
    font=("Arial", 11),
    bg="#eaf2f8"
).grid(row=0, column=0, padx=5)

team_size_box = ttk.Combobox(
    controls,
    values=[4, 5, 6],
    width=6,
    state="readonly"
)
team_size_box.set(4)
team_size_box.grid(row=0, column=1, padx=5)

tk.Button(
    controls,
    text="Generate Teams",
    command=create_teams,
    bg="#1e88e5",
    fg="white",
    width=16
).grid(row=0, column=2, padx=5)

tk.Button(
    controls,
    text="Show Students",
    command=show_students,
    width=14
).grid(row=0, column=3, padx=5)

tk.Button(
    controls,
    text="Explain CSP",
    command=show_csp_model,
    width=14
).grid(row=0, column=4, padx=5)


# Output area
output = tk.Text(
    root,
    height=20,
    width=110,
    font=("Consolas", 10),
    wrap="word"
)
output.pack(padx=15, pady=10, fill="both", expand=True)

show_students()
root.mainloop()