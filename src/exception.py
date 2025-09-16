import sys

def error_messages(error,error_detail:sys):

    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_msg = f"Error occured in file name {file_name} in line {line_number} error message {error}"

    return error_msg


class CustomException(Exception):

    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = error_messages(error_message,error_detail=error_details)

    def __str__(self):
        return self.error_message
    
