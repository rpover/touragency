from PySide6 import QtWidgets, QtCore
import src.client.api.resolvers
from src.server.database.models import Tour


class TourEdit(QtWidgets.QDialog):
    tour_id: int = None
    countries = {str: int}

    def __init__(self, parent, tour_id: int) -> None:
        super().__init__(parent=parent)
        self.tour_id = tour_id
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
        self.update_button = QtWidgets.QPushButton()
        self.close_button = QtWidgets.QPushButton()
        self.spacer = QtWidgets.QWidget()

    def __settingUi(self) -> None:
        self.setWindowTitle(f'Edit {self.tour_id}-tour')
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.country_label, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.hours_label, 1, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.price_label, 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.country_combo_box, 2, 1, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.hours_line_edit, 2, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.price_line_edit, 2, 3, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.spacer, 3, 2, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.update_button, 4, 2, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.close_button, 4, 3, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.country_label.setText('Country')
        self.hours_label.setText('Hours')
        self.price_label.setText('Price')
        self.update_button.setText('Update')
        self.close_button.setText('Close')

        self.update_button.clicked.connect(self.on_update_clicK)
        self.close_button.clicked.connect(self.on_close_click)

        self.country_combo_box.insertItem(0, self.parent().country.text())
        self.price_line_edit.setText(self.parent().price.text())
        self.hours_line_edit.setText(self.parent().hours.text())

        for c in src.client.api.resolvers.get_all_countries():
            self.countries[c['name']] = c['id']

            if self.parent().country.text() == c['name']:
                continue

            self.country_combo_box.insertItem(self.country_combo_box.count(), c['name'])

        self.spacer.setFixedHeight(10)
        self.update_button.setFixedWidth(50)
        self.close_button.setFixedWidth(50)

    def data_validate(self) -> bool:
        return self.hours_line_edit.text() != '' or self.price_line_edit.text() != ''

    def on_update_clicK(self) -> None:
        if not self.data_validate():
            messagebox = QtWidgets.QMessageBox(self)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            messagebox.setWindowTitle("Error")
            messagebox.setText('One or more fields is empty')
            messagebox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            messagebox.show()

            QtWidgets.QMessageBox()

        tour = Tour(
            id=self.tour_id,
            country_id=self.countries[self.country_combo_box.currentText()],
            hours=self.hours_line_edit.text(),
            price=self.price_line_edit.text()
        )

        answer = src.client.api.resolvers.update_tour(tour)

        match answer:
            case {'error': error}:
                print(error)
                return

        self.parent().tour_updated()
        self.close()

    def on_close_click(self) -> None:
        self.close()
