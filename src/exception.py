import sys
from logger import logging

def error_message_detail(error,error_detail:sys):
    
    _,_,exc_trace_back = error_detail.exc_info()  # return (type, value, traceback)
    file_name = exc_trace_back.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] in line [{1}], and error message [{2}]".format(file_name,exc_trace_back.tb_lineno,str(error))
    return error_message
    
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)
        
    def __str__(self):
        return self.error_message
    
    
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as error:
        logging.info("Divide by 0 error")
        raise CustomException(error,sys)