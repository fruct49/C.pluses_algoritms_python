import matplotlib.pyplot as plt
import numpy as np

# Ваши данные
sizes = np.array([10, 100, 1000, 10000, 100000, 200000, 300000, 400000, 500000])
radix = np.array([17, 128, 1540, 18750, 213400, 431200, 652100, 882300, 1105700]) / 1000  # в мс
merge = np.array([6, 52, 395, 4320, 52800, 112500, 171200, 231800, 293500]) / 1000
quick = np.array([3, 23, 162, 1850, 22300, 47800, 73400, 101200, 132100]) / 1000

# Создаем фигуру
plt.figure(figsize=(12, 7))

# Рисуем сплошные линии с повышенной детализацией
plt.plot(sizes, radix, '-', color='#1f77b4', label='Поразрядная', linewidth=3, alpha=0.8)
plt.plot(sizes, merge, '-', color='#ff7f0e', label='Слиянием', linewidth=3, alpha=0.8)
plt.plot(sizes, quick, '-', color='#2ca02c', label='Быстрая', linewidth=3, alpha=0.8)

# Добавляем маркеры
marker_size = 80
plt.scatter(sizes, radix, color='#1f77b4', s=marker_size, edgecolor='black', zorder=5)
plt.scatter(sizes, merge, color='#ff7f0e', s=marker_size, edgecolor='black', zorder=5)
plt.scatter(sizes, quick, color='#2ca02c', s=marker_size, edgecolor='black', zorder=5)

# Настройка осей
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Размер массива (элементы)', fontsize=14)
plt.ylabel('Время выполнения (мс)', fontsize=14)
plt.title('Сравнение алгоритмов сортировки', fontsize=16)

# Легенда и сетка
plt.legend(fontsize=12, framealpha=1)
plt.grid(True, which="both", ls="-", alpha=0.5)

# Подписи для ключевых точек
for i in [0, 3, 8]:  # Индексы 10, 10000, 500000 элементов
    plt.text(sizes[i], radix[i]*1.15, f'{radix[i]:.1f}', ha='center',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(sizes[i], merge[i]*1.15, f'{merge[i]:.1f}', ha='center',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    plt.text(sizes[i], quick[i]*1.15, f'{quick[i]:.1f}', ha='center',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('sorting_comparison.png', dpi=120, bbox_inches='tight')
plt.show()