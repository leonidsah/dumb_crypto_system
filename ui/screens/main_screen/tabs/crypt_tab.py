import time
import traceback

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import logic.values
import my_crypto.rsa
from logic import account_management
from logic.account_management import stribog_hash
from logic.logs import add_log_to_yaml
from my_crypto import kuznechik_wrapper


class CryptTab(QWidget):
    def __init__(self):
        super().__init__()
        # Вкладка "Шифрование"
        self.result = None
        qvbl = QVBoxLayout()

        # Комбо-бокс для выбора алгоритма
        crypt_algo_qcb = QComboBox()
        crypt_algo_qcb.addItem("RSA")
        crypt_algo_qcb.addItem("Кузнечик")
        crypt_algo_qcb.currentIndexChanged.connect(self.crypt_algo_qcb_changed)
        self.crypt_algo_qcb = crypt_algo_qcb
        self.crypt_algo_qhbl = QHBoxLayout()
        self.crypt_algo_qhbl.addWidget(QLabel("Алгоритм шифрования: "))
        self.crypt_algo_qhbl.addWidget(self.crypt_algo_qcb)

        # Форма для выбора файла для шифрования
        source_qle = QLineEdit()
        source_qle.setPlaceholderText("input_text.txt")
        source_qle.setReadOnly(True)  # Только для отображения
        source_qle.textChanged.connect(self.source_qle_changed)
        self.source_qle = source_qle
        source_qpb = QPushButton("📁")
        def source_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл для шифрования", "", "Все файлы (*)")
            if file_name:
                source_qle.setText(file_name)
        source_qpb.clicked.connect(source_qpb_clicked)
        self.file_qhbl = QHBoxLayout()
        self.file_qhbl.addWidget(source_qle)
        self.file_qhbl.addWidget(source_qpb)

        # Форма для выбора ключа шифрования
        crypt_key_qle = QLineEdit()
        crypt_key_qle.setPlaceholderText("my_key.key")
        crypt_key_qle.setReadOnly(True)  # Только для отображения
        crypt_key_qle.textChanged.connect(self.crypt_key_qle_changed)
        self.crypt_key_qle = crypt_key_qle
        crypt_key_qpb = QPushButton("📁")

        def crypt_key_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл с ключом", "", "Все файлы (*)")
            if file_name:
                crypt_key_qle.setText(file_name)

        crypt_key_qpb.clicked.connect(crypt_key_qpb_clicked)
        self.crypt_key_qpb = crypt_key_qpb
        self.crypt_key_qhbl = QHBoxLayout()
        self.crypt_key_qhbl.addWidget(crypt_key_qle)
        self.crypt_key_qhbl.addWidget(crypt_key_qpb)

        # Форма для выбора ключа шифрования для ЭЦП
        sign_pub_key_qle = QLineEdit()
        sign_pub_key_qle.setPlaceholderText("my_public_key.key")
        sign_pub_key_qle.setText(r"texts_and_keys/PUBLIC_KEY_2048.key")
        sign_pub_key_qle.setReadOnly(True)  # Только для отображения
        sign_pub_key_qle.textChanged.connect(self.crypt_key_qle_changed)
        sign_pub_key_qle.textChanged.connect(self.sign_pub_key_qle_changed)
        self.sign_pub_key_qle = sign_pub_key_qle
        sign_pub_key_qpb = QPushButton("📁")
        sign_pub_key_qpb.setEnabled(False)
        sign_pub_key_qpb.setEnabled(False)
        def sign_pub_key_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл с ключом", "", "Все файлы (*)")
            if file_name:
                sign_pub_key_qle.setText(file_name)

        sign_pub_key_qpb.clicked.connect(sign_pub_key_qpb_clicked)
        self.sign_pub_key_qpb = sign_pub_key_qpb
        self.sign_pub_key_qhbl = QHBoxLayout()
        self.sign_pub_key_qhbl.addWidget(QLabel("Открытый: "))
        self.sign_pub_key_qhbl.addWidget(sign_pub_key_qle)
        self.sign_pub_key_qhbl.addWidget(sign_pub_key_qpb)

        # Форма для выбора ключа шифрования для ЭЦП
        sign_pri_key_qle = QLineEdit()
        sign_pri_key_qle.setPlaceholderText("my_private_key.key")
        sign_pri_key_qle.setText(r"texts_and_keys/PRIVATE_KEY_2048.key")
        sign_pri_key_qle.setReadOnly(True)  # Только для отображения
        sign_pri_key_qle.textChanged.connect(self.crypt_key_qle_changed)
        sign_pri_key_qle.textChanged.connect(self.sign_pub_key_qle_changed)
        self.sign_pri_key_qle = sign_pri_key_qle
        sign_pri_key_qpb = QPushButton("📁")
        sign_pri_key_qpb.setEnabled(False)
        sign_pri_key_qpb.setEnabled(False)
        def sign_pri_key_qpb_clicked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл с ключом", "", "Все файлы (*)")
            if file_name:
                sign_pri_key_qle.setText(file_name)
        sign_pri_key_qpb.clicked.connect(sign_pri_key_qpb_clicked)
        self.sign_pri_key_qpb = sign_pri_key_qpb
        self.sign_pri_key_qhbl = QHBoxLayout()
        self.sign_pri_key_qhbl.addWidget(QLabel("Закрытый: "))
        self.sign_pri_key_qhbl.addWidget(sign_pri_key_qle)
        self.sign_pri_key_qhbl.addWidget(sign_pri_key_qpb)

        # Кнопки для шифрования / расшифрования
        encrypt_qpb = QPushButton("Зашифровать")
        encrypt_qpb.setEnabled(False)  # Неактивна до выбора файла и ключа
        encrypt_qpb.clicked.connect(self.encrypt_qpb_clicked)
        self.encrypt_qpb = encrypt_qpb
        decrypt_qpb = QPushButton("Расшифровать")
        decrypt_qpb.setEnabled(False)  # Неактивна до выбора файла и ключа
        decrypt_qpb.clicked.connect(self.decrypt_qpb_clicked)
        self.decrypt_qpb = decrypt_qpb
        self.crypt_qhbl = QHBoxLayout()
        self.crypt_qhbl.addWidget(encrypt_qpb)
        self.crypt_qhbl.addWidget(decrypt_qpb)

        # Кнопки для скачивания .txt и PDF
        download_txt_qpb = QPushButton("Скачать результат (.txt)")
        download_txt_qpb.setEnabled(False)  # Неактивна до выполнения шифрования
        download_txt_qpb.clicked.connect(self.download_txt_qpb_clicked)
        self.download_txt_qpb = download_txt_qpb
        download_pdf_qpb = QPushButton("Скачать PDF с ЭЦП")
        download_pdf_qpb.setEnabled(False)  # Неактивна до выполнения шифрования
        download_pdf_qpb.clicked.connect(self.download_pdf_qpb_clicked)
        self.download_pdf_qpb = download_pdf_qpb
        self.download_qhbl = QHBoxLayout()
        self.download_qhbl.addWidget(download_txt_qpb)
        self.download_qhbl.addWidget(download_pdf_qpb)

        ### Добавляем виджеты в основной layout
        qvbl.addLayout(self.crypt_algo_qhbl)
        qvbl.addWidget(QLabel("Текст для обработки:"))
        qvbl.addLayout(self.file_qhbl)
        qvbl.addWidget(QLabel("Ключ шифрования:"))
        qvbl.addLayout(self.crypt_key_qhbl)
        qvbl.addWidget(QLabel("Ключи для ЭЦП:"))
        qvbl.addLayout(self.sign_pri_key_qhbl)
        qvbl.addLayout(self.sign_pub_key_qhbl)
        qvbl.addLayout(self.crypt_qhbl)
        qvbl.addLayout(self.download_qhbl)
        self.setLayout(qvbl)

    def crypt_algo_qcb_changed(self, index):
        if index == 0:
            self.crypt_key_qpb.setVisible(True)
            self.crypt_key_qle.setReadOnly(True)
            self.crypt_key_qle.setPlaceholderText("my_key.key")
            self.crypt_key_qle.setText("")
        elif index == 1:
            self.crypt_key_qpb.setVisible(False)
            self.crypt_key_qle.setReadOnly(False)
            self.crypt_key_qle.setPlaceholderText("64 шестнадцатеричных символов")
            self.crypt_key_qle.setText("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")

    def source_qle_changed(self):
        self.check_if_ready_to_encrypt()

    def crypt_key_qle_changed(self):
        match self.crypt_algo_qcb.currentIndex():
            case 0:
                # RSA
                self.check_if_ready_to_encrypt()
            case 1:
                # Kuznechik
                if len(self.crypt_key_qle.text()) == 64 and len(self.source_qle.text()) != 0:
                    self.encrypt_qpb.setEnabled(True)
                    self.decrypt_qpb.setEnabled(True)
                else:
                    self.encrypt_qpb.setEnabled(False)
                    self.decrypt_qpb.setEnabled(False)

    def sign_pub_key_qle_changed(self):
        if (len(self.sign_pub_key_qle.text()) > 0) and (len(self.sign_pri_key_qle.text()) > 0):
            self.download_pdf_button.setEnabled(True)

    def encrypt_qpb_clicked(self):
        try:
            action = "encrypt"
            match self.crypt_algo_qcb.currentIndex():
                case 0:
                    # RSA
                    key_path = self.crypt_key_qle.text()
                    file_path = self.source_qle.text()
                    cipher = my_crypto.rsa.import_and_encrypt(key_path, file_path, "encrypt")
                    self.result = cipher
                    action += " RSA"
                case 1:
                    # Kuznechik
                    key = self.crypt_key_qle.text()
                    file_path = self.source_qle.text()
                    cipher = kuznechik_wrapper.kuznechik_encrypt(key, file_path)
                    self.result = cipher
                    action += " KUZ"

            timestamp = int(time.time())
            result_hash = stribog_hash(self.result)
            signature = 0
            try:
                signature = self.form_signature()
            except Exception as e:
                print("Signature creation failed.")
                print(e)
                traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                print(traceback_str)
            add_log_to_yaml(logic.values.username, action, self.result, timestamp, result_hash, signature)

            # После шифрования можно активировать кнопку для скачивания PDF с ЭЦП
            self.sign_pub_key_qpb.setEnabled(True)
            self.sign_pri_key_qpb.setEnabled(True)
            self.download_txt_qpb.setEnabled(True)
            self.download_pdf_qpb.setEnabled(True)
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)

    def decrypt_qpb_clicked(self):
        try:
            # Получаем выбранные файл и ключ, а также алгоритм
            file_name = self.source_qle.text()
            key_name = self.crypt_key_qle.text()
            action = "decrypt"
            match self.crypt_algo_qcb.currentIndex():
                case 0:
                    # RSA
                    key_path = self.crypt_key_qle.text()
                    file_path = self.source_qle.text()
                    message = my_crypto.rsa.import_and_encrypt(key_path, file_path, "decrypt")
                    self.result = message
                    action += " RSA"
                case 1:
                    # Kuznechik
                    key = self.crypt_key_qle.text()
                    file_path = self.source_qle.text()
                    message = kuznechik_wrapper.kuznechik_decrypt(key, file_path)
                    self.result = message
                    action += " KUZ"
            timestamp = int(time.time())
            result_hash = stribog_hash(self.result)
            signature = 0
            try:
                signature = self.form_signature()
            except Exception as e:
                print("Signature creation failed.")
            add_log_to_yaml(logic.values.username, action, self.result, timestamp, result_hash, signature)

            # После шифрования можно активировать кнопку для скачивания PDF с ЭЦП
            self.sign_pub_key_qpb.setEnabled(True)
            self.sign_pri_key_qpb.setEnabled(True)
            self.download_txt_qpb.setEnabled(True)
            self.download_pdf_qpb.setEnabled(True)
        except Exception as e:
            print(e)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(traceback_str)

    def form_signature(self):
        private_key = my_crypto.rsa.import_rsa_key(self.sign_pri_key_qle.text())
        public_key = my_crypto.rsa.import_rsa_key(self.sign_pub_key_qle.text())
        message_hash = account_management.stribog_hash(self.result)
        print(f"form_signature, message hash: {message_hash}")
        signature = my_crypto.rsa.create_signature(message_hash, private_key, public_key)
        return signature

    def download_pdf_qpb_clicked(self):
        def form_output_for_pdf():
            signature = self.form_signature()
            line = '=================='
            output = f"{line}\nСодержание шифровки\n{line}\n{self.result}\n{line}\nЭЦП\n{line}\n{signature}"
            return output

        def download_pdf(text):
            # Открываем диалоговое окно для выбора имени и пути сохранения
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,  # Используем self, так как это метод класса QWidget
                "Сохранить PDF файл",
                "",
                "PDF Files (*.pdf);;All Files (*)",
                options=options
            )

            # Если путь не выбран, выходим из функции
            if not file_path:
                return

            # Убедимся, что файл имеет расширение .pdf
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'

            try:
                # Настройки страницы
                pdf = canvas.Canvas(file_path, pagesize=letter)
                pdfmetrics.registerFont(TTFont('DejaVuSans', 'assets/DejaVuSans.ttf'))
                pdf.setFont('DejaVuSans', 12)  # Устанавливаем шрифт и размер
                width, height = letter  # Размер страницы
                x_margin, y_margin = 50, 750  # Отступы
                line_height = 14  # Высота строки

                # Обрабатываем текст с учётом переносов строк
                lines = []
                for paragraph in text.split('\n'):  # Разделяем текст по '\n'
                    current_line = ""
                    for char in paragraph:
                        current_line += char
                        if pdf.stringWidth(current_line) > (width - 2 * x_margin):
                            lines.append(current_line)  # Добавляем строку
                            current_line = ""  # Начинаем новую строку
                    if current_line:
                        lines.append(current_line)

                # Рисуем текст на странице
                for line in lines:
                    if y_margin < 50:  # Проверка на конец страницы
                        pdf.showPage()  # Добавляем новую страницу
                        pdf.setFont('DejaVuSans', 12)  # Устанавливаем шрифт на новой странице
                        y_margin = 750  # Сбрасываем координаты
                    pdf.drawString(x_margin, y_margin, line)
                    y_margin -= line_height
                pdf.save()  # Сохраняем PDF
                print(f"PDF успешно сохранен по пути: {file_path}")
            except Exception as e:
                print(f"Ошибка при сохранении PDF: {e}")

        try:
            output = form_output_for_pdf()
            download_pdf(output)
        except Exception as e:
            print(e)

    def download_txt_qpb_clicked(self):
        # Открываем диалог для выбора папки
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохраните результат")

        if file_path:  # Если путь выбран
            try:
                # Создаем пустой файл result.txt
                with open(file_path, 'w') as file:
                    file.write(str(self.result))
                print(f"Файл сохранен по пути: {file_path}")
            except Exception as e:
                print(f"Ошибка при создании файла: {e}")
        else:
            print("Путь для сохранения не был выбран.")

    def check_if_ready_to_encrypt(self):
        # Проверить, выбраны ли оба файла: для шифрования и ключ
        file_name = self.source_qle.text()
        key_name = self.crypt_key_qle.text()

        if file_name and key_name:
            # Активировать кнопки
            self.encrypt_qpb.setEnabled(True)
            self.decrypt_qpb.setEnabled(True)
        else:
            # Деактивировать кнопки
            self.encrypt_qpb.setEnabled(False)
            self.decrypt_qpb.setEnabled(False)
