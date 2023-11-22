from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from models.views import *
from django.conf.urls.static import static
from django.conf import settings
from account.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('resipy/',resipy, name="resipy"),
    path('delete-resipy/<id>/', delete_resipy, name="delete_resipy"),
    path('update-resipy/<id>/', update_resipy, name="update_resipy"),
    path('login-page/', login_page, name="login"),
    path('logout-page/', logout_page, name="logout"),
    path('register-page/', register, name="register"),
    path('students/', set_students, name="students"),
    path('email-send/', send_email, name="email"),
    path('email-seen/', seen_email, name="email_seen"),

    #আমদা যেই স্টুডেন্ট এর লিংক এ ক্লিক করবে তার <student_id> টি লোকেশন এ চলে আসবে
    path('see_marks/<student_id>/', see_marks, name="see_marks"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()



