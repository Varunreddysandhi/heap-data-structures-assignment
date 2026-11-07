import csv
import random
import statistics
from time import perf_counter

from heapsort import heapsort
from sorting_algorithms import quicksort, merge_sort


def run_benchmarks():
    sizes = [100, 500, 1000, 2000]
    repetitions = 5
    rng = random.Random(42)

    algorithms = [
        ("Heapsort", heapsort),
        ("Quicksort", quicksort),
        ("Merge Sort", merge_sort),
    ]

    results = []

    for size in sizes:
        for input_type in ["Random", "Sorted", "Reverse", "Repeated"]:
            timings = {name: [] for name, _ in algorithms}

            for trial in range(repetitions):
                if input_type == "Random":
                    original = [
                        rng.randrange(size) for _ in range(size)
                    ]
                elif input_type == "Sorted":
                    original = list(range(size))
                elif input_type == "Reverse":
                    original = list(range(size, 0, -1))
                else:
                    original = [
                        rng.randrange(10) for _ in range(size)
                    ]

                expected = sorted(original)

                # Shuffle execution order to reduce ordering bias.
                order = algorithms.copy()
                rng.shuffle(order)

                for name, algorithm in order:
                    data = original.copy()

                    start = perf_counter()
                    algorithm(data)
                    elapsed = perf_counter() - start

                    assert data == expected, (
                        f"{name} failed on {input_type}, size {size}"
                    )

                    timings[name].append(elapsed)

            medians = {
                name: statistics.median(timings[name])
                for name, _ in algorithms
            }

            results.append([
                input_type,
                size,
                medians["Heapsort"],
                medians["Quicksort"],
                medians["Merge Sort"],
            ])

            print(
                f"{input_type:<10} n={size:<5} "
                f"Heap={medians['Heapsort']:.7f}s  "
                f"Quick={medians['Quicksort']:.7f}s  "
                f"Merge={medians['Merge Sort']:.7f}s"
            )

    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Input type",
            "Size",
            "Heapsort median seconds",
            "Quicksort median seconds",
            "Merge Sort median seconds",
        ])

        writer.writerows(results)

    print("\nResults saved to results.csv")


if __name__ == "__main__":
    run_benchmarks()