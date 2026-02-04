# AIC262 – Lab 02 – Graded Lab Task 2

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple, Union

# ---------- (i) Shape classes ----------

@dataclass(frozen=True)
class Trapezoid:
    a: float   # top base
    b: float   # bottom base
    h: float   # height

    def area(self) -> float:
        return 0.5 * (self.a + self.b) * self.h


@dataclass(frozen=True)
class Parallelogram:
    base: float
    height: float

    def area(self) -> float:
        return self.base * self.height


# ---------- (ii) Comparison class & utilities ----------

Shape = Union[Trapezoid, Parallelogram]

class AreaComparer:
    """
    Compare shapes by area, store results in a dictionary, iterate over
    different dimensions, and search for shapes with largest areas.
    """
    def __init__(self):
        # maps a readable shape key -> area
        self.results: Dict[str, float] = {}

    @staticmethod
    def _key(shape: Shape) -> str:
        if isinstance(shape, Trapezoid):
            return f"Trapezoid(a={shape.a}, b={shape.b}, h={shape.h})"
        elif isinstance(shape, Parallelogram):
            return f"Parallelogram(base={shape.base}, height={shape.height})"
        else:
            return f"Unknown({shape})"

    def add(self, shape: Shape) -> float:
        """Compute area and store in dictionary; returns area."""
        area = shape.area()
        self.results[self._key(shape)] = area
        return area

    def bulk_add(self, shapes: Iterable[Shape]) -> None:
        for shp in shapes:
            self.add(shp)

    def largest(self) -> Tuple[str, float]:
        """Return (key, area) for the single largest area across all shapes."""
        if not self.results:
            raise ValueError("No results available.")
        key = max(self.results, key=self.results.get)
        return key, self.results[key]

    def largest_per_type(self) -> Dict[str, Tuple[str, float]]:
        """Return largest result per shape type."""
        out: Dict[str, Tuple[str, float]] = {}
        # group keys by type name
        groups: Dict[str, List[str]] = {}
        for k in self.results:
            tname = "Trapezoid" if k.startswith("Trapezoid") else "Parallelogram"
            groups.setdefault(tname, []).append(k)
        for tname, keys in groups.items():
            best = max(keys, key=self.results.get)
            out[tname] = (best, self.results[best])
        return out

    def top_k(self, k: int = 3) -> List[Tuple[str, float]]:
        """Return the top-k shapes by area, descending."""
        return sorted(self.results.items(), key=lambda kv: kv[1], reverse=True)[:k]

    def find_greater_than(self, threshold: float) -> Dict[str, float]:
        """Dictionary 'filter': shapes with area >= threshold."""
        return {k: v for k, v in self.results.items() if v >= threshold}

    # for demonstration—uses dictionary functions
    def debug_print(self) -> None:
        print("\nStored results (dict):")
        for k, v in self.results.items():
            print(f"  {k} -> {v}")

        print("\nDictionary functions demo:")
        # keys(), values(), items(), get(), in
        print("  keys():", list(self.results.keys())[:3], "...")
        print("  values() sample:", list(self.results.values())[:3], "...")
        print("  items() sample:", list(self.results.items())[:2], "...")
        any_key = next(iter(self.results))
        print("  get(any_key):", self.results.get(any_key))
        print("  'nonexistent' in dict? ->", "nonexistent" in self.results)


def demo() -> None:
    # Iteration over different dimensions for both shapes
    trapezoids = [
        Trapezoid(a, b, h)
        for (a, b, h) in [(3, 5, 4), (10, 12, 7.5), (8, 6, 10), (20, 30, 15)]
    ]
    parallelograms = [
        Parallelogram(base, height)
        for (base, height) in [(6, 4), (12, 9), (10, 10), (25, 11)]
    ]

    comparer = AreaComparer()
    comparer.bulk_add(trapezoids + parallelograms)
    comparer.debug_print()

    # Largest overall
    best_key, best_area = comparer.largest()
    print(f"\nLargest overall: {best_key} with area = {best_area}")

    # Largest per type
    best_per_type = comparer.largest_per_type()
    print("\nLargest per type:")
    for tname, (k, v) in best_per_type.items():
        print(f"  {tname}: {k} -> {v}")

    # Top-3 shapes
    print("\nTop-3 shapes by area:")
    for rank, (k, v) in enumerate(comparer.top_k(3), start=1):
        print(f"  {rank}. {k} -> {v}")

    # Threshold search using dictionary 'filter'
    threshold = 120.0
    print(f"\nShapes with area >= {threshold}:")
    for k, v in comparer.find_greater_than(threshold).items():
        print(f"  {k} -> {v}")


if __name__ == "__main__":
    demo()
