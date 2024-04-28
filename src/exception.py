import sys
from src.logger import logging

def error_message_detail(error):
    
    _,_,exc_trace_back = sys.exc_info()  # return (type, value, traceback)
    file_name = exc_trace_back.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] in line [{1}], and error message [{2}]".format(file_name,exc_trace_back.tb_lineno,str(error))
    return error_message
    
class CustomException(Exception):
    def __init__(self,error_message):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message)
        
    def __str__(self):
        return self.error_message
                    
    
if __name__ == "__main__":
    logging.info('Custom exception module imported')