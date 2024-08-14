from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


def envbuild():
    """_summary_
        .env 파일을 통해 환경변수에 접근하기 위해 빌드해주는 함수
    """
    import environ
    env = environ.Env()

    env_path = settings.BASE_DIR / ".env"

    if env_path.exists():
        with env_path.open("rt", encoding="utf8") as f:
            env.read_env(f)

    return env


def error_response(code, model_name=None, field_name=None):
    """
    에러 코드에 따른 메시지, HTTP 상태 코드, 예외를 처리하는 함수

    :param code: 에러 코드 (디폴트는 1)
    :return: Django REST Framework Response 객체 또는 예외 발생
    """

    # 에러 코드와 상태 코드, 예외, 메시지를 매핑
    error_mapping = {
        1: {
            "http_status": status.HTTP_401_UNAUTHORIZED,
            "exception": None,
            "message": "Unauthorized access."
            },
        2: {
            "http_status": status.HTTP_400_BAD_REQUEST,
            "exception": ObjectDoesNotExist,
            "message": f"{model_name} Object does not exist."
            },
        3: {
            "http_status": status.HTTP_400_BAD_REQUEST,
            "exception": None,
            "message": f"{field_name}은(는) 필수 필드입니다."
            },
        }

    # 매핑된 상태 코드, 예외, 메시지 가져오기
    error_info = error_mapping.get(code, {
        "http_status": status.HTTP_400_BAD_REQUEST,
        "exception": None,
        "message": "An error occurred."
        })


    return Response({
        "status": {
            "name": "error",
            "code": code
            },
        "message": error_info["message"]
        }, status=error_info["http_status"])