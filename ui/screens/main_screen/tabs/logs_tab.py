import yaml
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QScrollArea
)


class LogsTab(QWidget):
    def __init__(self, logs_path = r"logic/logs.yaml"):
        super().__init__()
        layout = QVBoxLayout()

        # Создаем заголовок
        header = QLabel("Обозреватель шифров пользователей")
        layout.addWidget(header)

        # Создаем прокручиваемый виджет
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Создаем дерево
        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels(["Поле", "Значение"])

        # Загружаем данные из YAML
        try:
            with open(logs_path, 'r', encoding='utf-8') as file:
                logs_data = yaml.safe_load(file)
            self.populate_tree(tree_widget, logs_data)
        except Exception as e:
            error_label = QLabel(f"Error loading YAML: {e}")
            layout.addWidget(error_label)

        # Добавляем дерево в прокручиваемую область
        scroll_area.setWidget(tree_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def populate_tree(self, tree_widget, data):
        """
        Рекурсивное заполнение QTreeWidget данными из словаря или списка.
        """
        if not isinstance(data, dict):
            return

        for user in data.get("users", []):
            user_item = QTreeWidgetItem(tree_widget)
            user_item.setText(0, "result_hash")
            user_item.setText(1, user.get("hash", "Unknown"))

            # Добавляем вложенные поля
            for key, value in user.items():
                field_item = QTreeWidgetItem(user_item)
                field_item.setText(0, key)
                field_item.setText(1, str(value))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Путь к YAML файлу
    logs_path = r"logic/logs.yaml"

    window = LogsTab(logs_path)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
