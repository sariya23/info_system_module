from enum import Enum
from sys import exit


class InputType(Enum):
    UNKNOWN = 0
    STDIN = 1
    FILE = 2
    HTTP = 3
    
def process_from_file(filename: str) -> str:
    pass

def process_from_http(url: str) -> str:
    pass 

def process_from_stdin() -> str:
    data = input()
    return data

def process_data(in_type: InputType):
    match in_type:
        case InputType.STDIN:
            return process_from_stdin()
        case InputType.FILE:
            filename = input()
            return process_from_file(filename)
        case InputType.HTTP:
            url = input()
            return process_from_http(url)
        case _:
            print("unknown input type")
            exit(1)
            

if __name__ == "__main__":
    print(process_data(InputType.STDIN))