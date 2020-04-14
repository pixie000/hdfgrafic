from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtGui import QColor

# Класс модели таблицы
class TableModel(QAbstractTableModel):
    def __init__(self, array, parent=None):
        super(TableModel, self).__init__(parent)
        self.array = array

    # Ставим названия столбцов
    headers = 'random', '(col_1)^2', 'sum(col_2)', 'combobox'

    # Устанавливаем количество строк и столбцов из массива
    def rowCount(self, parent):
        return self.array.shape[0]

    def columnCount(self, parent):
        return self.array.shape[1]

    def data(self, index, role=None):
        col = index.column()
        row = index.row()
        # Устанавливаем значения в ячейках из массива
        if role == Qt.DisplayRole:
            return str(self.array[row, col])
        # Устанавливаем цвет в первом столбце в зависимости от знака числа
        if role == Qt.BackgroundColorRole and col==0:
            return QVariant(QColor(Qt.darkRed)) if self.array[row, col] < 0 else QVariant(QColor(Qt.darkGreen))
        return QVariant()

    # Устанавливаем значения заголовков таблицы
    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Horizontal:
                return self.headers[p_int]
            else:
                return p_int+1
    # Устанавливаем значения из таблицы в массив при изменении
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            col = index.column()
            row = index.row()
            self.array[row, col] = int(value)
        return True

    # Ставим флаги для элементов модели
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
