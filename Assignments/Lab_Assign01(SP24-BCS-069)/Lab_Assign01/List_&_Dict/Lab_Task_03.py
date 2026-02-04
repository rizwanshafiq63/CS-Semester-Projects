# Task 3: finite-difference derivative of sin(x)
from math import sin, cos, pi

def forward_diff_sin(x, h):
    return (sin(x + h) - sin(x)) / h

def run(h=0.001, dx=0.001):
    xs = []
    x = -pi
    # build x from -pi to pi (inclusive) with increment dx
    while x <= pi + 1e-12:
        xs.append(x)
        x += dx

    approx = [forward_diff_sin(x, h) for x in xs]
    truth  = [cos(x) for x in xs]
    errors = [abs(a - t) for a, t in zip(approx, truth)]

    # Print a few sample rows
    print(f"\n=== Results with h = {h} (grid dx = {dx}) ===")
    print("   x\t\t approx d/dx sin(x)\t cos(x)\t\t abs error")
    for i in range(0, len(xs), max(1, len(xs)//8)):  # ~8 samples across the interval
        print(f"{xs[i]: .6f}\t {approx[i]: .8f}\t {truth[i]: .8f}\t {errors[i]: .2e}")

    print(f"\nMax abs error: {max(errors):.2e}")
    print(f"Mean abs error: {sum(errors)/len(errors):.2e}")

# Run the experiment for three h values
run(h=0.001)  
run(h=0.01)
run(h=0.1)
