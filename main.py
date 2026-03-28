from enum import Enum
from sys import exit


class InputType(Enum):
    UNKNOWN = 0
    STDIN = 1
    FILE = 2
    HTTP = 3


def process_input(data: str) -> str:
    data = data.strip()

    if data.isdigit():
        number = int(data)
        return f"Число: {number}, квадрат: {number ** 2}"

    if data == "":
        return "Пустой ввод"

    return f"Строка: {data}, длина: {len(data)}"


def process_from_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
        return process_input(data)
    except FileNotFoundError:
        return "Файл не найден"


def process_from_http(url: str) -> str:
    if url.strip() == "":
        return "Пустая ссылка"
    return f"Ссылка получена: {url}"


def process_from_stdin() -> str:
    data = input("Введите данные: ")
    return process_input(data)


def choose_input_type() -> InputType:
    print("Выберите режим ввода:")
    print("1 - ввод с клавиатуры")
    print("2 - ввод из файла")
    print("3 - ввод по ссылке")

    choice = input("Введите номер режима: ").strip()

    match choice:
        case "1":
            return InputType.STDIN
        case "2":
            return InputType.FILE
        case "3":
            return InputType.HTTP
        case _:
            return InputType.UNKNOWN


def process_data(in_type: InputType) -> str:
    match in_type:
        case InputType.STDIN:
            return process_from_stdin()
        case InputType.FILE:
            filename = input("Введите имя файла: ")
            return process_from_file(filename)
        case InputType.HTTP:
            url = input("Введите ссылку: ")
            return process_from_http(url)
        case _:
            print("unknown input type")
            exit(1)


if __name__ == "__main__":
    print("Запуск программы")
    input_type = choose_input_type()
    print(process_data(input_type))