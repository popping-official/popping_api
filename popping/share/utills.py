import random, string
from django.conf import settings


def generate_auth_code(length=8):
    """_summary_
        영문 대소문자 + 숫자 조합을 통해 랜덤으로 8글자 문자열 코드를 반환하는 함수
    """
    characters = string.ascii_letters + string.digits 
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


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