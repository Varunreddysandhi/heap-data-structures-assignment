# Heap Data Structures Implementation and Analysis

Python implementations of Heapsort, a max-heap priority queue,
and a non-preemptive task scheduler.

## Project Overview

This project includes:

- In-place Heapsort using a max-heap.
- Randomized Quicksort and Merge Sort for comparison.
- Sorting benchmarks across multiple sizes and input distributions.
- A task priority queue supporting insertion, extraction, and priority changes.
- A scheduler simulation with waiting-time and deadline metrics.
- Correctness tests and a detailed analysis report.

## Project Files

| File | Purpose |
|---|---|
| `heapsort.py` | Heapsort implementation and demonstration |
| `sorting_algorithms.py` | Randomized Quicksort and Merge Sort |
| `priority_queue.py` | Task class and max-heap priority queue |
| `scheduler.py` | Non-preemptive priority scheduler |
| `benchmark.py` | Sorting performance experiments |
| `test_algorithms.py` | Sorting, priority queue, and scheduler tests |
| `results.csv` | Sorting benchmark measurements |
| `scheduler_results.csv` | Scheduler output |
| `report.md` | Design, complexity analysis, and results |
| `README.md` | Project overview and instructions |

## Requirements

- Python 3.7 or later.
- No external packages are required.

## Running the Project

Open a terminal in the project folder.

### Run Heapsort

```bash
py heapsort.py
```

### Run Quicksort and Merge Sort

```bash
py sorting_algorithms.py
```

### Run the Priority Queue Demonstration

```bash
py priority_queue.py
```

### Run All Tests

```bash
py test_algorithms.py
```

Expected output:

```text
heapsort: all 11 tests passed!
quicksort: all 11 tests passed!
merge_sort: all 11 tests passed!
All sorting tests passed!
All priority queue tests passed!
All scheduler tests passed!
```

### Run Sorting Benchmarks

```bash
py benchmark.py
```

Results are printed and saved to `results.csv`.

### Run the Scheduler

```bash
py scheduler.py
```

Results are printed and saved to `scheduler_results.csv`.

Running either experiment again replaces its previous output file.

On systems without the Windows `py` launcher, use `python` or
`python3` instead.

## Heapsort

Heapsort builds a max-heap using bottom-up construction. It then
repeatedly moves the maximum element to the end of the active heap
and restores heap order.

- Heap construction: Θ(n).
- Worst-case sorting time: Θ(n log n).
- Average time on random permutations of distinct keys: Θ(n log n).
- All-case upper bound: O(n log n).
- Auxiliary space: O(1).
- Stability: not stable.

Because this implementation stops sifting when heap order already
holds, an all-equal input takes Θ(n).

## Sorting Benchmark Method

The benchmark tests:

- Sizes: 100, 500, 1000, and 2000.
- Distributions: random, sorted, reverse-sorted, and repeated values.
- Five trials for each algorithm, size, and distribution.
- Median sorting time measured with `time.perf_counter()`.

Each algorithm receives a separate copy of the same trial input.
Input generation and copying are excluded from timing. Execution
order is shuffled, and correctness is checked after each run.

Input generation and execution-order shuffling use seed 42.
Quicksort's random pivots are not explicitly seeded.

## Sorting Findings

In the recorded experiment:

- Randomized Quicksort was fastest in 13 of 16 comparisons.
- Heapsort was fastest in the remaining three comparisons.
- Heapsort was faster than the tested Merge Sort implementation
  in all 16 comparisons, although some differences were small.
- At 2000 repeated-value elements, Quicksort was approximately
  5.53 times as fast as Heapsort and 6.66 times as fast as Merge Sort.

Quicksort's three-way partitioning is particularly effective for
repeated values because equal elements are excluded from further sorting.

These results describe the recorded implementations and machine.
Exact timings vary between runs.

## Priority Queue

The priority queue uses a list-based max-heap. Higher numeric
priorities run first.

Each immutable Task stores:

- Task ID.
- Priority.
- Arrival time.
- Duration.
- Deadline.

Equal priorities are resolved by earlier arrival time, then
lexicographically smaller task ID.

A dictionary tracks task positions and is updated after every swap.

### Operations

| Method | Behavior |
|---|---|
| `insert(task)` | Adds a task; rejects duplicate IDs |
| `extract_max()` | Removes and returns the highest-priority task |
| `increase_key(task_id, new_priority)` | Raises a task's priority |
| `decrease_key(task_id, new_priority)` | Lowers a task's priority |
| `change_priority(task_id, new_priority)` | Updates priority in either direction |
| `is_empty()` | Checks whether the queue is empty |

Empty extraction raises `IndexError`. Missing task IDs raise
`KeyError`. Invalid directional priority changes raise `ValueError`.

Heap insertion, extraction, and priority adjustment require at most
O(log n) heap levels. Dictionary operations are assumed to take
expected O(1) time. Python list allocation makes insertion's
O(log n) bound amortized.

The empty check takes O(1), and total queue space is O(n).

## Scheduler

The scheduler uses non-preemptive priority scheduling.

Only tasks that have arrived are eligible for selection.
Once selected, a task runs until completion. Deadlines are
evaluated but do not determine selection order.

For the supplied workload:

```text
Execution order: T1 → T2 → T4 → T3 → T5
Average waiting time: 3.20
Average turnaround time: 5.60
Missed deadlines: 1
```

T2 misses its deadline because it arrives while T1 is running
and cannot preempt it.

The simulation uses expected amortized O(n log n) time and O(n)
space under the priority queue's implementation assumptions.

## Report

See `report.md` for the implementation details, mathematical
analysis, full benchmark table, scheduling results, and limitations.