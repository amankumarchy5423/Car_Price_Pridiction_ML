from src.logging.logger import my_logger
# import Exception
import os
import sys



class MyException(Exception):
    def __init__(self, message, error_details:sys):
        try : 
            self.message = message
            _,_,exc_tb = error_details.exc_info()

            self.lineno=exc_tb.tb_lineno
            self.file_name=exc_tb.tb_frame.f_code.co_filename 
        except Exception as e:
            my_logger.error(f"Error in MyException: {e}")
    
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))
    
# if __name__=='__main__':
#     try:
#         # my_logger.info("Enter the try block")
#         a=1/0
#         print("This will not be printed",a)
#     except Exception as e:
#         # my_logger.error(e)
#         raise MyException(e,sys)