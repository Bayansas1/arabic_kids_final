"""
URL configuration for arabic_kids_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Arabi_kids_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from core.views import RegisterUserView ,VerifyAnswerView ,GetQuestionView
from django.urls import path




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/users/', RegisterUserView.as_view(), name='register-user'),
    path('api/games/verify-answer/', VerifyAnswerView.as_view(), name='verify-answer'),
    path('api/games/get-question/<str:question_type>/', GetQuestionView.as_view(), name='get-question'),
    path('api/games/get-question/<str:question_type>/<int:question_id>/', GetQuestionView.as_view(), name='get-question-id'),
]

# دعم عرض الصور من media/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




 

