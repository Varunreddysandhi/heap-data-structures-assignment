def sift_down(arr, heap_size, root):
    """Restore the max-heap property below root."""
    while True:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < heap_size and arr[left] > arr[largest]:
            largest = left

        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest == root:
            break

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest


def heapsort(arr):
    """Sort a list in ascending order, in place."""
    n = len(arr)

    # Build a max-heap from the bottom up.
    for root in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, root)

    # Move each maximum to its final position.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]

        # Restore the heap, excluding the sorted elements.
        sift_down(arr, end, 0)


if __name__ == "__main__":
    numbers = [12, 11, 13, 5, 6, 7]

    print("Before sorting:", numbers)
    heapsort(numbers)
    print("After sorting: ", numbers)