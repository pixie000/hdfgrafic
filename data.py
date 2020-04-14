import numpy as np

# Класс для работы с данными
class Data(object):

    def __init__(self, data):
        self.data = data

    def calcData(self):
        # Пересчитываем данные во 2 и 3 столбце как значение в квадрате и накопление
        self.data[:, 1] = self.data[:, 0]**2
        self.data[:, 2] += self.data[:, 1]

        # Пересчитываем случайные значения в 1 столбце
    def randomize(self):
        self.data[:, 0] = np.random.randint(-10, 11, 8)
        self.calcData()

        # Возвращаем данные в main
    def get_data(self):
            return self.data
            
