from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: str
    priority: int
    arrival_time: int
    duration: int
    deadline: int


class PriorityQueue:
    """Max-heap with O(log n) priority updates by task ID."""

    def __init__(self):
        self.heap = []
        self.positions = {}

    def is_empty(self):
        return len(self.heap) == 0

    def _higher_priority(self, first, second):
        """Break ties by earlier arrival, then task ID."""
        return (
            -first.priority,
            first.arrival_time,
            first.task_id,
        ) < (
            -second.priority,
            second.arrival_time,
            second.task_id,
        )

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        self.positions[self.heap[i].task_id] = i
        self.positions[self.heap[j].task_id] = j

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if not self._higher_priority(
                self.heap[index], self.heap[parent]
            ):
                break

            self._swap(index, parent)
            index = parent

    def _sift_down(self, index):
        size = len(self.heap)

        while True:
            best = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self._higher_priority(
                self.heap[left], self.heap[best]
            ):
                best = left

            if right < size and self._higher_priority(
                self.heap[right], self.heap[best]
            ):
                best = right

            if best == index:
                break

            self._swap(index, best)
            index = best

    def insert(self, task):
        if task.task_id in self.positions:
            raise ValueError("Task ID already exists")

        self.positions[task.task_id] = len(self.heap)
        self.heap.append(task)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        highest = self.heap[0]
        last = self.heap.pop()
        del self.positions[highest.task_id]

        if self.heap:
            self.heap[0] = last
            self.positions[last.task_id] = 0
            self._sift_down(0)

        return highest

    def change_priority(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(task_id)

        index = self.positions[task_id]
        old_task = self.heap[index]

        # Replace the immutable task with its updated version.
        self.heap[index] = Task(
            task_id=old_task.task_id,
            priority=new_priority,
            arrival_time=old_task.arrival_time,
            duration=old_task.duration,
            deadline=old_task.deadline,
        )

        if new_priority > old_task.priority:
            self._sift_up(index)
        elif new_priority < old_task.priority:
            self._sift_down(index)

    def increase_key(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(task_id)

        current = self.heap[self.positions[task_id]]

        if new_priority < current.priority:
            raise ValueError("New priority must not be lower")

        self.change_priority(task_id, new_priority)

    def decrease_key(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(task_id)

        current = self.heap[self.positions[task_id]]

        if new_priority > current.priority:
            raise ValueError("New priority must not be higher")

        self.change_priority(task_id, new_priority)


if __name__ == "__main__":
    queue = PriorityQueue()

    queue.insert(Task("T1", 2, 0, 3, 10))
    queue.insert(Task("T2", 5, 0, 2, 8))
    queue.insert(Task("T3", 1, 1, 4, 15))

    queue.increase_key("T3", 6)

    while not queue.is_empty():
        task = queue.extract_max()
        print(f"{task.task_id}: priority {task.priority}")