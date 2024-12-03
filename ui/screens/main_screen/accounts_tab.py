from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout

import logic.mfa.totp
from logic import account_management


class AccountsTab(QWidget):
    def __init__(self):
        super().__init__()
        # Вкладка "Управление аккаунтами"
        layout = QVBoxLayout()
        # Поле ввода логина
        login_qle = QLineEdit()
        login_qle.setPlaceholderText("Введите логин")
        self.login_qle = login_qle
        # Поле ввода пароля
        password_qle = QLineEdit()
        password_qle.setPlaceholderText("Введите пароль")
        password_qle.setEchoMode(QLineEdit.Password)  # Скрытие пароля
        self.password_qle = password_qle
        # Поле ввода totp secret
        totp_key_qle = QLineEdit()
        totp_key_qle.setPlaceholderText("Ключ для TOTP (необязательно)")
        self.totp_key_qle = totp_key_qle
        totp_key_qpb = QPushButton("🔄")
        totp_key_qpb.clicked.connect(self.totp_key_qpb_clicked)
        totp_key_qhbl = QHBoxLayout()
        totp_key_qhbl.addWidget(totp_key_qle)
        totp_key_qhbl.addWidget(totp_key_qpb)


        # Кнопка "Добавить"
        create_account_qpb = QPushButton("Добавить")
        create_account_qpb.clicked.connect(self.create_account)  # Привязываем кнопку к функции добавления
        # Метка для статуса (успех/ошибка)
        status_ql = QLabel("")
        self.status_ql = status_ql


        ### Добавляем виджеты в основной layout
        layout.addWidget(QLabel("Добавить новый аккаунт"))
        layout.addWidget(login_qle)
        layout.addWidget(password_qle)
        layout.addLayout(totp_key_qhbl)
        layout.addWidget(create_account_qpb)
        layout.addWidget(status_ql)
        self.setLayout(layout)

    def totp_key_qpb_clicked(self):
        self.totp_key_qle.setText(logic.mfa.totp.generate_secret())

    def create_account(self):
        try:
            # Получаем данные из полей ввода
            username = self.login_qle.text()
            password = self.password_qle.text()
            totp_secret = self.totp_key_qle.text()
            # Проверка валидности учетных данных
            if account_management.check_credentials(username, password):
                account_management.save_user(username, password, totp_secret)
                self.status_ql.setText("Успешно")
                self.status_ql.setStyleSheet("color: green;")
            else:
                self.status_ql.setText("Ошибка: неверные данные")
                self.status_ql.setStyleSheet("color: red;")
        except Exception as e:
            print(e)