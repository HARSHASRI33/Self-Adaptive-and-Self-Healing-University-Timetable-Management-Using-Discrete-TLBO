"""Discrete TLBO scheduler with adaptive mutation and constrained self-healing.""" 
from dataclasses import dataclass
from collections import Counter, defaultdict
import random

@dataclass(frozen=True)
class Placement:
    slot: int; room: int; instructor: str

class Timetabler:
    HARD = 100_000
    def __init__(self, rooms, sessions, days=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"), periods=None):
        self.rooms, self.sessions, self.days = rooms, sessions, list(days)
        self.periods = periods or [("P1", "09:00-10:00"), ("P2", "10:00-11:00"), ("P3", "12:00-13:00"), ("P4", "14:00-15:00"), ("P5", "15:00-16:00"), ("P6", "16:00-17:00")]
        self.period_count, self.slot_count = len(self.periods), len(self.days) * len(self.periods)
        self.unavailable = defaultdict(set)       # faculty id -> occupied/absent slots
        self.blocked_rooms = defaultdict(set)     # room index -> unavailable slots

    def slot_label(self, slot):
        return f"{self.days[slot // self.period_count]} {self.periods[slot % self.period_count][1]}"

    def occupied(self, placement, duration): return range(placement.slot, placement.slot + duration)
    def valid_start_slots(self, duration):
        result = []
        for slot in range(self.slot_count):
            day, period = divmod(slot, self.period_count)
            # No Saturday/Sunday (only five days); P6 Friday is fixed club activity, not a class.
            if day == 4 and period == 5: continue
            if duration == 1: result.append(slot)
            # Labs must be two uninterrupted class hours; never cross tea/lunch breaks.
            elif period in (0, 3, 4) and not (day == 4 and period >= 4): result.append(slot)
        return result
    def rooms_for(self, session):
        return [i for i, r in enumerate(self.rooms) if r.kind == session.kind and r.capacity >= session.group.size]

    def score(self, timetable, baseline=None):
        b, room_used, teacher_used, group_used = Counter(), Counter(), Counter(), Counter()
        for session, p in zip(self.sessions, timetable):
            if p.slot not in self.valid_start_slots(session.duration): b["crosses_day"] += 1; continue
            room = self.rooms[p.room]
            if room.kind != session.kind or room.capacity < session.group.size: b["room_invalid"] += 1
            if p.instructor not in session.candidates: b["invalid_substitute"] += 1
            for slot in self.occupied(p, session.duration):
                room_used[slot, p.room] += 1; teacher_used[slot, p.instructor] += 1; group_used[slot, session.group.id] += 1
                if slot in self.unavailable[p.instructor]: b["faculty_absent"] += 1
                if slot in self.blocked_rooms[p.room]: b["blocked_room"] += 1
                if slot % self.period_count == 5: b["late"] += 1
        for name, used in (("room_clash", room_used), ("faculty_clash", teacher_used), ("group_clash", group_used)):
            b[name] = sum(n - 1 for n in used.values() if n > 1)
        b["changes"] = sum(a != z for a, z in zip(timetable, baseline)) if baseline is not None else 0
        hard = sum(b[k] for k in ("crosses_day", "room_invalid", "invalid_substitute", "faculty_absent", "blocked_room", "room_clash", "faculty_clash", "group_clash"))
        return hard * self.HARD + 5 * b["late"] + 50 * b["changes"], dict(b)

    def greedy_seed(self, rng):
        """Creates a feasible timetable first; TLBO then improves it."""
        order = sorted(range(len(self.sessions)), key=lambda i: (self.sessions[i].kind == "lecture", -self.sessions[i].group.size))
        plan = [None] * len(self.sessions)
        room_used, teacher_used, group_used = set(), set(), set()
        for i in order:
            s = self.sessions[i]; candidate = None
            # Sampling is fast because this campus deliberately has spare capacity.
            for _ in range(2_000):
                trial = Placement(rng.choice(self.valid_start_slots(s.duration)), rng.choice(self.rooms_for(s)), rng.choice(s.candidates))
                occupied = list(self.occupied(trial, s.duration))
                invalid = (any((x, trial.room) in room_used or (x, trial.instructor) in teacher_used or (x, s.group.id) in group_used for x in occupied)
                           or any(x in self.unavailable[trial.instructor] or x in self.blocked_rooms[trial.room] for x in occupied))
                if not invalid: candidate = trial; break
            if candidate is None: raise RuntimeError(f"No feasible placement for {s.id}; add rooms, periods, or faculty.")
            plan[i] = candidate
            for slot in self.occupied(candidate, s.duration):
                room_used.add((slot, candidate.room)); teacher_used.add((slot, candidate.instructor)); group_used.add((slot, s.group.id))
        return plan

    def mutate(self, plan, rng, indices, rate):
        result = plan.copy()
        for i in indices:
            if rng.random() < rate:
                s = self.sessions[i]
                result[i] = Placement(rng.choice(self.valid_start_slots(s.duration)), rng.choice(self.rooms_for(s)), rng.choice(s.candidates))
        return result

    def optimise(self, baseline=None, movable=None, population_size=12, generations=20, seed=10):
        rng = random.Random(seed); movable = set(range(len(self.sessions))) if movable is None else set(movable)
        start = baseline.copy() if baseline is not None else self.greedy_seed(rng)
        population = [start] + [self.mutate(start, rng, movable, .18) for _ in range(population_size - 1)]
        score = lambda p: self.score(p, baseline)[0]
        for g in range(generations):
            costs = [score(p) for p in population]; teacher = population[costs.index(min(costs))]
            rate = .16 * (1 - g / generations) + .02  # self-adaptive exploration
            new = [teacher]
            for learner_index, learner in enumerate(population[1:], 1):
                learner_cost = costs[learner_index]
                peer_index = rng.randrange(len(population)); peer = population[peer_index]
                candidate = learner.copy()
                for i in movable:
                    # Learner phase: use a better peer; otherwise use the teacher.
                    if rng.random() < .22: candidate[i] = peer[i] if costs[peer_index] < learner_cost else teacher[i]
                candidate = self.mutate(candidate, rng, movable, rate)
                new.append(candidate if score(candidate) < learner_cost else learner)
            population = new
        return min(population, key=score)

    def affected_and_neighbours(self, baseline):
        """Allow affected classes and their direct conflicts to move during healing."""
        _, issues = self.score(baseline, baseline); affected = set()
        for i, (s, p) in enumerate(zip(self.sessions, baseline)):
            if any(x in self.unavailable[p.instructor] or x in self.blocked_rooms[p.room] for x in self.occupied(p, s.duration)): affected.add(i)
        # permit clashes with disrupted sessions to move too; this prevents a repair dead-end.
        for i in list(affected):
            a, p = self.sessions[i], baseline[i]
            for j, (b, q) in enumerate(zip(self.sessions, baseline)):
                if set(self.occupied(p, a.duration)) & set(self.occupied(q, b.duration)) and (p.room == q.room or p.instructor == q.instructor or a.group.id == b.group.id): affected.add(j)
        return affected
