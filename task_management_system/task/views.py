from rest_framework.views import APIView
from serializers.customResponse import ResponseSerializer
from task.serializers import TaskSerializer, TaskResponseSerializer
from common import common_messages as commonMsg

class TaskView(APIView):

	def post(self, request):
		try:
			# as request data is immutable, have to copy it
			postData = request.data.copy()
			taskSerializer = TaskSerializer(
				data = postData,
				context = {
					'mode': 'add',
				},
				# partial = True #using this to avoid model fields validations and handling based on mode: add/update
			)

			if taskSerializer.is_valid(raise_exception=True):
				task = taskSerializer.save().__dict__
				
				if not task['id']:
					return ResponseSerializer.apiResponseFormat(status=False, msg=commonMsg.UNABLE_TO_SAVE, data=postData)
				
				# returning task id
				postData['task_id'] = task['id']
				
				return ResponseSerializer.apiResponseFormat(status=True, msg=commonMsg.SAVED_SUCCESSFULLY, data=postData)

		except Exception as ex:
			print('view: ', ex)
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])