from drf_yasg import openapi
from ..models import ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_USER


def api_response_schema(data_schema=None, code_schema=None):
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(
                type=openapi.TYPE_STRING, description="response message"
            ),
            "graph": data_schema,
            "code": code_schema,
        },
    )


emailList_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "emailList": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
        )
    },
)

role_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Role ID"),
        "role": openapi.Schema(
            type=openapi.TYPE_STRING, enum=[ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_USER]
        ),
    },
)

user_schema = waitinglist_user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="username of the user"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description="email of the user",
        ),
        "role": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="the primary key of the role"
        ),
    },
)
user_get_profile_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="username of the user"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description="email of the user",
        ),
        "role": openapi.Schema(
            type=openapi.TYPE_STRING, enum=[ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_USER]
        ),
    },
)

user_update_profile_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING, description="username of the user"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="password of the user"
        ),
    },
    required=["email"],
)


get_waitinglist_users_api_response_schema = api_response_schema(
    data_schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=waitinglist_user_schema)
)

get_userList_api_response_schema = api_response_schema(
    data_schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=user_schema)
)

get_roleList_api_response_schema = api_response_schema(
    data_schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=role_schema)
)

emailTag_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Email tag ID"),
        "email_format": openapi.Schema(
            type=openapi.TYPE_STRING, description="Email format"
        ),
        "email_tag": openapi.Schema(type=openapi.TYPE_STRING, description="Email tag"),
    },
)
delete_emailTag_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email_format": openapi.Schema(
            type=openapi.TYPE_STRING, description="Email format"
        ),
        "email_tag": openapi.Schema(type=openapi.TYPE_STRING, description="Email tag"),
    },
)
get_emailTagList_api_response_schema = api_response_schema(
    data_schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=emailTag_schema)
)

email_format_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "format": openapi.Schema(type=openapi.TYPE_STRING, description="Email format"),
    },
)
whiteList_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "format": openapi.Schema(type=openapi.TYPE_STRING, description="Email format"),
        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is active"),
    },
)

get_whiteList_api_response_schema = api_response_schema(
    data_schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=whiteList_schema)
)
