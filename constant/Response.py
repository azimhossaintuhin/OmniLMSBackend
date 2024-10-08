from typing import Union, Any
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST


# Success Response 
def SuccessResponse(key:str, data:Union[list ,dict ,str]) -> Response :
    return Response({key: data, "status": True}, status=HTTP_200_OK)


#Error  Response 
def ErrorResponse(message:str) -> Response :
    return Response({"message":message ,  "status":False}, status =HTTP_400_BAD_REQUEST)