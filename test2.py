import os
import tempfile
import unittest
from unittest.mock import patch

from main import InputType, choose_input_type, process_data, process_from_file, process_from_http, process_input


class ProcessInputTests(unittest.TestCase):
    def test_process_input_number(self):
        self.assertEqual(
            process_input("12"),
            "Введено число: 12. Квадрат: 144",
        )

    def test_process_input_string(self):
        self.assertEqual(
            process_input("hello"),
            "Введена строка: 'hello'. Длина: 5",
        )

    def test_process_input_strips_spaces(self):
        self.assertEqual(
            process_input("  test  "),
            "Введена строка: 'test'. Длина: 4",
        )

    def test_process_input_empty(self):
        self.assertEqual(
            process_input("   "),
            "Ошибка: введены пустые данные",
        )


class FileInputTests(unittest.TestCase):
    def test_process_from_file_with_number(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write("25")
            temp_name = temp_file.name

        self.addCleanup(lambda: os.path.exists(temp_name) and os.remove(temp_name))

        self.assertEqual(
            process_from_file(temp_name),
            "Введено число: 25. Квадрат: 625",
        )

    def test_process_from_file_not_found(self):
        missing_file = "missing_input_file.txt"
        self.assertEqual(
            process_from_file(missing_file),
            f"Ошибка: файл '{missing_file}' не найден",
        )


class HttpInputTests(unittest.TestCase):
    def test_process_from_http_valid_url(self):
        self.assertEqual(
            process_from_http("https://example.com"),
            "Ссылка получена: https://example.com",
        )

    def test_process_from_http_empty_url(self):
        self.assertEqual(
            process_from_http("   "),
            "Ошибка: ссылка не введена",
        )


class ChooseInputTypeTests(unittest.TestCase):
    @patch("builtins.input", return_value="1")
    def test_choose_input_type_stdin(self, _mock_input):
        self.assertEqual(choose_input_type(), InputType.STDIN)

    @patch("builtins.input", return_value="2")
    def test_choose_input_type_file(self, _mock_input):
        self.assertEqual(choose_input_type(), InputType.FILE)

    @patch("builtins.input", return_value="3")
    def test_choose_input_type_http(self, _mock_input):
        self.assertEqual(choose_input_type(), InputType.HTTP)

    @patch("builtins.input", return_value="99")
    def test_choose_input_type_unknown(self, _mock_input):
        self.assertEqual(choose_input_type(), InputType.UNKNOWN)


class ProcessDataTests(unittest.TestCase):
    @patch("main.process_from_stdin", return_value="stdin result")
    def test_process_data_stdin(self, mock_process_from_stdin):
        self.assertEqual(process_data(InputType.STDIN), "stdin result")
        mock_process_from_stdin.assert_called_once_with()

    @patch("builtins.input", return_value="input.txt")
    @patch("main.process_from_file", return_value="file result")
    def test_process_data_file(self, mock_process_from_file, _mock_input):
        self.assertEqual(process_data(InputType.FILE), "file result")
        mock_process_from_file.assert_called_once_with("input.txt")

    @patch("builtins.input", return_value="https://example.com")
    @patch("main.process_from_http", return_value="http result")
    def test_process_data_http(self, mock_process_from_http, _mock_input):
        self.assertEqual(process_data(InputType.HTTP), "http result")
        mock_process_from_http.assert_called_once_with("https://example.com")

    def test_process_data_unknown_type_exits(self):
        with self.assertRaises(SystemExit) as error:
            process_data(InputType.UNKNOWN)

        self.assertEqual(error.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
