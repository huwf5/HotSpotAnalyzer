from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self,status,message,data=None,code=None,headers=None,content_type=None,**kwargs):
        standard_response = {
            "message": message,
        }
        if data:
            standard_response["graph"] = data
        else:
            standard_response["graph"] = []
        if code:
            standard_response["code"] = code
        standard_response.update(kwargs)
        super().__init__(data=standard_response, status=status, headers=headers, content_type=content_type)
