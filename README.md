# Self-Adaptive and Self-Healing University Timetable Management Using Discrete Teaching-Learning-Based Optimization (TLBO)

## Overview
This project presents a Python-based university timetable management system that generates conflict-free academic schedules using a Discrete Teaching-Learning-Based Optimization (TLBO)-inspired approach. The system also includes a self-healing mechanism that repairs timetable disruptions such as faculty unavailability or blocked classrooms while minimizing changes to the existing schedule.

The project was developed as part of a research study on intelligent timetable optimization.

## Novelty
The novelty of this project lies in combining self-adaptive timetable optimization with a self-healing repair mechanism in a single framework. Instead of regenerating the entire timetable after disruptions such as faculty absence or room unavailability, the system repairs only the affected timetable entries while preserving the remaining schedule. The project also integrates conflict detection, constraint validation, and automated timetable generation into a Python-based implementation, making it suitable for academic scheduling and future research.

## Features
- Automatic university timetable generation
- Conflict detection and validation
- Self-adaptive optimization strategy
- Self-healing timetable repair
- Faculty substitution support
- Classroom and laboratory allocation
- CSV export of generated timetable
- Department-wise and section-wise timetable generation

## Project Structure
├── main.py                 # Main execution file
├── data.py                 # Dataset (faculty, courses, rooms, sections)
├── tlbo.py                 # TLBO-inspired optimization
├── fitness.py              # Fitness evaluation
├── constraints.py          # Constraint validation
├── self_healing.py         # Timetable repair module
├── output/
│   ├── timetable.csv
│   └── reports/
├── paper/
│   ├── research_paper.tex
│   └── references.bib
├── README.md

## Technologies Used
- Python 3.x
- Pandas
- CSV
- LaTeX (IEEE Conference Format)
- Overleaf

## Constraints Considered
### Hard Constraints
- No faculty conflicts
- No classroom conflicts
- No section conflicts
- Classroom capacity validation
- Laboratory allocation
- Faculty availability
- Blocked room handling

### Soft Constraints
- Reduce late-hour classes
- Minimize timetable changes
- Balance faculty workload
- Improve timetable quality

## Workflow
1. Load university dataset
2. Generate initial timetable
3. Validate timetable constraints
4. Evaluate timetable fitness
5. Improve timetable using TLBO-inspired optimization
6. Detect timetable disruptions
7. Repair affected sessions using self-healing
8. Export final timetable

## Research Contributions
- Self-Adaptive timetable optimization
- Self-Healing timetable repair
- Discrete TLBO-inspired scheduling
- Minimum-change timetable recovery
- Automatic timetable reporting

## Output
The system generates:
- Optimized timetable
- CSV output
- Department-wise timetable
- Section-wise timetable
- Conflict evaluation report

## Future Improvements
- Integration with university ERP systems
- Real-time faculty leave management
- Student elective scheduling
- Multi-campus timetable support
- Hybrid optimization using GA and PSO
- Web-based timetable management portal

## Research Paper
**Title
Self-Adaptive and Self-Healing University Timetable Management Using Discrete Teaching-Learning-Based Optimization

## Author
**Harsha Sri Eluri
Department of Computer Science and Engineering
SRM University AP, Amaravati, India
