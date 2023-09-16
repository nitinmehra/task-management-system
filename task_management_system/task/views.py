from rest_framework.views import APIView
from serializers.customResponse import ResponseSerializer
from task.serializers import TaskSerializer, TaskResponseSerializer
from common import common_messages as commonMsg
from task.models import Task
from rest_framework import status

class TaskView(APIView):

	# create task
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
				task = TaskResponseSerializer(taskSerializer.save()).data
				
				if not task['id']:
					return ResponseSerializer.apiResponseFormat(status=False, msg=commonMsg.UNABLE_TO_SAVE, data=postData)
				
				# returning task id
				postData['task_id'] = task['id']
				
				return ResponseSerializer.apiResponseFormat(status=True, msg=commonMsg.SAVED_SUCCESSFULLY, data=postData)

		except Exception as ex:
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])
	
	# update task
	def put(self, request, *args, **kwargs):
		try:
			# as request data is immutable, have to copy it
			postData = request.data.copy()
			taskId = kwargs.get('id')

			taskInstance = Task.objects.get(id=taskId)

			if not taskInstance:
				return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID, data=postData)

			taskSerializer = TaskSerializer(
				taskInstance,
				data = postData,
				context = {
					'mode': 'add',
				},
				# partial = True #using this to avoid model fields validations and handling based on mode: add/update
			)

			if taskSerializer.is_valid(raise_exception=True):
				taskSerializer.save()
				return ResponseSerializer.apiResponseFormat(True, msg=commonMsg.UPDATED_SUCCESSFULLY, data = [])

		except Exception as ex:
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])
		
	def get(self, request, *args, **kwargs):
		try:
			taskId = kwargs.get('id', None)
			# taskData = []
			if taskId:
				taskInstance = Task.objects.get(id=taskId)

				if taskInstance is None:
						return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})

				taskData = TaskResponseSerializer(taskInstance).data
					
			else:
				taskInstance = Task.objects.all().order_by('-created_at')
			
				if taskInstance is None:
					return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})
				
				taskData = TaskResponseSerializer(taskInstance, many=True).data

			return ResponseSerializer.apiResponseFormat(True, data=taskData)

		except Exception as ex:
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])
		