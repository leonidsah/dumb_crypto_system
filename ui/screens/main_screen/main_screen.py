from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel

import logic.values
from ui.screens.main_screen.tabs.accounts_tab import AccountsTab
from ui.screens.main_screen.tabs.check_signature_tab import CheckSignatureTab
from ui.screens.main_screen.tabs.crypt_tab import CryptTab
from ui.screens.main_screen.tabs.keys_tab import KeysTab
from ui.screens.main_screen.tabs.logs_tab import LogsTab


class MainAppScreen(QWidget):
    def __init__(self):
        super().__init__()
        screen_qvbl = QVBoxLayout()

        self.tabs = QTabWidget()
        self.crypt_tab = CryptTab()
        self.keys_tab = KeysTab()
        self.check_signature_tab = CheckSignatureTab()
        self.accounts_tab = AccountsTab()
        self.logs_tab = LogsTab()
        # Вкладка "Шифрование"
        self.tabs.addTab(self.crypt_tab, "Шифрование")
        # Вкладка "Ключи"
        self.tabs.addTab(self.keys_tab, "Ключи")
        # Вкладка "Проверка ЭЦП"
        self.tabs.addTab(self.check_signature_tab, "Проверка ЭЦП")
        # Вкладка "Аккаунты"
        self.tabs.addTab(self.accounts_tab, "Аккаунты")
        # Вкладка "Шифровки"
        self.tabs.addTab(self.logs_tab, "Шифровки")

        login_ql = QLabel()
        login_ql.setStyleSheet("color: gray;")
        login_ql.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_ql = login_ql

        screen_qvbl.addWidget(self.tabs)
        screen_qvbl.addWidget(login_ql)

        self.setLayout(screen_qvbl)

    def showEvent(self, event):
        super().showEvent(event)
        self.login_ql.setText("Аккаунт: 👤" + ("[NO_USER]" if logic.values.username is None else logic.values.username))

    def hide_unprivileged(self):
        index = self.tabs.indexOf(self.accounts_tab)
        if index != -1:
            self.tabs.removeTab(index)
        index = self.tabs.indexOf(self.logs_tab)
        if index != -1:
            self.tabs.removeTab(index)
