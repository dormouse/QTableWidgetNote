import logging

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication, QHBoxLayout,
                             QMainWindow,
                             QTableWidget, QTableWidgetItem,
                             QWidget)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout,
                             QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton,
                             QStyleFactory, QSpinBox, QTextEdit,
                             QVBoxLayout)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
                         QPixmap, QTransform)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')

__author__ = "Dormouse Young <dormouse.young@gmail.com>"
__status__ = "test"
__version__ = "0.1.1"
__create__ = "Jan 1 2017"
__modify__ = "Jan 7 2017"


class MyTable(QTableWidget):
    def __init__(self, *args):
        super(MyTable, self).__init__(*args)
        self.log = logging.getLogger(__name__)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)

        # setDropIndicatorShown not active under OSX
        self.setDropIndicatorShown(True)
        # so let's DIY
        self.oldItem = None
        self.oldColor = None

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, e):
        print("drag enter event")
        index = self.indexAt(e.pos())
        self.source_row = index.row()
        self.source_col = index.column()
        e.accept()

    def dropEvent(self, e):
        print("drop event")
        index = self.indexAt(e.pos())
        self.target_row = index.row()
        self.target_col = index.column()

        source_item = self.takeItem(self.source_row, self.source_col)
        target_item = self.takeItem(self.target_row, self.target_col)
        self.setItem(self.target_row, self.target_col, source_item)
        self.setItem(self.source_row, self.source_col, target_item)

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def dragLeaveEvent(self, e):
        print("drag leave")
        e.accept()

    def dragMoveEvent(self, e):
        index = self.indexAt(e.pos())
        newItem = self.horizontalHeaderItem(index.column())
        if self.oldItem:
            self.oldItem.setBackground(self.oldColor)
        if newItem:
            self.oldItem = newItem
            self.oldColor = newItem.background()
            newItem.setBackground(QColor(Qt.red))
        e.accept()


class ImageWidgetLabel(QLabel):
    def __init__(self, imagePath, parent=None):
        super(ImageWidgetLabel, self).__init__(parent)
        pic = QPixmap(imagePath)
        self.setPixmap(pic)


class ImageWidget(QWidget):
    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.log = logging.getLogger(__name__)
        self.createTableWidgets()
        self.createVGroupBox()
        self.InitTableData(self.tableUp)
        self.InitTableData(self.tableDown)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tableUp)
        mainLayout.addWidget(self.tableDown)
        mainLayout.addWidget(self.vGroupBox)
        self.setLayout(mainLayout)
        self.resize(800, 600)

    def createVGroupBox(self):
        self.vGroupBox = QGroupBox("Function Buttons")
        layout = QVBoxLayout()

        buttons = [
            dict(label="Set Header", func=self.setHeader),
            dict(label="Switch Header", func=self.switchHeader),
            dict(label="Show Image", func=self.showImage),
        ]

        for button in buttons:
            pushButton = QPushButton(button['label'])
            pushButton.clicked.connect(button['func'])
            layout.addWidget(pushButton)

        self.vGroupBox.setLayout(layout)

    def createTableWidgets(self):
        """ create QTableWidget
        There is two way to creat a QTableWidget:
        1. QTableWiget(rows, cols)
        2. table = QTableWidget()
           table.setRowCount(rows)
           table.setColumnCount(cols)
        """
        rows = 4
        cols = 5
        # Way one
        self.tableUp = MyTable(rows, cols)
        # Way tow
        self.tableDown = MyTable()
        self.tableDown.setRowCount(rows)
        self.tableDown.setColumnCount(cols)

    def InitTableData(self, table):
        data = [
            ["Jan", "Dormouse"],
            ["Feb", "Young"]
        ]
        for row_index, row_data in enumerate(data):
            for col_index, data in enumerate(row_data):
                table.setItem(row_index, col_index, QTableWidgetItem(data))

        table.item(1, 0).setBackground(QColor(125, 125, 125))
        print(type(table.item(1,0)))

    def changeCols(self):
        self.tableUp.setColumnCount(3)

    def setHeader(self):
        hHeader = ['Month', 'Name']
        vHeader = ['One', 'two', 'three']
        self.tableUp.setHorizontalHeaderLabels(hHeader)
        self.tableUp.setVerticalHeaderLabels(vHeader)

        self.tableUp.setHorizontalHeaderItem(2, QTableWidgetItem("Memo"))
        self.tableUp.setVerticalHeaderItem(3, QTableWidgetItem("The Fourth"))

        item1 = QTableWidgetItem('red')
        item1.setBackground(QColor(255, 0, 0))
        self.tableUp.setHorizontalHeaderItem(4, item1)

        memoHeaderItem = self.tableUp.horizontalHeaderItem(0)
        print(type(memoHeaderItem))
        print(memoHeaderItem.text())
        print(memoHeaderItem.background())
        print(memoHeaderItem.background().color().red())
        print(memoHeaderItem.background().color().green())
        print(memoHeaderItem.background().color().blue())
        memoHeaderItem.setBackground(QBrush(QColor(126,125,12)))
        print(memoHeaderItem.background().color().red())
        print(memoHeaderItem.background().color().green())
        print(memoHeaderItem.background().color().blue())

    def showImage(self):
        self.log.debug("show image")
        imagePath = 'images/hands.jpg'
        image = ImageWidget(imagePath, self)
        self.tableUp.setCellWidget(2, 3, image)

        label = ImageWidgetLabel(imagePath, self)
        self.tableUp.setCellWidget(2, 4, label)

    def switchHeader(self):
        view = self.tableUp.horizontalHeader()
        view.setVisible(not view.isVisible())

        view = self.tableUp.verticalHeader()
        view.setVisible(not view.isVisible())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # use "Fusion" style in OSX can show color header
    app.setStyle(QStyleFactory.create('Fusion'))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
