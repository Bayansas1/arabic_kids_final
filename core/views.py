
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    User, LetterChoice, WordImageMatch, UserAnswer, UserSkill
)
from .serializers import (
    UserSerializer, LetterChoiceSerializer, WordImageMatchSerializer, UserAnswerSerializer, UserSkillSerializer
)
from core.utils.bkt import BKTModel
from core.random import generate_new_letter_question, generate_new_matching_exercise


# ========== ViewSets ==========
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        is_correct = request.data.get('is_correct') in ["true", True, "1", 1]

        user = get_object_or_404(User, id=user_id)

        # تخزين الإجابة
        letter = request.data.get("letter")
        UserAnswer.objects.create(
            user=user,
            question_type=question_type,
            question_id=question_id,
            is_correct=is_correct,
            letter=letter if question_type == "letter" else None
        )

        # المهارة وتحديث BKT
        skill_name = "الحروف" if question_type == "letter" else "الكلمات"
        skill, _ = UserSkill.objects.get_or_create(
            user=user,
            skill_name=skill_name,
            defaults={"p_know": 0.2, "p_transit": 0.3, "p_guess": 0.2, "p_slip": 0.1}
        )

        bkt = BKTModel(skill.p_know, skill.p_transit, skill.p_guess, skill.p_slip)
        skill.p_know = bkt.update(is_correct)
        skill.save()

        next_action = "repeat" if skill.p_know < 0.7 else "next"
        next_question = None

        if question_type == "letter":
            current_question = LetterChoice.objects.get(id=question_id)
            wrong_letter = None
            if not is_correct:
                last_answer = UserAnswer.objects.filter(
                    user=user, question_type="letter", question_id=question_id
                ).last()
                wrong_letter = getattr(last_answer, 'letter', None)

            try:
                new_q = generate_new_letter_question(
                    target_letter=current_question.letter,
                    all_letters=[
                        'أ','ب','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ظ',
                        'ع','غ','ف','ق','ك','ل','م','ن','هـ','و','ي'
                    ],
                    wrong_attempt=wrong_letter or 'ب'
                )
                next_question = {
                    "question_id": new_q.id,
                    "type": "multiple_choice",
                    "content": {
                        "prompt": new_q.question_text,
                        "choices": new_q.choices,
                        "correct_answer": new_q.correct_letter
                    }
                }
            except Exception as e:
                next_question = {"error": str(e)}

        elif question_type == "match":
            previous_ids = UserAnswer.objects.filter(user=user, question_type="match").values_list('question_id', flat=True)
            previous_words = WordImageMatch.objects.filter(id__in=previous_ids).values_list('word', flat=True)
            exercise = generate_new_matching_exercise(previous_words=list(previous_words), category="animals")

            next_question = {
                "type": "matching",
                **exercise
            }

        return Response({
            "skill": skill_name,
            "updated_p_l": round(skill.p_know, 3),
            "next_action": next_action,
            "next_question": next_question
        }, status=status.HTTP_200_OK)


# ========== APIView Classes ==========
class RegisterUserView(APIView):
    def post(self, request):
        name = request.data.get('name')
        age = request.data.get('age')

        if not name or age is None:
            return Response({'error': 'الاسم والعمر مطلوبان'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            age = int(age)
        except ValueError:
            return Response({'error': 'العمر يجب أن يكون رقمًا'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(name=name, age=age)
        return Response({'id': user.id, 'name': user.name, 'age': user.age}, status=status.HTTP_201_CREATED)


class VerifyAnswerView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        question_type = request.data.get('question_type')
        question_id = request.data.get('question_id')
        user_answer = request.data.get('user_answer')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'المستخدم غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        is_correct = False
        selected_letter = None

        if question_type == 'letter':
            try:
                question = LetterChoice.objects.get(id=question_id)
                is_correct = (user_answer == question.correct_letter)
                selected_letter = question.letter
            except LetterChoice.DoesNotExist:
                return Response({'error': 'سؤال الحرف غير موجود'}, status=404)

            UserAnswer.objects.create(
                user=user,
                question_type='letter',
                question_id=question_id,
                is_correct=is_correct,
                letter=selected_letter
            )

            if not is_correct:
                all_letters = [chr(code) for code in range(0x0627, 0x064A + 1)]
                new_question = generate_new_letter_question(
                    target_letter=question.letter,
                    all_letters=all_letters,
                    wrong_attempt=user_answer
                )
                return Response({
                    'is_correct': False,
                    'new_question': {
                        'id': new_question.id,
                        'question_text': new_question.question_text,
                        'choices': new_question.choices,
                        'letter': new_question.letter
                    }
                }, status=200)

        elif question_type == 'match':
            try:
                question = WordImageMatch.objects.get(id=question_id)
                correct_url = request.build_absolute_uri(question.image_url.url)
                is_correct = (user_answer == correct_url)
            except WordImageMatch.DoesNotExist:
                return Response({'error': 'سؤال المطابقة غير موجود'}, status=404)

            UserAnswer.objects.create(
                user=user,
                question_type='match',
                question_id=question_id,
                is_correct=is_correct
            )

        else:
            return Response({'error': 'نوع السؤال غير صالح'}, status=400)

        return Response({'is_correct': is_correct}, status=200)
class GetQuestionView(APIView):
      def get(self, request, question_type, question_id=None):
        if question_type == 'letter':
            try:
                q = LetterChoice.objects.get(id=question_id)
                return Response({
                    'id': q.id,
                    'type': 'letter',
                    'question_text': q.question_text,
                    'letter': q.letter,
                    'choices': q.choices
                })
            except LetterChoice.DoesNotExist:
                return Response({'error': 'سؤال الحرف غير موجود'}, status=404)

        elif question_type == 'match':
            previous_words = request.query_params.getlist('previous_words')
            category = request.query_params.get('category', 'fruits')
            result = generate_new_matching_exercise(previous_words, category)

            if result['level_completed']:
                return Response(result, status=200)

            return Response({
                'type': 'match',
                'exercise': result['exercise'],
                'message': result['message']
            })

        return Response({'error': 'نوع السؤال غير صالح'}, status=400)