import random
import pandas as pd
import matplotlib.pyplot as plt

def triangle(x, y):
    return -x <= y <= x

def monte(x_min, x_max, y_min, y_max, num_points):
    points_inside = 0

    for _ in range(num_points):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)

        if triangle(x, y):
            points_inside += 1

    rectangle_area = (x_max - x_min) * (y_max - y_min)
    return (points_inside / num_points) * rectangle_area

x_min, x_max = 3, 6
y_min, y_max = -6, 6

n_values = [100, 500, 1000, 5000, 10000, 50000, 100000]
results = []

for n in n_values:
    area = monte(x_min, x_max, y_min, y_max, num_points=n)
    results.append((n, area))

df = pd.DataFrame(results, columns=["N", "Приближенная площадь"])
print(df)

plt.plot(df["N"], df["Приближенная площадь"], marker='o')
plt.xscale("log")
plt.xlabel("Количество испытаний (N)")
plt.ylabel("Приближенная площадь")
plt.title("Зависимость площади от количества испытаний")
plt.grid(True)
plt.show()
