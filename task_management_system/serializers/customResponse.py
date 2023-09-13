from rest_framework.exceptions import ErrorDetail, ValidationError
from common import common_messages as commonMsg
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import EmptyResultSet

class ResponseSerializer():

    def customValidationFormat(fieldName, msg, errorCode):
        return {
            fieldName:  [ErrorDetail(string=msg, code=errorCode)]
        }

    def handleExceptions(exception):
        response = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'errorMsg': commonMsg.SOMETHING_WENT_WRONG
        }
        
        if type(exception) == ValidationError:
            errorsList = exception.detail

            response['code'] = status.HTTP_400_BAD_REQUEST
            for field in errorsList:
                errorCode = errorsList[field][0].code
                if errorCode == 'required':
                    response['errorMsg'] = commonMsg.REQUIRED_FIELD.format(field_name = field)
                    return response
                elif errorCode == 'blank':
                    response['errorMsg'] = commonMsg.BLANK_FIELD.format(field_name = field)
                    return response
                elif errorCode == 'max_length':
                    response['errorMsg'] = field + ': ' + errorsList[field][0]
                    return response
                else:
                    response['errorMsg'] = errorsList[field][0]
                    return response
        elif type(exception) == EmptyResultSet:
            response['code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['errorMsg'] = str(exception)
            return response
        else:

            return response
    
    def apiResponseFormat(status=True, code=status.HTTP_200_OK, msg='', data=[]):
        return Response({
                'status': status,
                'code': code,
                'msg': msg,
                'data': data,
            },code)
    
    def dateValidationFormat(fieldName, msg, errorCode):
        return {
            fieldName:  [ErrorDetail(string=msg, code=errorCode)]
        }