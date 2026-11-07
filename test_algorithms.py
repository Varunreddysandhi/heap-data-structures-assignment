import random

from heapsort import heapsort
from sorting_algorithms import quicksort, merge_sort
from priority_queue import PriorityQueue, Task
from scheduler import simulate_scheduler


def test_sorting():
    test_cases = [
        [],                         # Empty list
        [5],                        # One element
        [2, 1],                     # Two elements
        [1, 2, 3, 4, 5],           # Already sorted
        [5, 4, 3, 2, 1],           # Reverse sorted
        [3, 3, 3, 3],              # All equal
        [4, 2, 4, 1, 2],           # Repeated values
        [-3, 0, 5, -1],            # Negative numbers
    ]

    rng = random.Random(42)

    for size in [10, 100, 1000]:
        test_cases.append(
            [rng.randint(-100, 100) for _ in range(size)]
        )

    algorithms = [
        heapsort,
        quicksort,
        merge_sort,
    ]

    for algorithm in algorithms:
        for case_number, original in enumerate(test_cases, start=1):
            actual = original.copy()
            expected = sorted(original)

            algorithm(actual)

            assert actual == expected, (
                f"{algorithm.__name__} failed test {case_number}"
            )

        print(
            f"{algorithm.__name__}: "
            f"all {len(test_cases)} tests passed!"
        )

    print("All sorting tests passed!")


def check_heap(queue):
    assert len(queue.heap) == len(queue.positions)

    for index, task in enumerate(queue.heap):
        assert queue.positions[task.task_id] == index

        if index > 0:
            parent = (index - 1) // 2

            assert not queue._higher_priority(
                task, queue.heap[parent]
            ), "Heap property violated"


def expect_error(error_type, operation):
    try:
        operation()
    except error_type:
        return

    raise AssertionError(f"Expected {error_type.__name__}")


def test_priority_queue():
    queue = PriorityQueue()

    # An empty queue must be detected.
    assert queue.is_empty()
    expect_error(IndexError, queue.extract_max)

    # Insert tasks and check the heap after each insertion.
    tasks = [
        Task("T1", 2, 0, 3, 10),
        Task("T2", 5, 0, 2, 8),
        Task("T3", 1, 1, 4, 15),
    ]

    for task in tasks:
        queue.insert(task)
        check_heap(queue)

    assert not queue.is_empty()

    # Duplicate IDs must be rejected.
    expect_error(ValueError, lambda: queue.insert(tasks[0]))

    # Increasing priority must move a task upward.
    queue.increase_key("T3", 6)
    check_heap(queue)

    assert queue.extract_max().task_id == "T3"
    check_heap(queue)

    # Decreasing priority must move a task downward.
    queue.decrease_key("T2", 0)
    check_heap(queue)

    assert queue.extract_max().task_id == "T1"
    check_heap(queue)

    assert queue.extract_max().task_id == "T2"
    assert queue.is_empty()
    check_heap(queue)

    # Equal priorities: earlier arrival, then task ID.
    tie_queue = PriorityQueue()

    for task in [
        Task("B", 4, 0, 1, 10),
        Task("C", 4, 1, 1, 10),
        Task("A", 4, 0, 1, 10),
    ]:
        tie_queue.insert(task)

    for expected_id in ["A", "B", "C"]:
        assert tie_queue.extract_max().task_id == expected_id
        check_heap(tie_queue)

    # Invalid priority changes must be rejected.
    error_queue = PriorityQueue()
    error_queue.insert(Task("X", 5, 0, 1, 10))

    expect_error(
        ValueError,
        lambda: error_queue.increase_key("X", 4),
    )
    expect_error(
        ValueError,
        lambda: error_queue.decrease_key("X", 6),
    )
    expect_error(
        KeyError,
        lambda: error_queue.change_priority("missing", 10),
    )

    # Compare a larger workload against a reference ordering.
    rng = random.Random(123)
    large_queue = PriorityQueue()
    reference = {}

    for number in range(100):
        task = Task(
            task_id=f"T{number:03d}",
            priority=rng.randint(0, 20),
            arrival_time=rng.randint(0, 10),
            duration=1,
            deadline=100,
        )

        large_queue.insert(task)
        reference[task.task_id] = task
        check_heap(large_queue)

    for number in range(0, 100, 3):
        task_id = f"T{number:03d}"
        old = reference[task_id]
        new_priority = rng.randint(0, 20)

        large_queue.change_priority(task_id, new_priority)

        reference[task_id] = Task(
            old.task_id,
            new_priority,
            old.arrival_time,
            old.duration,
            old.deadline,
        )

        check_heap(large_queue)

    expected_order = sorted(
        reference.values(),
        key=lambda task: (
            -task.priority,
            task.arrival_time,
            task.task_id,
        ),
    )

    for expected_task in expected_order:
        assert large_queue.extract_max() == expected_task
        check_heap(large_queue)

    assert large_queue.is_empty()

    print("All priority queue tests passed!") 

def test_scheduler():
    tasks = [
        Task("T1", 2, 0, 4, 6),
        Task("T2", 5, 1, 3, 5),
        Task("T3", 3, 2, 2, 10),
        Task("T4", 4, 4, 1, 8),
        Task("T5", 1, 6, 2, 15),
    ]

    results = simulate_scheduler(tasks)

    # Verify selection order and non-preemptive execution.
    assert [row["Task"] for row in results] == [
        "T1", "T2", "T4", "T3", "T5"
    ]

    assert [row["Start"] for row in results] == [
        0, 4, 7, 8, 10
    ]

    assert [row["Finish"] for row in results] == [
        4, 7, 8, 10, 12
    ]

    # Check waiting times and turnaround times.
    assert [row["Waiting"] for row in results] == [
        0, 3, 3, 6, 4
    ]

    assert [row["Turnaround"] for row in results] == [
        4, 6, 4, 8, 6
    ]

    assert sum(row["Waiting"] for row in results) == 16
    assert sum(row["Turnaround"] for row in results) == 28

    # Finishing exactly at a deadline counts as meeting it.
    assert [row["Met deadline"] for row in results] == [
        True, False, True, True, True
    ]

    assert [row["Tardiness"] for row in results] == [
        0, 2, 0, 0, 0
    ]

    # Empty input should produce an empty schedule.
    assert simulate_scheduler([]) == []

    # Check initial idle time and a gap between tasks.
    idle_results = simulate_scheduler([
        Task("A", 1, 3, 2, 5),
        Task("B", 2, 10, 1, 11),
    ])

    assert [row["Start"] for row in idle_results] == [3, 10]
    assert [row["Finish"] for row in idle_results] == [5, 11]
    assert all(row["Waiting"] == 0 for row in idle_results)

    # Higher priority runs first when both tasks are available.
    priority_results = simulate_scheduler([
        Task("Low", 1, 0, 1, 10),
        Task("High", 5, 0, 1, 10),
    ])

    assert [row["Task"] for row in priority_results] == [
        "High", "Low"
    ]

    # Invalid inputs must be rejected.
    expect_error(
        ValueError,
        lambda: simulate_scheduler([
            Task("A", 1, 0, 1, 10),
            Task("A", 2, 0, 1, 10),
        ]),
    )

    expect_error(
        ValueError,
        lambda: simulate_scheduler([
            Task("A", 1, -1, 1, 10),
        ]),
    )

    expect_error(
        ValueError,
        lambda: simulate_scheduler([
            Task("A", 1, 0, 0, 10),
        ]),
    )

    print("All scheduler tests passed!")


if __name__ == "__main__":
    test_sorting()
    test_priority_queue()
    test_scheduler()