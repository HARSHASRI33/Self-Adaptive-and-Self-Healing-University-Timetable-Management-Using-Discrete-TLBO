"""CSV and department/section reports in the requested column order."""
from collections import defaultdict 
import csv

HEADERS = ["Section", "Day", "Period", "Course", "Faculty", "Room", "Time", "Hours", "Priority", "SubjectID", "Type"]

def report_rows(scheduler, plan):
    rows = []
    groups = {}
    for session, placement in zip(scheduler.sessions, plan):
        groups[session.group.id] = session.group
        day, period = divmod(placement.slot, scheduler.period_count)
        period_name, time = scheduler.periods[period]
        if session.duration > 1:
            time = f"{time.split('-')[0]}-{scheduler.periods[period + session.duration - 1][1].split('-')[1]}"
        faculty = getattr(scheduler, "faculty_names", {}).get(placement.instructor, placement.instructor)
        rows.append((session.group.department, session.group.id, [session.group.id, scheduler.days[day], period_name,
                     session.course, faculty, scheduler.rooms[placement.room].id, time, session.duration,
                     session.priority, session.subject_id, "Lab" if session.kind != "lecture" else "Theory"]))
    # Friday 16:00–17:00 is fixed, campus-wide club time, not an optimised class.
    for group in groups.values():
        rows.append((group.department, group.id, [group.id, "Friday", "P6", "Club Activity", "Student Affairs",
                     "Club Area", "16:00-17:00", 1, "Mandatory", f"CLUB-{group.id}", "Club"]))
    return rows

def write_csv(filename, scheduler, plan):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file); writer.writerow(HEADERS)
        for _, _, row in sorted(report_rows(scheduler, plan)): writer.writerow(row)

def write_grouped_table(filename, scheduler, plan):
    grouped = defaultdict(lambda: defaultdict(list))
    for department, section, row in report_rows(scheduler, plan): grouped[department][section].append(row)
    line, minor = "=" * 136, "-" * 136
    with open(filename, "w", encoding="utf-8") as file:
        file.write("UNIVERSITY TIMETABLE — DEPARTMENT / SECTION VIEW\n" + line + "\n")
        for department in sorted(grouped):
            file.write(f"\nDEPARTMENT: {department}\n{line}\n")
            for section, entries in sorted(grouped[department].items()):
                file.write(f"SECTION: {section}\n{minor}\n")
                file.write(f"{'Period':<7} {'Course':<25} {'Day':<11} {'Faculty':<17} {'Room':<13} {'Time':<12} {'Hours':<6} {'Priority':<10} {'Subject ID':<12} {'Type':<8}\n{minor}\n")
                day_order = {day: i for i, day in enumerate(scheduler.days)}
                for row in sorted(entries, key=lambda x: (day_order[x[1]], x[2])):
                    _, day, period, course, faculty, room, time, hours, priority, subject_id, kind = row
                    file.write(f"{period:<7} {course:<25.25} {day:<11} {faculty:<17.17} {room:<13} {time:<12} {hours:<6} {priority:<10} {subject_id:<12} {kind:<8}\n")
                file.write(minor + "\n")

def print_summary(scheduler, plan):
    score, breakdown = scheduler.score(plan)
    print(f"Score: {score}; hard conflicts: {sum(breakdown.get(k, 0) for k in ('room_clash', 'faculty_clash', 'group_clash'))}")
