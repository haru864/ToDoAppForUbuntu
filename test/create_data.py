import csv
import random
import os


current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
csv_file_path = current_directory + "/" + "test_data.csv"

num_rows = 1000
column_list = [
    "id",
    "task_name",
    "task_type",
    "difficulty_level",
    "is_completed",
    "estimated_time_seconds",
    "remaining_time_seconds",
    "total_elapsed_time_seconds",
]

"""
タスクA 難易度が上がるに連れて、見積もりよりも時間がかかる
タスクB 難易度が上がるに連れて、見積もりよりも時間がかからない
タスクC 難易度とかかった時間に相関関係がない
"""
with open(csv_file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(column_list)
    for i in range(num_rows):
        id = i + 1
        task_name = "task_" + str(id).zfill(4)
        task_type = random.choice(["A", "B", "C"])
        difficulty_level = random.randint(1, 5)
        is_completed = 1
        estimated_time_seconds = random.randint(30, 100)
        remaining_time_seconds = 0
        if task_type == "A":
            total_elapsed_time_seconds = random.randint(
                estimated_time_seconds + 1, estimated_time_seconds * 2
            )
        elif task_type == "B":
            total_elapsed_time_seconds = random.randint(1, estimated_time_seconds - 1)
        elif task_type == "C":
            total_elapsed_time_seconds = random.randint(1, estimated_time_seconds * 2)
        else:
            total_elapsed_time_seconds = -1
        writer.writerow(
            [
                id,
                task_name,
                task_type,
                difficulty_level,
                is_completed,
                estimated_time_seconds,
                remaining_time_seconds,
                total_elapsed_time_seconds,
            ]
        )
