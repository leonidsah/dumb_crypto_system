import random

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, \
    QFileDialog
from pyqtspinner import spinner

from my_crypto.rsa import generate_keys, export_rsa_key


class KeysTab(QWidget):
    def __init__(self):
        super().__init__()
        qvbl = QVBoxLayout()
        # Вкладка "Ключи"
        keys_tabs = QTabWidget()
        rsa_keys_tab = QWidget()
        kuznechik_qvbl = QWidget()
        # Подвкладка "RSA"
        rsa_qvbl = QVBoxLayout()
        rsa_qvbl.alignment()
        # Выбор битности ключей
        key_size_qcb = QComboBox()
        key_size_qcb.addItem("2048")
        key_size_qcb.addItem("4096")
        key_size_qcb.addItem("8192")
        self.key_size_qcb = key_size_qcb
        # Поле ввода label'а публичного ключа
        pub_key_qle = QLineEdit()
        pub_key_qle.setText("PUBLIC_KEY")
        self.pub_key_qle = pub_key_qle
        # Поле ввода label'а приватного ключа
        pri_key_qle = QLineEdit()
        pri_key_qle.setText("PRIVATE_KEY")
        self.pri_key_qle = pri_key_qle
        # Поле выбора пути сохранения ключей
        rsa_export_qpb = QPushButton("Сохранить")
        rsa_export_qpb.setEnabled(False)
        rsa_export_qpb.clicked.connect(self.select_rsa_export_path)
        self.rsa_export_qpb = rsa_export_qpb

        # Значок с кружочком ожидания и галочкой в случае успешного завершения создания ключей
        # Кнопка сгенерировать ключи
        generate_qpb = QPushButton("Сгенерировать ключи")
        generate_qpb.clicked.connect(self.generate_rsa_keys)
        self.generate_qpb = generate_qpb
        status_qspnr = spinner.WaitingSpinner(self, False, False)
        status_qspnr.start()
        status_qspnr.color = QtCore.Qt.GlobalColor.cyan
        status_qspnr.setVisible(False)
        status_ql = QLabel("✅")
        status_ql.setVisible(False)
        self.status_ql = status_ql
        generate_qhbl = QHBoxLayout()
        generate_qhbl.addWidget(generate_qpb)
        generate_qhbl.addWidget(status_qspnr)
        generate_qhbl.addWidget(status_ql)

        # Добавляем виджеты в макет
        rsa_qvbl.addWidget(QLabel("Размер ключа:"))
        rsa_qvbl.addWidget(key_size_qcb)
        rsa_qvbl.addWidget(QLabel("Имя открытого ключа:"))
        rsa_qvbl.addWidget(pub_key_qle)
        rsa_qvbl.addWidget(QLabel("Имя закрытого ключа:"))
        rsa_qvbl.addWidget(pri_key_qle)
        rsa_qvbl.addLayout(generate_qhbl)
        rsa_qvbl.addWidget(rsa_export_qpb)
        # Подвкладка "Кузнечик"
        kuznechik_qvbl = QWidget()
        self.kuz_keys_layout = QVBoxLayout()
        self.kuz_keys_layout.alignment()
        # Поле ввода label'а публичного ключа
        self.kuz_key_line = QLineEdit()
        self.kuz_key_line.setText("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")
        self.kuz_key_line.setReadOnly(True)
        # Кнопка сгенерировать ключи
        self.kuz_generate_key_button = QPushButton("Сгенерировать ключ (256 бит)")
        self.kuz_generate_key_button.clicked.connect(self.kuz_generate_key)

        # Добавляем виджеты в макет
        self.kuz_keys_layout.addWidget(QLabel("Ключ шифрования:"), alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.kuz_keys_layout.addWidget(self.kuz_key_line)
        self.kuz_keys_layout.addWidget(self.kuz_generate_key_button)

        keys_tabs.addTab(rsa_keys_tab, "RSA")
        keys_tabs.addTab(kuznechik_qvbl, "Кузнечик")
        rsa_keys_tab.setLayout(rsa_qvbl)
        kuznechik_qvbl.setLayout(self.kuz_keys_layout)
        qvbl.addWidget(keys_tabs)
        self.setLayout(qvbl)

    def generate_rsa_keys(self):
        # Пока функция выполняется сделать поля ввода серыми
        self.pri_key_qle.setEnabled(False)
        self.pub_key_qle.setEnabled(False)
        self.generate_qpb.setEnabled(False)
        self.key_size_qcb.setEnabled(False)
        self.rsa_export_qpb.setText("Сохранить")
        # Вызвать функцию, передать ей имена ключей
        self.public_key, self.private_key = generate_keys(int(self.key_size_qcb.currentText()))
        # Когда функция закончила выполнение - сделать активной кнопку сохранения и поля ввода
        self.status_ql.setVisible(True)
        self.rsa_export_qpb.setEnabled(True)

    def select_rsa_export_path(self):
        try:
            # Открыть диалог для выбора файла с ключом
            folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения ключей")
            export_rsa_key(self.private_key, folder_path, self.pri_key_qle.text())
            export_rsa_key(self.public_key, folder_path, self.pub_key_qle.text())
            self.private_key = None
            self.public_key = None

            self.pri_key_qle.setEnabled(True)
            self.pub_key_qle.setEnabled(True)
            self.generate_qpb.setEnabled(True)
            self.key_size_qcb.setEnabled(True)
            self.rsa_export_qpb.setEnabled(False)
            self.status_ql.setVisible(False)
            self.rsa_export_qpb.setText("Сохранено")
        except Exception as e:
            print(e)

    def kuz_generate_key(self):
        def generate_hex_string(length=64):
            return ''.join(random.choice('0123456789abcdef') for _ in range(length))

        self.kuz_key = generate_hex_string()
        self.kuz_key_line.setText(self.kuz_key)