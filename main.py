from data import build_campus, build_sessions  # type: ignore[reportMissingImports]
from scheduler import Timetabler  # type: ignore[reportMissingImports]
from reports import write_csv, write_grouped_table, print_summary  # type: ignore[reportMissingImports]
import json

rooms, groups, faculty = build_campus()
sessions = build_sessions(groups, faculty)
system = Timetabler(rooms, sessions)
system.faculty_names = {person.id: person.name for person in faculty}
print(f"Campus: {sum(g.size for g in groups)} students, {len(groups)} sections, {len(rooms)} rooms, {len(sessions)} sessions")
initial = system.optimise(generations=20)
print("Initial timetable created."); print_summary(system, initial)
write_csv("initial_timetable.csv", system, initial)
write_grouped_table("initial_timetable_by_department.txt", system, initial)
with open("initial_plan.json", "w", encoding="utf-8") as f:
    json.dump([{"slot": p.slot, "room": p.room, "instructor": p.instructor} for p in initial], f, indent=2)
print("Created: initial_timetable.csv, initial_timetable_by_department.txt, initial_plan.json")
