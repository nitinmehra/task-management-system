from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from serializers.customResponse import ResponseSerializer
from task.serializers import TaskSerializer, TaskResponseSerializer
from common import common_messages as commonMsg
from task.models import Task
from rest_framework import status

class TaskView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]

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

			# validating data, if success enters in condition else raise the exception
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

			# checking whether the task exist or not
			try:
				taskInstance = Task.objects.get(id=taskId)
			except Task.DoesNotExist:
				return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})

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
		
	# get task details and task list
	def get(self, request, *args, **kwargs):
		try:
			taskId = kwargs.get('id', None)
			# taskData = []
			if taskId:

				# checking whether the task exist or not
				try:
					taskInstance = Task.objects.get(id=taskId)
				except Task.DoesNotExist:
					return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})

				taskData = TaskResponseSerializer(taskInstance).data
					
			else:
				# fetching all the records
				taskInstance = Task.objects.all().order_by('-created_at')
			
				if taskInstance is None:
					return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})
				
				taskData = TaskResponseSerializer(taskInstance, many=True).data

			return ResponseSerializer.apiResponseFormat(True, data=taskData)

		except Exception as ex:
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])
		
	# delete task
	def delete(self, request, *args, **kwargs):
		try:
			taskId = kwargs.get('id', None)
			
			if taskId:
				# checking whether the task exist or not
				try:
					taskInstance = Task.objects.get(id=taskId)
				except Task.DoesNotExist:
					return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data={})

				# if task exist delete it
				res = Task.objects.get(id=taskId).delete()
				if res:
					return ResponseSerializer.apiResponseFormat(status=True, msg=commonMsg.DELETED_SUCCESSFULLY, data={})
				else:
					return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.UNABLE_TO_DELETE, data=None)
			
			else:
				return ResponseSerializer.apiResponseFormat(status=False, code=status.HTTP_400_BAD_REQUEST, msg=commonMsg.INVALID_ID.format('task'), data=None)
					
		except Exception as ex:
			exception = ResponseSerializer.handleExceptions(ex)
			return ResponseSerializer.apiResponseFormat(False, exception['code'], exception['errorMsg'], [])