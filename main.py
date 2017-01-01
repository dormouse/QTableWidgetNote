import logging

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication, QMainWindow,
                             QTableWidget, QTableWidgetItem)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')


class MyTable(QTableWidget):
    def __init__(self, *args):
        super(MyTable, self).__init__(*args)
        self.log = logging.getLogger(__name__)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

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
        e.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createActions()
        self.createMenus()

        self.tw = MyTable(4, 6)
        self.addData()

        self.resize(800, 200)
        self.setCentralWidget(self.tw)

    def createActions(self):
        self.changeColsAct = QAction("改变列数", self, triggered=self.changeCols)
        self.setHeaderAct = QAction("设置表头", self, triggered=self.setHeader)
        self.switchHeaderAct = QAction("开关表头", self, triggered=self.switchHeader)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.setHeaderAct)
        self.editMenu.addAction(self.switchHeaderAct)
        self.editMenu.addAction(self.changeColsAct)

    def addData(self):
        data = [
            ["Jan", "Dormouse"],
            ["Feb", "Young"]
        ]
        for row_index, row_data in enumerate(data):
            for col_index, data in enumerate(row_data):
                self.tw.setItem(row_index, col_index, QTableWidgetItem(data))

    def changeCols(self):
        self.tw.setColumnCount(3)

    def setHeader(self):
        hHeader = ['月份', '姓名']
        vHeader = ['一', '二', '三']
        self.tw.setHorizontalHeaderLabels(hHeader)
        self.tw.setVerticalHeaderLabels(vHeader)

        self.tw.setHorizontalHeaderItem(2, QTableWidgetItem("备注"))
        self.tw.setVerticalHeaderItem(3, QTableWidgetItem("第四"))

    def switchHeader(self):
        view = self.tw.horizontalHeader()
        view.setVisible(not view.isVisible())

        view = self.tw.verticalHeader()
        view.setVisible(not view.isVisible())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
