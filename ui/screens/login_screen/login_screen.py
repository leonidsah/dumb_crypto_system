from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

import logic.values
from logic import values
from logic.account_management import verify_user


class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        welcome_ql = QLabel("Вход в систему 'КриптоКролик'")
        welcome_ql.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_qle = QLineEdit(self)
        self.login_qle.setPlaceholderText("Логин")
        self.login_qle.setText("user")
        self.password_qle = QLineEdit(self)
        self.password_qle.setEchoMode(QLineEdit.Password)
        self.password_qle.setPlaceholderText("Пароль")
        self.password_qle.setText("password")
        self.check_qpb = QPushButton("Войти", self)
        self.check_qpb.clicked.connect(self.authenticate_user)

        layout.addWidget(welcome_ql)
        layout.addWidget(self.login_qle)
        layout.addWidget(self.password_qle)
        layout.addWidget(self.check_qpb)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def authenticate_user(self):
        username = self.login_qle.text()
        password = self.password_qle.text()

        if verify_user(username, password):
            logic.values.username = username
            self.parentWidget().setCurrentIndex(1)  # Переход на экран аутентификации
        else:
            self.login_qle.setStyleSheet("border: 1px solid red")
            self.password_qle.setStyleSheet("border: 1px solid red")
