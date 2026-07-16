"""Synthetic data for a 510-student university timetable. """
from dataclasses import dataclass

@dataclass(frozen=True)
class Room:
    id: str; block: str; floor: int; capacity: int; kind: str = "lecture"
@dataclass(frozen=True)
class Faculty:
    id: str; name: str; role: str; department: str
@dataclass(frozen=True)
class StudentGroup:
    id: str; department: str; semester: int; size: int
@dataclass(frozen=True)
class Session:
    id: str; group: StudentGroup; course: str; subject_id: str; candidates: tuple[str, ...]
    kind: str; duration: int; priority: str

GROUPS = [("AA", "CSE", 1, 60), ("AB", "CSE", 3, 55), ("AC", "ECE", 1, 60),
          ("AD", "BSC", 2, 55), ("AE", "BBA", 1, 55), ("AF", "EEE", 3, 50),
          ("AG", "POL", 1, 45), ("AH", "CIVIL", 5, 65), ("AI", "MECH", 3, 65)]
SUBJECTS = {
    "CSE": [("Programming Fundamentals", "CSE101"), ("Data Structures", "CSE201"), ("Discrete Mathematics", "MAT110"), ("Web Development", "CSE150")],
    "ECE": [("Circuit Theory", "ECE101"), ("Digital Electronics", "ECE201"), ("Signals and Systems", "ECE220"), ("Embedded Systems", "ECE250")],
    "BSC": [("Applied Physics", "BSC101"), ("Organic Chemistry", "BSC102"), ("Statistics", "BSC210"), ("Environmental Science", "BSC130")],
    "BBA": [("Principles of Management", "BBA101"), ("Financial Accounting", "BBA102"), ("Business Economics", "BBA210"), ("Marketing Basics", "BBA120")],
    "EEE": [("Electrical Machines", "EEE201"), ("Power Systems", "EEE220"), ("Control Systems", "EEE230"), ("Engineering Mathematics", "MAT120")],
    "POL": [("Political Theory", "POL101"), ("Indian Constitution", "POL102"), ("Public Administration", "POL210"), ("International Relations", "POL220")],
    "CIVIL": [("Structural Analysis", "CIV301"), ("Surveying", "CIV210"), ("Geotechnical Engineering", "CIV320"), ("Construction Management", "CIV330")],
    "MECH": [("Thermodynamics", "MEC201"), ("Fluid Mechanics", "MEC220"), ("Machine Design", "MEC310"), ("Manufacturing Process", "MEC230")],
}

def build_campus():
    rooms = []
    for block, floors in (("V", 4), ("SR", 4)):
        for floor in range(1, floors + 1):
            for number, capacity in enumerate((70, 70, 60, 60), 1): rooms.append(Room(f"{block}-{floor:02d}-{number:02d}", block, floor, capacity))
    for kind in ("physics_lab", "chemistry_lab", "computer_lab"):
        for number in range(1, 4): rooms.append(Room(f"X-{kind[:3].upper()}-{number}", "X", 1, 70, kind))
    names = ["Mr. Aditya", "Mrs. Harsha", "Dr. Meera", "Mr. Rahul", "Mrs. Kavya", "Dr. Nikhil", "Mr. Arjun", "Mrs. Priya", "Dr. Ananya", "Mr. Vivek", "Mrs. Sneha", "Dr. Rohan"]
    departments = list(SUBJECTS) + ["PHY", "CHEM", "COMP"]
    faculty = [Faculty(f"{dept}-F{n + 1:02d}", names[(n + d) % len(names)], "Professor" if n == 0 else "Assistant Professor", dept)
               for d, dept in enumerate(departments) for n in range(3)]
    return rooms, [StudentGroup(*row) for row in GROUPS], faculty

def build_sessions(groups, faculty):
    by_dept = {}
    for person in faculty: by_dept.setdefault(person.department, []).append(person)
    sessions = []
    for group in groups:
        subject_list = SUBJECTS[group.department]
        for index, (course, subject_id) in enumerate(subject_list):
            teachers = by_dept[group.department]
            candidate_ids = (teachers[index % 3].id, teachers[(index + 1) % 3].id)  # Professor/assistant substitute pair
            meetings = 2 if index < 3 else 1
            for meeting in range(1, meetings + 1):
                sessions.append(Session(f"{group.id}-{subject_id}-{meeting}", group, course, subject_id, candidate_ids, "lecture", 1, "High" if index < 3 else "Medium"))
        for lab_name, kind, dept in (("Physics Lab", "physics_lab", "PHY"), ("Chemistry Lab", "chemistry_lab", "CHEM"), ("Computer Lab", "computer_lab", "COMP")):
            teachers = by_dept[dept]
            sessions.append(Session(f"{group.id}-{kind}", group, lab_name, f"{dept}L{group.semester}01", (teachers[0].id, teachers[1].id), kind, 2, "High"))
    return sessions
