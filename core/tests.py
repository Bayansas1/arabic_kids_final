# question_logic.py
import random
from .models import LetterChoice

def generate_new_letter_question(target_letter, all_letters, wrong_attempt):
    if wrong_attempt == target_letter:
        raise ValueError("الحرف الخطأ لا يمكن أن يكون نفس الحرف الصحيح.")

    available_choices = [l for l in all_letters if l != target_letter and l != wrong_attempt]
    if len(available_choices) < 3:
        raise ValueError("عدد الحروف المتبقية غير كافٍ.")

    additional_choices = random.sample(available_choices, 3)
    all_choices = additional_choices + [target_letter, wrong_attempt]
    random.shuffle(all_choices)

    choices_dict = {str(i+1): letter for i, letter in enumerate(all_choices)}
    correct_key = next(k for k, v in choices_dict.items() if v == target_letter)

    question = LetterChoice.objects.create(
        question_text=f"اختر الحرف الصحيح المرتبط بـ '{target_letter}'",
        correct_letter=correct_key,
        choices=choices_dict,
        letter=target_letter
    )
    return question

# Create your tests here.
