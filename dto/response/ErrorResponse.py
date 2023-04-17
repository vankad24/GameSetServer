from dto.response.ErrorDto import ErrorDto
from dto.response.BaseResponse import BaseResponse

class ErrorResponse(BaseResponse):
    def __init__(self, msg):
        super().__init__(False, ErrorDto(msg))