import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# 1. Загрузка данных
# ==============================
# Предполагается, что файл sanku.xlsx находится в текущей папке
# Первый столбец — размер матрицы, первая строка — число ядер
df = pd.read_excel('sanku.xlsx', sheet_name='Лист1', index_col=0)

print("Исходные данные (время выполнения, вероятно, в секундах):")
print(df, "\n")

# Размеры матриц и число ядер
sizes = df.index.values                # [200, 400, 800, 1600]
cores = df.columns.values.astype(int)  # [1, 2, 4, 8, 16]

# ==============================
# 2. График времени выполнения от размера матрицы
# ==============================
plt.figure(figsize=(10, 6))
for core in cores:
    plt.plot(sizes, df[core], marker='o', label=f'{core} ядер')
plt.xlabel('Размер матрицы')
plt.ylabel('Время выполнения (с)')
plt.title('Время выполнения в зависимости от размера матрицы и числа ядер')
plt.legend()
plt.grid(True)
plt.savefig('time_vs_size.png', dpi=300)
plt.show()

# ==============================
# 3. График времени выполнения от числа ядер
# ==============================
plt.figure(figsize=(10, 6))
for size in sizes:
    plt.plot(cores, df.loc[size], marker='s', label=f'Размер {size}')
plt.xlabel('Число ядер')
plt.ylabel('Время выполнения (с)')
plt.title('Время выполнения в зависимости от числа ядер')
plt.legend()
plt.grid(True)
plt.savefig('time_vs_cores.png', dpi=300)
plt.show()

# ==============================
# 4. Ускорение (Speedup) и его график
# ==============================
speedup = pd.DataFrame(index=sizes, columns=cores)
for size in sizes:
    t1 = df.loc[size, 1]  # время на 1 ядре
    for core in cores:
        speedup.loc[size, core] = t1 / df.loc[size, core]

print("Ускорение (Speedup = T1 / Tp):")
print(speedup, "\n")

plt.figure(figsize=(10, 6))
for size in sizes:
    plt.plot(cores, speedup.loc[size], marker='o', label=f'Размер {size}')
plt.plot(cores, cores, 'k--', label='Линейное ускорение (идеал)')
plt.xlabel('Число ядер')
plt.ylabel('Ускорение')
plt.title('Ускорение параллельных вычислений')
plt.legend()
plt.grid(True)
plt.savefig('speedup.png', dpi=300)
plt.show()

# ==============================
# 5. Эффективность (Efficiency) и её график
# ==============================
efficiency = speedup.div(cores, axis=1)
print("Эффективность (Efficiency = Speedup / p):")
print(efficiency, "\n")

plt.figure(figsize=(10, 6))
for size in sizes:
    plt.plot(cores, efficiency.loc[size], marker='o', label=f'Размер {size}')
plt.xlabel('Число ядер')
plt.ylabel('Эффективность')
plt.title('Эффективность параллельных вычислений')
plt.legend()
plt.grid(True)
plt.savefig('efficiency.png', dpi=300)
plt.show()

# ==============================
# 6. Логарифмический график времени (для наглядности)
# ==============================
plt.figure(figsize=(10, 6))
for core in cores:
    plt.loglog(sizes, df[core], marker='o', label=f'{core} ядер')
plt.xlabel('Размер матрицы (лог. шкала)')
plt.ylabel('Время выполнения (с) (лог. шкала)')
plt.title('Время выполнения в логарифмическом масштабе')
plt.legend()
plt.grid(True)
plt.savefig('time_loglog.png', dpi=300)
plt.show()
