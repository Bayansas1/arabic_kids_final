
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, WordImageMatchViewSet, LetterChoiceViewSet,
    UserAnswerViewSet, UserSkillViewSet,
    RegisterUserView, VerifyAnswerView, GetQuestionView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'word-matches', WordImageMatchViewSet)
router.register(r'letter-choices', LetterChoiceViewSet)
router.register(r'user-answers', UserAnswerViewSet, basename="useranswer")
router.register(r'user-skills', UserSkillViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # التسجيل والتحقق من الأسئلة
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('games/verify-answer/', VerifyAnswerView.as_view(), name='verify-answer'),
    path('games/get-question/<str:question_type>/', GetQuestionView.as_view(), name='get-question'),
    path('games/get-question/<str:question_type>/<int:question_id>/', GetQuestionView.as_view(), name='get-question-id'),
]
