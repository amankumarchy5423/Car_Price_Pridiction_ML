from src.exception.project_exception import MyException
from src.logging.logger import my_logger
import sys


def main():
    try:
        val = 10 / 0
        print("Hello from complete-ml-pipeline!",val)
    except Exception as e :
        MyException(e,sys)
        my_logger.error(e)


if __name__ == "__main__":
    main()
