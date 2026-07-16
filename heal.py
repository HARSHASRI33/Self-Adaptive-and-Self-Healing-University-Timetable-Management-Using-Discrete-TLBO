"""Run this AFTER main.py to repair a saved timetable after a disruption."""
# All project files are siblings in this folder. Run with: python heal.py
from data import build_campus, build_sessions
from data import build_campus, build_sessions  # type: ignore[reportMissingImports]
from scheduler import Timetabler, Placement  # type: ignore[reportMissingImports]
from reports import write_csv, write_grouped_table, print_summary  # type: ignore[reportMissingImports]
import json


rooms, groups, faculty = build_campus()
system = Timetabler(rooms, build_sessions(groups, faculty))
system.faculty_names = {person.id: person.name for person in faculty}
with open("initial_plan.json", encoding="utf-8") as f:
    original = [Placement(**item) for item in json.load(f)]

# Demonstration absence: select a real CSE class, then make its scheduled faculty absent.
# For a real event, replace these lines with a known faculty id and slot number.
target = next(i for i, session in enumerate(system.sessions) if session.group.department == "CSE")
system.unavailable[original[target].instructor].add(original[target].slot)

affected = system.affected_and_neighbours(original)
repaired = system.optimise(baseline=original, movable=affected, generations=25, seed=22)
print(f"Self-healing complete. Sessions allowed to move: {len(affected)}")
print_summary(system, repaired)
write_csv("repaired_timetable.csv", system, repaired)
write_grouped_table("repaired_timetable_by_department.txt", system, repaired)
print("Created: repaired_timetable.csv and repaired_timetable_by_department.txt")
