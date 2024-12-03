import yaml

def add_log_to_yaml(login, action, result, timestamp, result_hash, signature,
                    file_path=r"C:\Users\leoni\PycharmProjects\dumb_crypto_system\logic\logs.yaml"):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    if 'users' not in data:
        data['users'] = []

    new_user = {
        'login': login,
        'action': action,
        'result': f'{result}',
        'timestamp': timestamp,
        'hash': result_hash,
        'signature': signature
    }

    data['users'].append(new_user)

    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)
