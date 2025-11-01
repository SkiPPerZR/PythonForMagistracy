import threading
import time

def squares():
    for i in range(1, 11):
        print(f"Квадрат {i} = {i ** 2}")
        time.sleep(0.3)

def cubes():
    for i in range(1, 11):
        print(f"Куб {i} = {i ** 3}")
        time.sleep(0.3)

t1 = threading.Thread(target=squares)
t2 = threading.Thread(target=cubes)

t1.start()
t2.start()

t1.join()
t2.join()

print("\n=== Задание 2 ===\n")

def print_numbers(name: str):
    for i in range(1, 11):
        print(f"{name} выводит число {i}")
        time.sleep(1)

threads = []
for n in range(3):
    t = threading.Thread(target=print_numbers, args=(f"Поток-{n+1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nВсе потоки завершены.")