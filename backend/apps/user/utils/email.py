import random
import string
from application.settings import EMAIL_VALIDATION_TIME_LIMIT, EMAIL_HOST_USER
from django.core.mail import send_mail


def generate_verify_code(length=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_verify_email(email, username, verify_code):
    subject = "热点分析系统注册验证"
    message = (
        f"尊敬的{username}，您好！\n"
        f"    您的注册验证码为：{verify_code}。\n"
        f"    请在{EMAIL_VALIDATION_TIME_LIMIT}分钟内完成注册，注册完成后请联系管理员激活账号。\n"
        f"    感谢您的支持！\n"
        "热点分析系统团队"
    )
    email_from = f"热点分析系统<{EMAIL_HOST_USER}>"
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
