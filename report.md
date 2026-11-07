# Heap Data Structures Implementation Analysis and Applications

## 1. Introduction

This project implements Heapsort and a binary-heap priority queue
in Python. It evaluates sorting performance and demonstrates
priority-based task scheduling.

Heapsort is compared experimentally with Randomized Quicksort
and Merge Sort. The priority queue supports task insertion,
maximum extraction, priority changes, and an empty check.

A scheduler simulation demonstrates how task priorities and
arrival times affect execution order, waiting time, turnaround
time, and deadline completion.

## 2. Heapsort Implementation

Heapsort is implemented in heapsort.py using a Python list.

For an element at index i, its children are located at:

- Left child: 2i + 1
- Right child: 2i + 2

A max-heap maintains the property that every parent is at least
as large as its children. Therefore, the largest element is
stored at index 0.

The algorithm first builds a max-heap from the bottom up.
It starts at the final internal node and applies sift_down
to each internal node in reverse order.

During sorting, the root is swapped with the final element
of the active heap. The active heap is reduced by one, and
sift_down restores the heap property.

This process continues until the list is sorted in ascending
order. The implementation uses iterative sifting and modifies
the supplied list in place.

## 3. Heapsort Complexity Analysis

### Building the Heap

A single sift_down operation takes O(h) time for a node of
height h.

Most nodes are near the leaves and require little work.
The number of nodes of height h is at most proportional to
n / 2^(h + 1).

The total construction work is therefore bounded by:

O(n Σ[h=0 to floor(log₂ n)] h / 2^(h + 1)) = O(n)

Because the series converges to a constant, bottom-up heap
construction takes Θ(n) time.

This is more efficient than building a heap through n
separate insertions, which has an O(n log n) upper bound.

### Extraction and Sorting

The sorting phase performs n - 1 root extractions.

Each extraction swaps the root with the end of the active
heap and restores heap order. Sifting takes at most
O(log n) time because a binary heap has logarithmic height.

Thus, the sorting phase takes at most O(n log n) time.

Combining both phases gives:

O(n) + O(n log n) = O(n log n)

### Worst Case

In unfavorable arrangements, repeated sifting traverses
a logarithmic number of levels.

Worst-case running time is Θ(n log n).

### Average Case

For uniformly random permutations of distinct keys,
standard Heapsort has average running time Θ(n log n).

Its balanced heap structure prevents the severely
unbalanced partitions that can occur in Quicksort.

### Best Case and the All-Case Upper Bound

Heapsort has an O(n log n) upper bound in the best,
average, and worst cases.

An upper bound does not imply that every input requires
Θ(n log n) work.

In this implementation, sift_down stops when the current
node is already at least as large as its children.
For an all-equal array, every sift_down stops immediately.

Heap construction then takes Θ(n), and the n - 1
extractions each require constant work. Consequently,
the best case over inputs allowing repeated values is
Θ(n).

This does not contradict the O(n log n) all-case bound:
linear time also satisfies that upper bound.

### Space Complexity and Overheads

The implementation sorts in place and uses a constant
number of index variables.

Because sift_down is iterative, no recursive call stack
is required. Auxiliary space complexity is O(1).

Heapsort is not stable: equal elements are not guaranteed
to retain their original relative order.

## 4. Comparison Algorithms

### Randomized Quicksort

The comparison implementation chooses a pivot uniformly
at random from the current subarray.

Three-way partitioning separates values into groups smaller
than, equal to, and greater than the pivot. Equal values
are excluded from further sorting.

Expected running time is O(n log n), with a worst-case
bound of O(n²). Duplicate-heavy inputs can require less
work. An all-equal array takes Θ(n).

An explicit stack stores pending subarray boundaries.
This implementation has an O(n) auxiliary-space upper
bound; it does not guarantee O(log n) stack space.

### Merge Sort

Merge Sort recursively divides the list into halves,
sorts both halves, and merges them using a shared buffer.

Its recurrence is:

T(n) = 2T(n / 2) + Θ(n)

This gives Θ(n log n) running time in the best, average,
and worst cases for this implementation, which always
performs the merges.

The buffer requires O(n) space. The recursive call stack
requires O(log n), so total auxiliary space is O(n).

The implementation is stable because equal values from
the left half are selected first.

## 5. Experimental Method

### Test Environment

- Operating system: [Enter your operating system]
- Processor: [Enter your processor]
- Python version: [Enter the output of py --version]

### Input Sizes

The sorting algorithms were tested with:

100, 500, 1000, and 2000 elements.

### Input Distributions

| Distribution | Description |
|---|---|
| Random | Random integers from 0 through n - 1 |
| Sorted | Distinct integers in ascending order |
| Reverse | Distinct integers in descending order |
| Repeated | Random integers from 0 through 9 |

The random distribution can contain duplicates. The
repeated distribution contains at most ten distinct values.

### Measurement Procedure

Each size and distribution was tested across five trials.
Every algorithm received a separate copy of the same
input in each trial.

Input generation and copying occurred outside the timed
interval. Running time was measured using
time.perf_counter().

Correctness was checked after timing by comparing the
result with Python's sorted() function.

Algorithm execution order was shuffled between trials.
The median time was recorded for each algorithm.

A local random generator seeded with 42 controlled input
generation and execution-order shuffling. Randomized
Quicksort's pivot generator was not explicitly seeded.

Results were saved to results.csv.

## 6. Sorting Results and Discussion

### Measured Results

All values are median running times in seconds, rounded
to seven decimal places. Lower values indicate faster
execution.

| Input type | Size | Heapsort | Quicksort | Merge Sort |
|---|---:|---:|---:|---:|
| Random | 100 | 0.0001089 | 0.0000948 | 0.0001304 |
| Random | 500 | 0.0007939 | 0.0006280 | 0.0010325 |
| Random | 1000 | 0.0018215 | 0.0013769 | 0.0020811 |
| Random | 2000 | 0.0050055 | 0.0032563 | 0.0051807 |
| Sorted | 100 | 0.0001123 | 0.0001036 | 0.0001161 |
| Sorted | 500 | 0.0007955 | 0.0006790 | 0.0008129 |
| Sorted | 1000 | 0.0021220 | 0.0021876 | 0.0023342 |
| Sorted | 2000 | 0.0043015 | 0.0035100 | 0.0043143 |
| Reverse | 100 | 0.0000940 | 0.0001057 | 0.0001170 |
| Reverse | 500 | 0.0007774 | 0.0007075 | 0.0008047 |
| Reverse | 1000 | 0.0016212 | 0.0017626 | 0.0021222 |
| Reverse | 2000 | 0.0043253 | 0.0038585 | 0.0043639 |
| Repeated | 100 | 0.0001024 | 0.0000335 | 0.0001270 |
| Repeated | 500 | 0.0006805 | 0.0001624 | 0.0008549 |
| Repeated | 1000 | 0.0017794 | 0.0003980 | 0.0025853 |
| Repeated | 2000 | 0.0046307 | 0.0008368 | 0.0055696 |

### Random Inputs

Quicksort was fastest at every tested size, followed by
Heapsort and then Merge Sort.

At 2000 elements, Quicksort took 0.0032563 seconds,
Heapsort took 0.0050055 seconds, and Merge Sort took
0.0051807 seconds.

Heapsort's time was approximately 1.54 times Quicksort's
time. Although both have O(n log n) expected or guaranteed
bounds as applicable, their constant factors differ.

### Sorted Inputs

Quicksort was fastest at sizes 100, 500, and 2000.
Heapsort was fastest at size 1000.

At 2000 elements, Heapsort and Merge Sort had very close
times: 0.0043015 and 0.0043143 seconds respectively.
Quicksort took 0.0035100 seconds.

Random pivot selection prevents ascending order from
systematically forcing an extreme pivot. Heapsort's
upper bound also remains O(n log n) on sorted input.

### Reverse-Sorted Inputs

Heapsort was fastest at sizes 100 and 1000. Quicksort
was fastest at sizes 500 and 2000.

At 2000 elements, Quicksort took 0.0038585 seconds,
compared with 0.0043253 seconds for Heapsort and
0.0043639 seconds for Merge Sort.

None of these implementations systematically suffers
the first-pivot Quicksort behavior on descending input:
the Quicksort implementation uses random pivots.

### Repeated-Value Inputs

Quicksort was substantially faster at every tested size.

At 2000 elements, its time was 0.0008368 seconds,
compared with 0.0046307 seconds for Heapsort and
0.0055696 seconds for Merge Sort.

Quicksort was approximately 5.53 times as fast as
Heapsort and 6.66 times as fast as Merge Sort.

Three-way partitioning processes all values equal to
the pivot together. Because these inputs contain at
most ten distinct values, it eliminates large groups
from further sorting.

These inputs are not all equal, so the linear all-equal
Heapsort best case does not directly describe them.

### Overall Interpretation

Quicksort was fastest in 13 of the 16 comparisons.
Heapsort was fastest in the remaining three comparisons.

Heapsort was faster than this Merge Sort implementation
in all 16 measurements. However, some differences were
small, so repeated experiments would be needed to judge
whether those small gaps are reliable.

All algorithms took more time as input size increased.
The measurements illustrate implementation-level
differences but do not independently prove asymptotic
complexity.

Random pivot choices, interpreter overhead, allocation,
background activity, and timing noise affect the results.
Five-trial medians reduce some variation but do not
eliminate it.

The conclusions apply to these implementations and
tested inputs, rather than every possible implementation
of these algorithms.

## 7. Priority Queue Design

### List-Based Binary Heap

The priority queue uses a Python list to represent a
complete binary tree.

For an element at index i:

- Parent: (i - 1) // 2
- Left child: 2i + 1
- Right child: 2i + 2

A list provides direct indexed access and avoids the
need for explicit tree-node pointers.

A max-heap is used because a larger priority number
represents a more urgent task.

### Task Representation

Each Task stores:

- Task ID.
- Priority.
- Arrival time.
- Duration.
- Deadline.

Tasks are immutable dataclass instances. Priority changes
replace the stored task with an updated instance.

This helps prevent accidental priority changes that
would bypass heap maintenance.

### Tie Breaking

Tasks are ordered by:

1. Higher priority.
2. Earlier arrival time.
3. Lexicographically smaller task ID.

This gives deterministic behavior when priorities tie.

### Position Dictionary

A dictionary maps task IDs to their current heap indices.

Every swap updates the dictionary. This allows priority
changes to locate a task without scanning the heap.

The complexity analysis assumes expected O(1) dictionary
operations and constant-cost task comparisons.

## 8. Priority Queue Operations and Complexity

### Insertion

Insertion appends the task and repeatedly compares it
with its parent. Swaps continue until heap order holds.

The task can move through O(log n) levels.

Heap maintenance takes O(log n) worst-case time.
Including Python list growth, insertion has amortized
O(log n) time under expected constant-time dictionary
operations. An individual list reallocation can cost O(n).

Duplicate task IDs are rejected.

### Extract Maximum

The root contains the highest-priority task.

Extraction removes the root, moves the last task to the
root, and sifts it downward until heap order is restored.

Heap maintenance takes O(log n) worst-case time under
the dictionary assumptions.

Extracting from an empty queue raises IndexError.

### Increase Key

The position dictionary locates the task. Its priority
is increased, and it moves upward as necessary.

Expected time is O(log n), accounting for expected
constant-time dictionary access.

A lower replacement priority is rejected by increase_key.

### Decrease Key

After decreasing a task's priority, the task moves
downward as necessary.

Expected time is O(log n) under the same assumptions.

A higher replacement priority is rejected by decrease_key.

### Change Priority

The general change_priority method chooses upward or
downward sifting according to the priority change.

Its expected time is O(log n).

A missing task ID raises KeyError.

### Empty Check

is_empty checks whether the heap list has length zero.
Its time complexity is O(1).

### Space Complexity

The heap and position dictionary each store O(n) entries.
Total priority queue space is O(n).

## 9. Scheduler Simulation

### Scheduling Policy

The scheduler uses non-preemptive priority scheduling.

At each selection point, all tasks that have arrived
are inserted into the priority queue. The highest-priority
available task is selected and runs until completion.

A higher-priority task arriving during execution does
not interrupt the running task.

If no task is ready, simulation time jumps to the next
arrival.

Deadlines are used to evaluate the schedule. They do
not determine selection order.

### Input Tasks

Times are expressed in arbitrary simulation units.

| Task | Priority | Arrival | Duration | Deadline |
|---|---:|---:|---:|---:|
| T1 | 2 | 0 | 4 | 6 |
| T2 | 5 | 1 | 3 | 5 |
| T3 | 3 | 2 | 2 | 10 |
| T4 | 4 | 4 | 1 | 8 |
| T5 | 1 | 6 | 2 | 15 |

### Scheduling Results

| Task | Start | Finish | Waiting | Turnaround | Tardiness | Deadline met |
|---|---:|---:|---:|---:|---:|---|
| T1 | 0 | 4 | 0 | 4 | 0 | Yes |
| T2 | 4 | 7 | 3 | 6 | 2 | No |
| T4 | 7 | 8 | 3 | 4 | 0 | Yes |
| T3 | 8 | 10 | 6 | 8 | 0 | Yes |
| T5 | 10 | 12 | 4 | 6 | 0 | Yes |

Execution order:

T1 → T2 → T4 → T3 → T5

The metrics are calculated as:

Waiting time = Start time - Arrival time

Turnaround time = Finish time - Arrival time

Tardiness = max(0, Finish time - Deadline)

A task meets its deadline if its finish time is less
than or equal to its deadline.

### Summary Metrics

Average waiting time:

(0 + 3 + 3 + 6 + 4) / 5 = 3.20

Average turnaround time:

(4 + 6 + 4 + 8 + 6) / 5 = 5.60

One task missed its deadline. Four out of five tasks,
or 80%, met their deadlines.

### Discussion

T1 starts first because it is the only available task
at time 0.

T2 arrives at time 1 with the highest priority, but
cannot interrupt T1. It starts at time 4 and finishes
at time 7, missing its deadline of 5 by two units.

After T2 finishes, T4 is selected ahead of T3 because
T4 has higher priority, despite arriving later.

T3 experiences the longest waiting time, six units.

This example shows that non-preemptive priority
scheduling does not guarantee deadline satisfaction.
Priority order and deadline order are different.

In a continuing workload, repeated high-priority
arrivals could also delay low-priority tasks for a
long time. Aging or a different scheduling policy
could address that issue, but neither is implemented.

### Scheduler Complexity

Sorting n tasks by arrival time takes O(n log n).

Each task is inserted and extracted once. These
operations take expected amortized O(log n) per task
under the priority queue's implementation assumptions.

Total simulation time is therefore expected amortized
O(n log n), and space usage is O(n).

The simulation jumps between events instead of looping
through every individual time unit.

## 10. Correctness Testing

Sorting tests compare all three sorting algorithms
against Python's sorted() on 11 inputs each.

Priority queue tests check:

- Empty-queue behavior.
- Insertion and extraction order.
- Duplicate task rejection.
- Priority increases and decreases.
- Tie breaking.
- Invalid updates and missing task IDs.
- Heap ordering after operations.
- Consistency of the position dictionary.
- A larger workload against a reference ordering.

Scheduler tests check:

- The expected execution order.
- Start and finish times.
- Waiting and turnaround times.
- Deadline completion and tardiness.
- Empty input.
- Initial idle time and gaps between tasks.
- Selection among simultaneously available tasks.
- Duplicate IDs and invalid task timing.

The tests can be run using:

py test_algorithms.py

## 11. Conclusion

Heapsort provides an O(n log n) running-time upper
bound for every input and uses O(1) auxiliary space
in this iterative implementation.

Its worst and average cases are Θ(n log n), while
all-equal input takes Θ(n) with the early-stopping
sift_down procedure.

In the experiments, Randomized Quicksort was fastest
in 13 of 16 comparisons. Its largest advantage occurred
on repeated-value inputs because three-way partitioning
processed equal values together.

Heapsort was faster than the tested Merge Sort
implementation in all measured comparisons, although
some differences were small.

The list-based priority queue supports efficient task
selection and priority updates. A position dictionary
avoids linear searches when locating tasks.

The scheduler produced an average waiting time of
3.20 units and an average turnaround time of 5.60 units.
One task missed its deadline, demonstrating a limitation
of non-preemptive priority scheduling.

