import argparse
import csv

import requests

state={
    "packageName": "",
    "path": "",
    "mode": "0",
    "packageVersion": ""
}

def all_digits(s):
    return all(c in "0123456789" for c in s) and s

def check_version(ver):
    if (ver=="latest"):
        return True
    symbols = ver.split('.')
    if (all([all_digits(s) for s in symbols[:-1]])):
        return True
    return False

def get_state(file_path):
    """Получение параметров из CSV файла"""
    with open(file_path, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for key, val in row.items():
                if (key in state.keys()):
                    if (key=="packageVersion" and not check_version(val)):
                        print(f"Неверный формат версии! {val}")
                        exit()
                    if (key=="mode" and val not in ("0", "1")):
                        print("Неверный режим работы! "
                              "По умолчанию установлен режим 0(URL)")
                        continue
                    state[key] = val
                else:
                    print(f"Неизвестный ключ: {key}")

def build_url(base_url, package_name, version):
    """Формирует URL для запроса к PyPI API."""
    base = base_url.rstrip("/")
    if version == "latest" or not version:
        return f"{base}/{package_name}/json"
    return f"{base}/{package_name}/{version}/json"

def fetch_package_data(url):
    """Загружает JSON-данные о пакете по URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            print(f"Пакет не найден по URL: {url}")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Ошибка: превышено время ожидания ответа!")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def print_package_info(package_info):
    """Выводит основную информацию о пакете."""
    print("\n=== Информация о пакете ===")
    print(f"Имя: {package_info.get('name', 'N/A')}")
    print(f"Версия: {package_info.get('version', 'N/A')}")
    print(f"Описание: {package_info.get('summary', 'N/A')}")

def extract_direct_dependencies(requires_dist):
    """Извлекает прямые зависимости, исключая условные (extra)."""
    if not requires_dist:
        return []
    return [dep for dep in requires_dist if "; extra ==" not in dep]

def print_dependencies(dependencies):
    """Выводит список зависимостей на экран."""
    if not dependencies:
        print("\nПакет не имеет прямых зависимостей.")
        return
    print(f"\n=== Прямые зависимости ({len(dependencies)}) ===")
    for dep in dependencies:
        print(f"  - {dep}")

def get_dependencies():
    """Получение прямых зависимостей пакета."""
    package_name = state["packageName"]
    version = state["packageVersion"]
    mode = state["mode"]
    path = state["path"]

    if not package_name:
        print("Ошибка: не указано имя пакета!")
        return []

    if mode == "0":
        url = build_url(path, package_name, version)
        data = fetch_package_data(url)
        if not data:
            return []
        package_info = data.get("info", {})
    else:
        print("Режим 1 (локальный файл) будет реализован на этапе 3.")
        return []

    print_package_info(package_info)
    requires_dist = package_info.get("requires_dist", None)
    dependencies = extract_direct_dependencies(requires_dist)
    print_dependencies(dependencies)
    return dependencies

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default="../testConfig.csv",
                        help="Путь к файлу конфигурации")

    args = parser.parse_args()
    get_state(args.path)
    for key, val in state.items():
        print(f"{key}: {val}")
    get_dependencies()

if (__name__=="__main__"):
    main()