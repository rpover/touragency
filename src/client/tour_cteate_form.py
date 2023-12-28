from PySide6 import QtWidgets, QtCore
import src.client.api.resolvers
from src.server.database.models import Tour


class TourCreate(QtWidgets.QDialog):
    countries = {str: int}

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.__initUi()
        self.__settingUi()
        self.show()

    def __initUi(self) -> None:
        self.main_layout = QtWidgets.QGridLayout()
        self.country_label = QtWidgets.QLabel()
        self.hours_label = QtWidgets.QLabel()
        self.price_label = QtWidgets.QLabel()
        self.country_combo_box = QtWidgets.QComboBox()
        self.hours_line_edit = QtWidgets.QLineEdit()
        self.price_line_edit = QtWidgets.QLineEdit()
        self.create_button = QtWidgets.QPushButton()
        self.close_button = QtWidgets.QPushButton()
        self.spacer = QtWidgets.QWidget()

    def __settingUi(self) -> None:
        self.setWindowTitle(f'Create tour')
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.country_label, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.hours_label, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.price_label, 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.country_combo_box, 2, 1, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.hours_line_edit, 2, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.price_line_edit, 2, 3, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.spacer, 3, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.create_button, 4, 2, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.close_button, 4, 3, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.country_label.setText('Country')
        self.hours_label.setText('Hours')
        self.price_label.setText('Price')
        self.create_button.setText('Create')
        self.close_button.setText('Close')

        self.create_button.clicked.connect(self.on_create_click)
        self.close_button.clicked.connect(self.on_close_click)

        for c in src.client.api.resolvers.get_all_countries():
            self.countries[c['name']] = c['id']

            self.country_combo_box.insertItem(self.country_combo_box.count(), c['name'])

        self.spacer.setFixedHeight(10)
        self.create_button.setFixedWidth(50)
        self.close_button.setFixedWidth(50)

    def data_validate(self) -> bool:
        return self.hours_line_edit.text() != '' or self.price_line_edit.text() != ''

    def on_create_click(self) -> None:
        if not self.data_validate():
            messagebox = QtWidgets.QMessageBox(self)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            messagebox.setWindowTitle("Error")
            messagebox.setText('One or more fields is empty')
            messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            messagebox.show()

            QtWidgets.QMessageBox()

        tour = Tour(
            country_id=self.countries[self.country_combo_box.currentText()],
            hours=self.hours_line_edit.text(),
            price=self.price_line_edit.text()
        )

        answer = src.client.api.resolvers.create_tour(tour)

        match answer:
            case {'error': error}:
                print(error)
                return

        self.parent().add_tour(
            tour_id=str(answer['id']),
            country=self.country_combo_box.currentText(),
            hours=str(answer['hours']),
            price=str(answer['price'])
            )

        self.close()

    def on_close_click(self) -> None:
        self.close()
