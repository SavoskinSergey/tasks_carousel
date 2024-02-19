
import pprint
import random

from collections import deque
from typing import Optional


class CircularIterator:
    def __init__(self, data, pattern=[1, 1, 1, 1]):
        self.data: list = data
        self.pattern: list = pattern
        self.counter = [0, 0, 0, 0]
        self.index = 1

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.index >= len(self.data) + 1:
            self.index = 1
        current = self.data[self.index - 1]
        self.counter[self.index - 1] += 1
        if self.counter[self.index - 1] == self.pattern[self.index - 1]:
            self.counter[self.index - 1] = 0
            self.index += 1

        return current


class Carousel():
    def __init__(self) -> None:
        self.items = {
            1 : deque(),
            2 : deque(),
            3 : deque(),
            4 : deque(),
        }
        self.history_slide = {
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
        }
        self.lap_counter = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
        }
        self.vision_count = 0
        self.viewed_count = 0
        self.current_lap = 1
        self.circular_list = CircularIterator([1, 2, 3, 4], pattern=[2, 2, 1, 1])

    def get_slide(self):
        if self.vision_count == self.viewed_count:
            return {
                'task': (
                    'id00000',
                    'Нет задач',
                    'Текущие задачи закончены, сбросьте статусы или заведите новую задачу',
                    0),
                'visible': 1,
                'viewed': 0
            }
        else:
            slide_task = self.get_task(self.current_lap)
            self.viewed_count += 1
            return slide_task

    def refresh(self):
        for i in self.lap_counter:
            self.lap_counter[i] = 1
        self.circular_list.index = 1
        self.viewed_count = 0
        self.history_slide = {
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
        }

    def get_task(self, current_lap) -> dict[str, Optional[tuple]]:
        # взводим механизм, получаем текущую ветку, переводим курсор на следующий элемент
        item = next(self.circular_list)
        if all(lap_number != current_lap for lap_number in self.lap_counter):
            print("Ни один элемент списка не равен", current_lap)
            self.current_lap += 1

        slide_task = ''
        while slide_task == '':
            while (len(self.items[item]) == 0 or self.lap_counter[item] != current_lap):
                item = next(self.circular_list)

            if self.history_slide[item] < len(self.items[item]):
                slide_task = self.items[item][self.history_slide[item]]
                self.history_slide[item] += 1
            elif len(self.items[item]) != 0:
                self.lap_counter[item] += 1
            else:
                self.lap_counter[item] += 1

        return slide_task

        # return [('blank task', 1), 0]


if __name__ == "__main__":
    v_data = [('task' + str(i), random.randint(1, 4)) for i in range(5)]
    car1 = Carousel()
    for item in v_data:
        if item:  # todo добавить проверку на актуальность
            car1.items[item[1]].append({'task': item, 'visible': 1, 'viewed': 0})
            car1.vision_count += 1

    # pprint.pprint(carousel)
    pprint.pprint(car1.items)

    while True:
        command = input().lower()
        match command:
            case 'n':
                print(car1.get_slide())

            case 'l':
                car1.refresh()
                print(car1.lap_counter)

            case 'i':
                pprint.pprint(car1.items)
                pprint.pprint(car1.history_slide)
                pprint.pprint([car1.viewed_count, 'from', car1.vision_count])

            case 'a':
                task, priority = input('"name" "priority"').split()
                car1.items[int(priority)].append((task, priority))
                car1.vision_count += 1
            case 'x':
                break
            case default:
                print('type again')

    print('Bye!')
