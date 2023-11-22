from django.shortcuts import render,redirect
from .utils import send_email_to_clint,send_email_with_attachment
from django.conf import settings
# Create your views here.


def send_email(request):
    #send_email_to_clint()
    return render(request,'email.html')

def seen_email(request):
    subject = "This email is From Django server with Attachment"
    message = "Hey please find this attach file with this email"
    recipient_list = ["webc998@gmail.com"]
    file_path = f"{settings.BASE_DIR}/main.html"
    send_email_with_attachment(subject,message,recipient_list,file_path)
    return redirect('email')