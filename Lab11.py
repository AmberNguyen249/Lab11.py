import os
import matplotlib.pyplot as plt

# Load student ID → name
def load_students(filename):
    students = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            sid = line[:3]
            name = line[3:].strip()
            students[sid] = name
    return students

# Load assignments: name, ID, points
def load_assignments(filename):
    assignments = {}
    name_to_id = {}
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            aid = lines[i + 1]
            points = int(lines[i + 2])
            assignments[aid] = (name, points)
            name_to_id[name] = aid
    return assignments, name_to_id

# Load submissions from all files in submissions folder
def load_submissions(folder):
    submissions = {}  # (student_id, assignment_id) → percent (as a float)
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        with open(filepath) as f:
            for line in f:
                sid, aid, percent = line.strip().split("|")
                submissions[(sid, aid)] = float(percent) / 100  # convert to 0-1 scale
    return submissions

# Calculate total grade for a student
def calculate_student_grade(student_name):
    student_id = None
    for sid, name in students.items():
        if name == student_name:
            student_id = sid
            break

    if student_id is None:
        print("Student not found")
        return

    total_score = 0
    for aid, (aname, points) in assignments.items():
        percent = submissions.get((student_id, aid), 0)
        total_score += percent * points

    grade = round((total_score / 1000) * 100)
    print(f"{grade}%")

# Get stats for assignment
def assignment_statistics(assignment_name):
    if assignment_name not in assignment_name_to_id:
        print("Assignment not found")
        return

    aid = assignment_name_to_id[assignment_name]
    points = assignments[aid][1]

    scores = [
        submissions[(sid, aid)] * points
        for sid in students
        if (sid, aid) in submissions
    ]

    if not scores:
        print("Assignment not found")
        return

    percentages = [round(score / points * 100) for score in scores]
    print(f"Min: {min(percentages)}%")
    print(f"Avg: {round(sum(percentages) // len(percentages))}%")
    print(f"Max: {max(percentages)}%")

# Show histogram of scores for assignment
def display_assignment_graph(assignment_name):
    if assignment_name not in assignment_name_to_id:
        print("Assignment not found")
        return

    aid = assignment_name_to_id[assignment_name]
    points = assignments[aid][1]

    scores = [
        submissions[(sid, aid)] * 100
        for sid in students
        if (sid, aid) in submissions
    ]

    if not scores:
        print("Assignment not found")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"{assignment_name} Score Distribution")
    plt.xlabel("Score (%)")
    plt.ylabel("Number of Students")
    plt.show()

# Load everything
students = load_students("data/students.txt")
assignments, assignment_name_to_id = load_assignments("data/assignments.txt")
submissions = load_submissions("data/submissions")

# Menu
def main():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")

    selection = input("\nEnter your selection: ")

    if selection == "1":
        student_name = input("What is the student's name: ")
        calculate_student_grade(student_name)

    elif selection == "2":
        assignment_name = input("What is the assignment name: ")
        assignment_statistics(assignment_name)

    elif selection == "3":
        assignment_name = input("What is the assignment name: ")
        display_assignment_graph(assignment_name)

if __name__ == "__main__":
    main()
