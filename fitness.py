import numpy as np
from collections import Counter

class ExamFitness:
    def __init__(self, classrooms_df, timeslot_df):
        self.classrooms = classrooms_df
        self.timeslots = timeslot_df

        self.room_capacities = classrooms_df["capacity"].tolist()
        self.num_rooms = len(self.room_capacities)

        # Dummy student count per exam (boleh upgrade jika ada data sebenar)
        self.exam_students = [30] * len(timeslot_df)

    def evaluate(self, solution):
        """
        solution: list of timeslot assignment for each exam
        """
        hard_penalty = 0
        soft_penalty = 0

        # =========================
        # HARD CONSTRAINTS
        # =========================

        # 1. Multiple exams in same timeslot & room
        timeslot_count = Counter(solution)
        for count in timeslot_count.values():
            if count > self.num_rooms:
                hard_penalty += (count - self.num_rooms) * 50

        # 2. Room capacity violation
        for exam_idx, timeslot in enumerate(solution):
            room_idx = exam_idx % self.num_rooms
            if self.exam_students[exam_idx] > self.room_capacities[room_idx]:
                hard_penalty += 100

        # =========================
        # SOFT CONSTRAINTS
        # =========================

        # 3. Timeslot imbalance
        avg = len(solution) / len(set(solution))
        for count in timeslot_count.values():
            soft_penalty += abs(count - avg)

        # 4. Room underutilization
        for exam_idx in range(len(solution)):
            room_idx = exam_idx % self.num_rooms
            unused_capacity = self.room_capacities[room_idx] - self.exam_students[exam_idx]
            soft_penalty += max(0, unused_capacity) * 0.1

        # =========================
        # FINAL FITNESS
        # =========================
        total_fitness = hard_penalty + soft_penalty
        return total_fitness
