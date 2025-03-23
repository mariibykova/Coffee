import sqlite3
import sys
import io
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


f = 'coffee.sqlite'
con = sqlite3.connect(f)
cur = con.cursor()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.s = cur.execute('PRAGMA table_info("cof")')
        self.column_names = [i[1] for i in cur.fetchall()]
        self.result = cur.execute(f'''select * from cof''').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(self.column_names)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()

    def update_result(self):
        self.column_names = [i[1] for i in cur.fetchall()]
        self.result = cur.execute('''select * from cof''')
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(self.column_names)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
