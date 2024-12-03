import traceback

import qrcode.image.base
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from logic import values
from logic.mfa.qr_code import get_pixmap, generate_qr_data
from logic.mfa.totp import verify_totp, is_totp_set_up
import logic.values


class AuthScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.qr_auth_success = False
        self.totp_auth_success = False
        layout = QVBoxLayout()

        # Отображаем сообщение о необходимости ввода OTP
        qr_code_qle = QLineEdit()
        qr_code_qle.setPlaceholderText("Значение из QR-кода")
        self.qr_code_qle = qr_code_qle
        self.qr_code_value = generate_qr_data()

        qr_code_pixmap = get_pixmap(self.qr_code_value)
        qr_code_ql = QLabel()
        qr_code_ql.setPixmap(qr_code_pixmap)
        qr_code_ql.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # TOTP
        totp_qle = QLineEdit()
        totp_qle.setPlaceholderText("Временный код")
        self.totp_qle = totp_qle

        check_qpb = QPushButton("Проверить")
        check_qpb.clicked.connect(self.verify_auth)
        status_ql = QLabel("")
        self.status_ql = status_ql

        layout.addWidget(QLabel("Отсканируйте QR-код:"))
        layout.addWidget(qr_code_ql)
        layout.addWidget(qr_code_qle)
        layout.addWidget(QLabel("Введите код из мобильного приложения:"))
        layout.addWidget(totp_qle)
        layout.addWidget(check_qpb)
        layout.addWidget(status_ql)
        self.setLayout(layout)


    def showEvent(self, event):
        try:
            super().showEvent(event)
            self.totp_check()
            print(f"QR-code: {self.qr_code_value}")
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)

    def verify_qr_auth(self):
        if not self.qr_auth_success:
            self.qr_auth_success = self.qr_code_qle.text() == self.qr_code_value

    def verify_totp_auth(self):
        if not self.totp_auth_success:
            self.totp_auth_success = verify_totp(logic.values.username, self.totp_qle.text())

    def verify_auth(self):
        try:
            self.verify_qr_auth()
            self.verify_totp_auth()
            if self.qr_auth_success and self.totp_auth_success:
                if logic.values.username != "admin":
                    # Получаем MainAppScreen из QStackedWidget и вызываем hide_account_tab
                    main_app_screen = self.parentWidget().widget(2)
                    main_app_screen.hide_unprivileged()
                self.status_ql.setText("")
                self.parentWidget().setCurrentIndex(2)
            else:
                if (not self.qr_auth_success) and (not self.totp_auth_success):
                    status = "Проверки с QR и временным кодом не удались."
                elif not self.qr_auth_success:
                    status = "Проверка с QR-кодом не удалась."
                elif not self.totp_auth_success:
                    status = "Проверка с временным кодом не удалась."
                self.status_ql.setStyleSheet("color: red;")
                self.status_ql.setText(status)
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)

    def totp_check(self):
        if is_totp_set_up(logic.values.username):
            pass
        else:
            self.totp_auth_success = True
            self.totp_qle.setEnabled(False)
            self.totp_qle.setPlaceholderText("Проверка временных кодов не настроена")
