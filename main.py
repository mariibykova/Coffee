import sqlite3
from PyQt5 import QtWidgets, uic

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.load_coffee_data()

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        for row in rows:
            self.coffee_table.insertRow(self.coffee_table.rowCount())
            for i, value in enumerate(row):
                self.coffee_table.setItem(self.coffee_table.rowCount() - 1, i, QtWidgets.QTableWidgetItem(str(value)))
        conn.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
