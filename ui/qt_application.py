from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

import logic.values
from ui.screens.auth_screen.auth_screen import AuthScreen
from ui.screens.login_screen.login_screen import LoginScreen
from ui.screens.main_screen.main_screen import MainAppScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КриптоКролик")
        self.setGeometry(500, 300, 1200, 500)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon("assets/icon_chatgpt.ico"))

        self.login_screen = LoginScreen()
        self.auth_screen = AuthScreen()
        self.main_app_screen = MainAppScreen()

        self.central_widget.addWidget(self.login_screen)  # Экран логина
        self.central_widget.addWidget(self.auth_screen)  # Экран многофакторной аутентификации
        self.central_widget.addWidget(self.main_app_screen)  # Основной экран программы

        if logic.values.skip_auth:
            logic.values.username = "admin"
            self.central_widget.setCurrentIndex(2)  # Переход на экран аутентификации


