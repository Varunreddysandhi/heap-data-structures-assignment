import csv

from priority_queue import PriorityQueue, Task


def simulate_scheduler(tasks):
    """Schedule available tasks by highest priority."""
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("Task IDs must be unique")

    for task in tasks:
        if task.arrival_time < 0:
            raise ValueError("Arrival times must be nonnegative")
        if task.duration <= 0:
            raise ValueError("Durations must be positive")

    pending = sorted(
        tasks,
        key=lambda task: (task.arrival_time, task.task_id),
    )

    queue = PriorityQueue()
    results = []
    current_time = 0
    next_task = 0

    while next_task < len(pending) or not queue.is_empty():
        # Jump to the next arrival when the processor is idle.
        if queue.is_empty() and next_task < len(pending):
            current_time = max(
                current_time,
                pending[next_task].arrival_time,
            )

        # Add every task that has arrived.
        while (
            next_task < len(pending)
            and pending[next_task].arrival_time <= current_time
        ):
            queue.insert(pending[next_task])
            next_task += 1

        task = queue.extract_max()

        start = current_time
        finish = start + task.duration
        waiting = start - task.arrival_time
        turnaround = finish - task.arrival_time
        lateness = max(0, finish - task.deadline)

        results.append({
            "Task": task.task_id,
            "Priority": task.priority,
            "Arrival": task.arrival_time,
            "Duration": task.duration,
            "Deadline": task.deadline,
            "Start": start,
            "Finish": finish,
            "Waiting": waiting,
            "Turnaround": turnaround,
            "Tardiness": lateness,
            "Met deadline": finish <= task.deadline,
        })

        current_time = finish

    return results


def main():
    tasks = [
        Task("T1", 2, 0, 4, 6),
        Task("T2", 5, 1, 3, 5),
        Task("T3", 3, 2, 2, 10),
        Task("T4", 4, 4, 1, 8),
        Task("T5", 1, 6, 2, 15),
    ]

    results = simulate_scheduler(tasks)

    print(
        f"{'Task':<6}{'Priority':<10}{'Start':<8}"
        f"{'Finish':<8}{'Wait':<8}{'Deadline met'}"
    )

    for row in results:
        print(
            f"{row['Task']:<6}"
            f"{row['Priority']:<10}"
            f"{row['Start']:<8}"
            f"{row['Finish']:<8}"
            f"{row['Waiting']:<8}"
            f"{row['Met deadline']}"
        )

    average_waiting = sum(
        row["Waiting"] for row in results
    ) / len(results)

    average_turnaround = sum(
        row["Turnaround"] for row in results
    ) / len(results)

    missed_deadlines = sum(
        not row["Met deadline"] for row in results
    )

    print(f"\nAverage waiting time: {average_waiting:.2f}")
    print(f"Average turnaround time: {average_turnaround:.2f}")
    print(f"Missed deadlines: {missed_deadlines}")

    with open(
        "scheduler_results.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    print("Results saved to scheduler_results.csv")


if __name__ == "__main__":
    main()