import traceback

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog

import my_crypto.rsa
from logic import account_management


class CheckSignatureTab(QWidget):
    def __init__(self):
        super().__init__()

        # Вкладка "Проверка ЭЦП"
        qvbl = QVBoxLayout()

        # Форма для ввода ЭЦП
        signature_qle = QLineEdit()
        signature_qle.setPlaceholderText("ЭЦП")
        signature_qle.textChanged.connect(self.signature_qle_changed)
        self.signature_qle = signature_qle

        # Форма для выбора файла с текстом
        source_qle = QLineEdit()
        source_qle.setPlaceholderText("input_text.txt")
        source_qle.setReadOnly(True)
        self.source_qle = source_qle
        source_qpb = QPushButton("📁")
        def source_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл для проверки ЭЦП", "", "Все файлы (*)")
            if file_name:
                source_qle.setText(file_name)
        source_qpb.clicked.connect(source_qpb_clicked)
        source_qhbl = QHBoxLayout()
        source_qhbl.addWidget(source_qle)
        source_qhbl.addWidget(source_qpb)

        # Форма для выбора файла с публичным ключом
        sign_pub_key_qle = QLineEdit()
        sign_pub_key_qle.setPlaceholderText("public.key")
        sign_pub_key_qle.setReadOnly(True)
        self.sign_pub_key_qle = sign_pub_key_qle
        sign_pub_key_qpb = QPushButton("📁")
        def sign_pub_key_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать публичный ключ проверки ЭЦП", "", "Все файлы (*)")
            if file_name:
                sign_pub_key_qle.setText(file_name)
        sign_pub_key_qpb.clicked.connect(sign_pub_key_qpb_clicked)
        sign_pub_key_qle.textChanged.connect(self.signature_key_input_changed)
        sign_pub_key_qhbl = QHBoxLayout()
        sign_pub_key_qhbl.addWidget(sign_pub_key_qle)
        sign_pub_key_qhbl.addWidget(sign_pub_key_qpb)

        # Кнопка "проверить"
        check_signature_qpb = QPushButton("Проверить")
        check_signature_qpb.setEnabled(False)  # Неактивна до выбора файла и ключа
        check_signature_qpb.clicked.connect(self.check_signature)
        self.check_signature_qpb = check_signature_qpb
        # Надпись с результатом
        status_ql = QLabel("")
        self.status_ql = status_ql

        ### Добавляем виджеты в основной layout
        qvbl.addWidget(QLabel("ЭЦП:"))
        qvbl.addWidget(signature_qle)
        qvbl.addWidget(QLabel("Исходный текст:"))
        qvbl.addLayout(source_qhbl)
        qvbl.addWidget(QLabel("Публичный ключ:"))
        qvbl.addLayout(sign_pub_key_qhbl)
        qvbl.addWidget(check_signature_qpb)
        qvbl.addWidget(status_ql)

        self.setLayout(qvbl)

    def signature_qle_changed(self):
        text = self.signature_qle.text()
        if text.find('\n') != -1:
            self.signature_qle.setText(text.replace('\n', ''))

    def sign_pub_key_qpb_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать публичный ключ проверки ЭЦП", "", "Все файлы (*)")
        if file_name:
            self.sign_pub_key_qle.setText(file_name)

    def signature_key_input_changed(self):
        if (len(self.source_qle.text()) > 0) and (len(self.sign_pub_key_qle.text())) > 0:
            self.check_signature_qpb.setEnabled(True)

    def check_signature(self):
        try:
            signature = int(self.signature_qle.text())
            public_key = my_crypto.rsa.import_rsa_key(self.sign_pub_key_qle.text())
            f = open(self.source_qle.text(), 'r')
            text = f.read()
            message_hash = account_management.stribog_hash(text)
            check = my_crypto.rsa.check_signature(signature, message_hash, public_key)
            if check:
                self.status_ql.setText("Подлинность автора текста подтверждена")
                self.status_ql.setStyleSheet("color: green;")
            else:
                self.status_ql.setText("Подлинность автора текста не подтверждена")
                self.status_ql.setStyleSheet("color: red;")
        except Exception as e:
            self.status_ql.setText("Ошибка. Подлинность автора текста не подтверждена")
            self.status_ql.setStyleSheet("color: red;")
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)
