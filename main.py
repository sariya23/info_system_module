from enum import Enum
from sys import exit
#test

class InputType(Enum):
    UNKNOWN = 0
    STDIN = 1
    FILE = 2
    HTTP = 3


def process_input(data: str) -> str:
    data = data.strip()

    if data.isdigit():
        number = int(data)
        return f"Введено число: {number}. Квадрат: {number ** 2}"

    if data == "":
        return "Ошибка: введены пустые данные"

    return f"Введена строка: '{data}'. Длина: {len(data)}"


def process_from_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
        return process_input(data)
    except FileNotFoundError:
        return f"Ошибка: файл '{filename}' не найден"


def process_from_http(url: str) -> str:
    if url.strip() == "":
        return "Ошибка: ссылка не введена"
    return f"Ссылка получена: {url}"


def process_from_stdin() -> str:
    data = input("Введите текст или число: ")
    return process_input(data)


def choose_input_type() -> InputType:
    print("Выберите режим ввода:")
    print("1 - ввод с клавиатуры")
    print("2 - чтение из файла")
    print("3 - ввод ссылки")

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
            print("Неизвестный тип ввода")
            exit(1)


if __name__ == "__main__":
    print("Программа запущена")
    input_type = choose_input_type()
    result = process_data(input_type)
    print("Результат:")
    print(result)
