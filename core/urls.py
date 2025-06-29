
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'word-matches', WordImageMatchViewSet)
router.register(r'letter-choices', LetterChoiceViewSet)
router.register(r'user-answers', UserAnswerViewSet, basename="useranswer")
router.register(r'user-skills', UserSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]


from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_user),
    path('api/letter-question/', views.get_letter_question),
    path('api/matching-exercise/', views.get_word_image_exercise),
    path('api/save-answer/', views.save_user_answer),
]

# core/urls.py


