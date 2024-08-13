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