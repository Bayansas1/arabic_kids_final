
import random
from .models import LetterChoice

def generate_new_letter_question(target_letter, all_letters, wrong_attempt):
    # تأكد أن الحرف الخطأ ليس نفس الحرف الصحيح
    if wrong_attempt == target_letter:
        raise ValueError("الحرف الخطأ لا يمكن أن يكون نفس الحرف الصحيح.")

    # أنشئ مجموعة الحروف الممكنة بعد إزالة الحرف الصحيح والخطأ المستخدم مسبقًا
    available_choices = [l for l in all_letters if l != target_letter and l != wrong_attempt]

    # نحتاج فقط إلى 3 حروف إضافية (لأن لدينا الصحيح + الخطأ بالفعل = 2)
    if len(available_choices) < 3:
        raise ValueError("عدد الحروف المتبقية غير كافٍ لاختيار ثلاثة اختيارات إضافية.")

    # اختر 3 اختيارات عشوائية أخرى
    additional_choices = random.sample(available_choices, 3)

    # أنشئ القائمة النهائية (الصحيح + الخطأ المختار + 3 أخرى)
    all_choices = additional_choices + [target_letter, wrong_attempt]
    random.shuffle(all_choices)

    # أنشئ القاموس بالشكل {'1': 'أ', '2': 'ب', ...}
    choices_dict = {str(i+1): letter for i, letter in enumerate(all_choices)}
    
    # المفتاح الصحيح هو المفتاح الذي يحتوي على الحرف الصحيح
    correct_key = next(k for k, v in choices_dict.items() if v == target_letter)

    # إنشاء السؤال في قاعدة البيانات
    question = LetterChoice.objects.create(
        question_text=f"اختر الحرف الصحيح المرتبط بـ '{target_letter}'",
        correct_letter=correct_key,
        choices=choices_dict,
        letter=target_letter
    )

    return question


import random
from .models import WordImageMatch


def generate_new_matching_exercise(previous_words, category):
    arabic_names = {
        "fruits": "الفواكه",
        "vegetables": "الخضار",
        "animals": "الحيوانات",
        "body": "أجزاء الجسم"
    }

    # جميع الكلمات في هذا التصنيف
    all_items = WordImageMatch.objects.filter(category=category)

    if all_items.count() < 3:
        return {
            "exercise": None,
            "message": "لا يوجد عدد كافٍ من الكلمات لبدء هذا المستوى.",
            "level_completed": True
        }

    # استبعاد الكلمات السابقة
    new_candidates = all_items.exclude(word__in=previous_words)

    if new_candidates.count() < 2:
        # لم يتبقَ كلمتان جديدتان -> تم إنهاء المستوى
        return {
            "exercise": None,
            "message": f" تم إنهاء مستوى {arabic_names.get(category, category)}!",
            "level_completed": True
        }

    # اختيار كلمتين جديدتين
    selected_new = random.sample(list(new_candidates), 2)

    # اختيار كلمة من التمرين السابق (عشوائيًا)
    old_word = random.choice(previous_words)
    old_item = all_items.filter(word=old_word).first()

    # تأكيد أن الكلمة السابقة موجودة
    if not old_item:
        raise ValueError("الكلمة السابقة غير موجودة في قاعدة البيانات.")

    # دمجهم معًا
    selected = selected_new + [old_item]
    random.shuffle(selected)

    # بناء التمرين
    exercise_data = [
        {
            "word": item.word,
            "image_url": f"/media/{item.image_path}"
        }
        for item in selected
    ]

    return {
        "exercise": exercise_data,
        "message": "تمرين جديد ",
        "level_completed": False
    }
