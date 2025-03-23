import sys
import sqlite3
from PyQt5 import QtWidgets
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_AddEditCoffeeForm


class AddEditCoffeeForm(QtWidgets.QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        self.setupUi(self)
        self.coffee_id = coffee_id
        if self.coffee_id:
            self.load_coffee_data()

    def load_coffee_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        coffee_data = cursor.fetchone()
        conn.close()
        if coffee_data:
            self.nameInput.setText(coffee_data[1])
            self.roastLevelInput.setText(coffee_data[2])
            self.groundOrBeansInput.setCurrentText(coffee_data[3])
            self.tasteDescriptionInput.setText(coffee_data[4])
            self.priceInput.setText(str(coffee_data[5]))
            self.packageVolumeInput.setText(str(coffee_data[6]))

    def save_coffee_data(self):
        name = self.nameInput.text()
        roast_level = self.roastLevelInput.text()
        ground_or_beans = self.groundOrBeansInput.currentText()
        taste_description = self.tasteDescriptionInput.text()
        price = float(self.priceInput.text())
        package_volume = float(self.packageVolumeInput.text())

        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        if self.coffee_id:
            cursor.execute(
                "UPDATE coffee SET name=?, roast_level=?, ground_or_beans=?, taste_description=?, price=?, package_volume=? WHERE id=?",
                (name, roast_level, ground_or_beans, taste_description, price, package_volume, self.coffee_id)
            )
        else:
            cursor.execute(
                "INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast_level, ground_or_beans, taste_description, price, package_volume)
            )
        conn.commit()
        conn.close()
        self.accept()


class CoffeeApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        self.setupUi(self)
        self.load_coffee_data()
        self.addButton.clicked.connect(self.open_add_coffee_form)
        self.editButton.clicked.connect(self.open_edit_coffee_form)

    def load_coffee_data(self):
        self.coffee_table.setRowCount(0)
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        for row in rows:
            self.coffee_table.insertRow(self.coffee_table.rowCount())
            for i, value in enumerate(row):
                self.coffee_table.setItem(self.coffee_table.rowCount() - 1, i, QtWidgets.QTableWidgetItem(str(value)))
        conn.close()

    def open_add_coffee_form(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_coffee_data()

    def open_edit_coffee_form(self):
        selected_row = self.coffee_table.currentRow()
        if selected_row >= 0:
            coffee_id = int(self.coffee_table.item(selected_row, 0).text())
            dialog = AddEditCoffeeForm(self, coffee_id)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.load_coffee_data()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())