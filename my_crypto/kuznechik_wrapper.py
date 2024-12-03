import subprocess


def kuznechik_encrypt(key, path):
    """Вычисляет хеш строки data, используя внешнюю программу stribog.exe."""
    try:
        # Вызов stribog.exe с аргументом data и получение хеша из вывода
        result = subprocess.run(["my_crypto/eriebanksy-kuznyechik.exe", key, path, "enc"], capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Убираем лишние пробелы/переносы строк
    except subprocess.CalledProcessError as e:
        print("Ошибка при вызове eriebanksy-kuznyechik.exe:", e)
        return None

def kuznechik_decrypt(key, path):
    """Вычисляет хеш строки data, используя внешнюю программу stribog.exe."""
    try:
        # Вызов stribog.exe с аргументом data и получение хеша из вывода
        result = subprocess.run(["my_crypto/eriebanksy-kuznyechik.exe", key, path, "dec"], capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()  # Убираем лишние пробелы/переносы строк
    except subprocess.CalledProcessError as e:
        print("Ошибка при вызове eriebanksy-kuznyechik.exe:", e)
        return None