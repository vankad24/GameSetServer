class BaseResponse:
	def __init__(self, success=True, error=None):
		self.success = success
		self.error = error

	def to_dict(self):
		return {"success":self.success,"error":None if self.error is None else self.error.to_dict()}