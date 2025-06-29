
# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .bkt import update_bkt

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# core/views.py
class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer

class WordImageMatchViewSet(viewsets.ModelViewSet):
    queryset = WordImageMatch.objects.all()
    serializer_class = WordImageMatchSerializer

class LetterChoiceViewSet(viewsets.ModelViewSet):
    queryset = LetterChoice.objects.all()
    serializer_class = LetterChoiceSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer


    @action(detail=False, methods=['post'])
    def submit(self, request):
        user_id = request.data.get('user_id')
        question_type = request.data.get('question_type')
        question_id = request.data.get('question_id')
        is_correct = request.data.get('is_correct')

        user = User.objects.get(id=user_id)
        UserAnswer.objects.create(user=user, question_type=question_type,
                                  question_id=question_id, is_correct=is_correct)

        # BKT update
        skill_name = "الحروف" if question_type == "letter" else "الكلمات"
        skill, created = UserSkill.objects.get_or_create(user=user, skill_name=skill_name)

        new_p_know = update_bkt(skill.p_know, skill.p_transit, skill.p_guess, skill.p_slip, is_correct)
        skill.p_know = new_p_know
        skill.save()

        return Response({"new_p_know": new_p_know}, status=status.HTTP_200_OK)


from core.random import generate_new_letter_question
from core.models import UserAnswer, UserSkill

def handle_student_answer(user, letter, is_correct):
    if not is_correct:
        all_letters = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
        new_question = generate_new_letter_question(letter, all_letters)
        return new_question
    return None


from rest_framework.decorators import api_view
from .models import LetterChoice



from  .models import WordImageMatch
from core.random import generate_new_matching_exercise


@api_view(['POST'])
def generate_matching_exercise_api(request):
    data = request.data
    previous_words = data.get('previous_words', [])
    category = data.get('category')

    result = generate_new_matching_exercise(previous_words, category)
    return Response(result)


@api_view(['POST'])
def register_user(request):
    name = request.data.get('name')
    age = request.data.get('age')
    if not name or not age:
        return Response({'error': 'الاسم والعمر مطلوبان'}, status=400)
    user = User.objects.create(name=name, age=age)
    return Response(UserSerializer(user).data)


@api_view(['POST'])
def save_user_answer(request):
    serializer = UserAnswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'تم الحفظ بنجاح'})
    return Response(serializer.errors, status=400)

