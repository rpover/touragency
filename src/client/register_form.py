from PySide6.QtWidgets import QDialog, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QMessageBox
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from src.client.api.session import Session
from src.server.database.models import User


class RegisterWindow(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.__initUi()
        self.__settingUi()
        self.show()

    def __initUi(self) -> None:
        self.setWindowTitle('Register')
        self.setMinimumSize(370, 225)

        self.main_v_layout = QVBoxLayout()
        self.label_lineedit_h_layout = QHBoxLayout()
        self.label_v_layout = QVBoxLayout()
        self.line_edit_v_layout = QVBoxLayout()

        self.label_name = QLabel()
        self.label_surname = QLabel()
        self.label_phone = QLabel()
        self.label_password = QLabel()
        self.label_confirm = QLabel()

        self.spacer = QSpacerItem(0, 10)

        self.line_edit_name = QLineEdit()
        self.line_edit_surname = QLineEdit()
        self.line_edit_phone = QLineEdit()
        self.line_edit_password = QLineEdit()
        self.line_edit_confirm = QLineEdit()

        self.register_button = QPushButton()

    def __settingUi(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.addLayout(self.label_lineedit_h_layout)
        self.label_lineedit_h_layout.addLayout(self.label_v_layout)
        self.label_lineedit_h_layout.addLayout(self.line_edit_v_layout)

        self.label_v_layout.addWidget(self.label_name)
        self.label_v_layout.addWidget(self.label_surname)
        self.label_v_layout.addWidget(self.label_phone)
        self.label_v_layout.addSpacerItem(self.spacer)
        self.label_v_layout.addWidget(self.label_password)
        self.label_v_layout.addWidget(self.label_confirm)

        self.line_edit_v_layout.addWidget(self.line_edit_name)
        self.line_edit_v_layout.addWidget(self.line_edit_surname)
        self.line_edit_v_layout.addWidget(self.line_edit_phone)
        self.line_edit_v_layout.addSpacerItem(self.spacer)
        self.line_edit_v_layout.addWidget(self.line_edit_password)
        self.line_edit_v_layout.addWidget(self.line_edit_confirm)

        self.main_v_layout.addWidget(self.register_button)

        self.label_name.setText('Name')
        self.label_surname.setText('Surname')
        self.label_phone.setText('Phone')
        self.label_password.setText('Password')
        self.label_confirm.setText('Confirm')
        self.register_button.setText('Register')

        self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_edit_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button.clicked.connect(self.on_register_button_clicked)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return.numerator:
            self.register()

    def on_register_button_clicked(self) -> None:
        self.register()

    def data_is_valid(self) -> bool:
        if self.line_edit_password.text() != self.line_edit_confirm.text():
            self.parent().show_message(text="Incorrect confirm password", error=True, parent=self)
            return False

        for x in (self.line_edit_password, self.line_edit_surname, self.line_edit_phone, self.line_edit_name, self.line_edit_confirm):
            if x.text() == "":
                self.parent().show_message(text="One or more fields are empty", error=True, parent=self)
                return False

        return True

    def register(self) -> None:
        if not self.data_is_valid():
            return

        user = User(
            name=self.line_edit_name.text(),
            surname=self.line_edit_surname.text(),
            phone=self.line_edit_phone.text(),
            password=self.line_edit_password.text()
        )

        session = Session()
        session.register(user)

        if session.error:
            return self.parent().show_message(
                text=session.error,
                error=True,
                parent=self
            )

        if session.auth:
            self.parent().show_message(
                text='Successful register',
                error=False,
                parent=self
            )

        self.parent().open_login_dialog()
        self.close()
