import yaml
import os
import subprocess
import secrets
import re


def generate_salt(length=16):
    """Генерирует случайную соль длиной length символов."""
    return secrets.token_hex(length // 2)


def stribog_hash(data):
    """Вычисляет хеш строки data, используя внешнюю программу stribog.exe."""
    try:
        # Вызов stribog.exe с аргументом data и получение хеша из вывода
        result = subprocess.run(["my_crypto/stribog.exe", str(data)], capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Убираем лишние пробелы/переносы строк
    except subprocess.CalledProcessError as e:
        print("Ошибка при вызове stribog.exe:", e)
        return None


def save_user(username, password, totp_secret, filepath="logic/accounts.yaml"):
    """Сохраняет имя пользователя, соль и хеш пароля в файл YAML."""
    salt = stribog_hash(generate_salt())
    if totp_secret == "":
        totp_secret = "~"

    # Вычисляем хеш с помощью stribog.exe
    password_hash = stribog_hash(password + salt)
    if password_hash is None:
        print("Не удалось сгенерировать хеш пароля.")
        return

    # Загружаем существующие данные, если файл существует
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            data = yaml.safe_load(file) or {"users": []}
    else:
        data = {"users": []}

    # Добавляем нового пользователя с хешем и солью
    data["users"].append({
        "login": username,
        "password_hash": password_hash,
        "salt": salt,
        "totp_key": totp_secret,
    })

    # Сохраняем обновленные данные в YAML-файл
    with open(filepath, "w") as file:
        yaml.dump(data, file)

    print(f"Пользователь {username} успешно сохранен в {filepath}.")


def verify_user(username, password, filepath="logic/accounts.yaml"):
    """Проверяет введённый пользователем пароль, используя хеш и соль из users.yaml."""
    try:
        # Загрузка данных из YAML-файла
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)

        # Ищем пользователя по имени
        user = next((u for u in data["users"] if u["login"] == username), None)

        if not user:
            print("Пользователь не найден.")
            return False

        # Получаем соль и сохраненный хеш из файла
        salt = user["salt"]
        stored_hash = user["password_hash"]

        # Комбинируем введенный пароль с солью
        salted_password = password + salt

        # Генерируем хеш для проверки
        computed_hash = stribog_hash(salted_password)

        if computed_hash is None:
            print("Не удалось сгенерировать хеш для проверки.")
            return False

        # Сравниваем с сохраненным хешем
        if computed_hash == stored_hash:
            print("Пароль верный")
            return True
        else:
            print("Неверный пароль")
            return False

    except FileNotFoundError:
        print("Файл users.yaml не найден.")
        return False
    except yaml.YAMLError:
        print("Ошибка при чтении файла YAML.")
        return False

def check_credentials(login, password):
    # Проверяем, что длина логина и пароля от 1 до 32 символов и что они содержат только a-z, A-Z, 0-9
    if not (1 <= len(login) <= 32) or not (6 <= len(password) <= 32):
        return False

    # Регулярное выражение для проверки символов
    valid_pattern = re.compile(r'^[a-zA-Z0-9_]+$')

    # Проверяем, что логин и пароль соответствуют шаблону
    if not valid_pattern.match(login) or not valid_pattern.match(password):
        return False
    return True

# Пример использования
#verify_user("admin", "simple_password")
#save_user("admin", "simple_password")
#save_user("user1", "user1_password")