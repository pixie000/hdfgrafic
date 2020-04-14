from PyQt5.QtWidgets import QItemDelegate, QComboBox
from PyQt5.QtCore import Qt

# Класс для создания делегата combobox
class Delegate(QItemDelegate):
    def __init__(self):
        super(Delegate, self).__init__()

    def createEditor(self, parent, option, index):
        # Создаем экземпляр combobox
        cmb = QComboBox(parent)
        # Ставим числа в выпадающий список
        cmb.addItems(['1', '2', '3', '4', '5'])
        return cmb

    def setEditorData(self, editor, index):
        # Устанавлливаем значения из модели
        editor.setCurrentIndex(int(index.data(Qt.DisplayRole)))

        # Устанавливаем значения в модель
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)
