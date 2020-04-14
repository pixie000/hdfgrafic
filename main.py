import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QApplication, QTableView, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from TableModel import TableModel
from delegate import Delegate
from data import Data
import numpy as np
import h5py

# Создаем начальные значения массива
data = np.random.randint(-10, 11, (8, 4))
data[:, 1:4] = 0

class Main(QWidget):
    def __init__(self):
        super().__init__()

        # Устанаваливаем свойства окна
        self.setGeometry(500, 100, 600, 750)
        self.setWindowTitle('Task 2')
        # Создаем экземпляр делегата
        self.combobox = Delegate()
        # Создаем кнопки
        self.randomButton = QPushButton('Random')
        self.saveButton = QPushButton('Save')
        self.loadButton = QPushButton('Load')
        # Передаем данные в экземпляр для обработки данных
        self.back = Data(data)
        # Пересчитываем данные во 2, 3 столбцах
        self.back.calcData()
        # Получаем данные
        self.backData = self.back.get_data()
        # Создаем экземпляр модели
        self.model = TableModel(self.backData)
        # Создаем виджет таблицы и подключаем модель
        self.view = QTableView(self)
        self.view.setModel(self.model)
        # Устанавливаем делегат на 4 столбец
        self.view.setItemDelegateForColumn(3, self.combobox)
        # Устанавливаем минимальную ширину столбцов
        self.view.horizontalHeader().setMinimumSectionSize(137)
        # Создаем виджет графика
        self.plot = pg.PlotWidget()
        self.plot.setBackground('w')
        # Создаем вертикальный и горизонтальный контейнеры и распологаем виджеты
        self.layout = QVBoxLayout(self)
        self.layoutHor = QHBoxLayout(self)
        self.layout.addLayout(self.layoutHor)
        self.layoutHor.addWidget(self.randomButton)
        self.layoutHor.addWidget(self.saveButton)
        self.layoutHor.addWidget(self.loadButton)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.plot)
        self.show()
        # Устанавливаем сигналы на кнопки и изменение данных в таблице
        self.model.dataChanged.connect(self.back.calcData)
        self.saveButton.clicked.connect(self.save)
        self.loadButton.clicked.connect(self.load)
        self.randomButton.clicked.connect(self.back.randomize)
        self.view.horizontalHeader().sectionClicked.connect(self.graphic)

    def graphic(self):
        # Берем индексы выделенных столбцов
        selected = self.view.selectionModel().selectedColumns(0)
        # Рисуем график, если столбца два
        if len(selected) == 2:
            self.plot.plotItem.clear()
            self.plot.showGrid(x=True, y=True)
            x = self.backData[:, selected[0].column()]
            y = self.backData[:, selected[1].column()]
            self.plot.plot(x, y, pen='b', symbol='x' )

    def save(self):
        # Сохраняем файл в формат hdf5
        with h5py.File('Test.hdf5', 'w') as file:
            file.create_dataset('Test', data=self.backData)

    def load(self):
        # Берем данные из файла
        with h5py.File('Test.hdf5', 'r') as file:
            hdfdata = file['Test'][:]
        self.backData = hdfdata

        # Переопределяем данные в ячейках таблицы
        for row in range(self.backData.shape[0]):
            for col in range(self.backData.shape[1]):
                self.model.setData(self.model.index(row, col), self.backData[row, col], role=Qt.EditRole)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
