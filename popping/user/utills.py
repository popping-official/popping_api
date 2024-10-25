from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
    
def generate_auth_code(length=8):
    
    import random, string
    
    """_summary_
        영문 대소문자 + 숫자 조합을 통해 랜덤으로 8글자 문자열 코드를 반환하는 함수
    """
    characters = string.ascii_letters + string.digits 
    code = ''.join(random.choice(characters) for _ in range(length))
    return code



def send_auth_email(target_email: list, subject: str, purpose_message: str):
    
    auth_code = generate_auth_code()

    # HTML 템플릿을 렌더링
    html_content = render_to_string('auth-mail.html', {'purpose_message' : purpose_message, 'auth_code': auth_code})
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, 'app.popping@gmail.com', target_email)
    # HTML 첨부
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    return auth_code



def send_link_email(target_email: list, subject: str, purpose_message: str, link: str):
    
    # HTML 템플릿을 렌더링
    html_content = render_to_string('link-mail.html', {'purpose_message' : purpose_message, 'link': link})
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, 'app.popping@gmail.com', target_email)
    # HTML 첨부
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    return True


def change_point(user_instance, is_increase, point, type_num):
    """_summary_
    Args:
        user_instance (_user_): 유저 인스턴스
        is_increase (bool): 증가(적립) = true / 감소(사용) = false
        point (integer): 증감된 포인트
        type_num (integer): 
            1. 신규 회원 적립
            2. 구매 적립
            3. 리뷰 적립
            4. 이벤트 적립
            5. 상품구매 사용
    """
    from .models import PointChange, PointHistory
    
    point_history = PointHistory.objects.filter(userFK=user_instance).last()
    if point_history:
        before_change_point = point_history.currentPoint
    else:
        before_change_point = 0

    point_history = PointHistory.objects.create(
        userFK = user_instance,
        PointChangeFK = PointChange.objects.get(pk=type_num),
    )
    if is_increase:
        # 증가 : 적립
        point_history.increasePoint = point
        before_change_point += point
    else:
        # 감소 : 사용
        PointHistory.decreasePoint = point
        before_change_point -= point
        
    point_history.currentPoint = before_change_point
        
    point_history.save()