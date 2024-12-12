import time
import pyotp
import qrcode
import yaml

def generate_secret():
    return pyotp.random_base32()

def get_totp_key(login, filepath=r"logic/accounts.yaml"):
    try:
        # Загрузка данных из YAML-файла
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)

        # Ищем пользователя по имени
        for user in data['users']:
            if user['login'] == login:
                if 'totp_key' in user:
                    return user['totp_key']
                else:
                    return None

    except FileNotFoundError:
        print("Файл accounts.yaml не найден.")
        return False
    except yaml.YAMLError:
        print("Ошибка при чтении файла YAML.")
        return False

def verify_totp(login, input):
    secret_key = get_totp_key(login)
    totp = pyotp.TOTP(secret_key)
    return totp.verify(input)

def is_totp_set_up(login, filepath=r"logic/accounts.yaml"):
    try:
        # Загрузка данных из YAML-файла
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)

        totp_key = None
        # Ищем пользователя по имени
        for user in data['users']:
            if user['login'] == login:
                if 'totp_key' in user:
                    if user['totp_key'] == '~':
                        return False
                    else:
                        return True
                else:
                    return False
    except FileNotFoundError:
        print("Файл accounts.yaml не найден.")
        return False
    except yaml.YAMLError:
        print("Ошибка при чтении файла YAML.")
        return False