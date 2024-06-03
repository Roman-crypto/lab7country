import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QToolBar, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QPushButton, QMessageBox

class CountryDialog(QDialog):
    def __init__(self, parent=None, country_data=None):
        super(CountryDialog, self).__init__(parent)
        self.setWindowTitle("Дані про нову країну" if country_data is None else "Редагувати країну")

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.capital_edit = QLineEdit()
        self.population_edit = QLineEdit()
        self.area_edit = QLineEdit()
        self.language_edit = QLineEdit()
        self.un_member_check = QCheckBox("Чи є країна членом ООН?")
        self.development_level_edit = QLineEdit()

        self.form_layout.addRow("Назва країни", self.name_edit)
        self.form_layout.addRow("Столиця", self.capital_edit)
        self.form_layout.addRow("Кількість населення", self.population_edit)
        self.form_layout.addRow("Площа країни, кв. км", self.area_edit)
        self.form_layout.addRow("Мова(-и) країни", self.language_edit)
        self.form_layout.addRow(self.un_member_check)
        self.form_layout.addRow("Рівень розвитку країни", self.development_level_edit)

        if country_data:
            self.name_edit.setText(country_data['name'])
            self.capital_edit.setText(country_data['capital'])
            self.population_edit.setText(country_data['population'])
            self.area_edit.setText(country_data['area'])
            self.language_edit.setText(country_data['language'])
            self.un_member_check.setChecked(country_data['un_member'])
            self.development_level_edit.setText(country_data['development_level'])

        self.layout.addLayout(self.form_layout)

        self.button_layout = QVBoxLayout()
        self.ok_button = QPushButton("Ок")
        self.cancel_button = QPushButton("Скасувати")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Інформація про країни")
        self.setGeometry(100, 100, 800, 400)

        self.create_menu()
        self.create_toolbar()
        self.create_table()

    def create_menu(self):
        self.menu = self.menuBar().addMenu("Файл")
        exit_action = QAction("Вихід", self)
        exit_action.triggered.connect(self.close)
        self.menu.addAction(exit_action)

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        add_action = QAction("Додати країну", self)
        add_action.triggered.connect(self.add_country)
        self.toolbar.addAction(add_action)

        edit_action = QAction("Змінити країну", self)
        edit_action.triggered.connect(self.edit_country)
        self.toolbar.addAction(edit_action)

        delete_action = QAction("Видалити країну", self)
        delete_action.triggered.connect(self.delete_country)
        self.toolbar.addAction(delete_action)

        clear_action = QAction("Очистити таблицю", self)
        clear_action.triggered.connect(self.clear_table)
        self.toolbar.addAction(clear_action)

    def create_table(self):
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["Назва країни", "Столиця", "Кількість населення", "Площа країни, кв. км", "Мова(-и) країни", "Член ООН", "Рівень розвитку"])
        self.setCentralWidget(self.table)

    def add_country(self):
        dialog = CountryDialog(self)
        if dialog.exec():
            country_data = {
                'name': dialog.name_edit.text(),
                'capital': dialog.capital_edit.text(),
                'population': dialog.population_edit.text(),
                'area': dialog.area_edit.text(),
                'language': dialog.language_edit.text(),
                'un_member': dialog.un_member_check.isChecked(),
                'development_level': dialog.development_level_edit.text()
            }

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(country_data['name']))
            self.table.setItem(row_position, 1, QTableWidgetItem(country_data['capital']))
            self.table.setItem(row_position, 2, QTableWidgetItem(country_data['population']))
            self.table.setItem(row_position, 3, QTableWidgetItem(country_data['area']))
            self.table.setItem(row_position, 4, QTableWidgetItem(country_data['language']))
            self.table.setItem(row_position, 5, QTableWidgetItem("Так" if country_data['un_member'] else "Ні"))
            self.table.setItem(row_position, 6, QTableWidgetItem(country_data['development_level']))

    def edit_country(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            country_data = {
                'name': self.table.item(selected_row, 0).text(),
                'capital': self.table.item(selected_row, 1).text(),
                'population': self.table.item(selected_row, 2).text(),
                'area': self.table.item(selected_row, 3).text(),
                'language': self.table.item(selected_row, 4).text(),
                'un_member': self.table.item(selected_row, 5).text() == "Так",
                'development_level': self.table.item(selected_row, 6).text()
            }

            dialog = CountryDialog(self, country_data)
            if dialog.exec():
                self.table.setItem(selected_row, 0, QTableWidgetItem(dialog.name_edit.text()))
                self.table.setItem(selected_row, 1, QTableWidgetItem(dialog.capital_edit.text()))
                self.table.setItem(selected_row, 2, QTableWidgetItem(dialog.population_edit.text()))
                self.table.setItem(selected_row, 3, QTableWidgetItem(dialog.area_edit.text()))
                self.table.setItem(selected_row, 4, QTableWidgetItem(dialog.language_edit.text()))
                self.table.setItem(selected_row, 5, QTableWidgetItem("Так" if dialog.un_member_check.isChecked() else "Ні"))
                self.table.setItem(selected_row, 6, QTableWidgetItem(dialog.development_level_edit.text()))
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, виберіть рядок для редагування.")

    def delete_country(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, виберіть рядок для видалення.")

    def clear_table(self):
        self.table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())



