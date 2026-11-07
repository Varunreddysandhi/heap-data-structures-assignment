import random


def quicksort(arr):
    """Sort in place using random pivots and three-way partitioning."""
    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        if low >= high:
            continue

        pivot = arr[random.randint(low, high)]

        lt = low
        i = low
        gt = high

        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1

        stack.append((low, lt - 1))
        stack.append((gt + 1, high))


def merge_sort(arr):
    """Sort in place using an auxiliary merge buffer."""
    buffer = [None] * len(arr)

    def sort_section(low, high):
        # The section includes low but excludes high.
        if high - low <= 1:
            return

        mid = (low + high) // 2

        sort_section(low, mid)
        sort_section(mid, high)

        i = low
        j = mid
        k = low

        while i < mid and j < high:
            if arr[i] <= arr[j]:
                buffer[k] = arr[i]
                i += 1
            else:
                buffer[k] = arr[j]
                j += 1

            k += 1

        while i < mid:
            buffer[k] = arr[i]
            i += 1
            k += 1

        while j < high:
            buffer[k] = arr[j]
            j += 1
            k += 1

        for k in range(low, high):
            arr[k] = buffer[k]

    sort_section(0, len(arr))


if __name__ == "__main__":
    original = [12, 11, 13, 5, 6, 7]

    quicksort_data = original.copy()
    merge_sort_data = original.copy()

    quicksort(quicksort_data)
    merge_sort(merge_sort_data)

    print("Original:  ", original)
    print("Quicksort: ", quicksort_data)
    print("Merge Sort:", merge_sort_data)