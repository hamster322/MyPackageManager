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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default="../testConfig.csv",
                        help="Путь к файлу конфигурации")

    args = parser.parse_args()
    get_state(args.path)
    for key, val in state.items():
        print(f"{key}: {val}")

if (__name__=="__main__"):
    main()