import random
from .models import LetterChoice, WordImageMatch


def generate_new_letter_question(target_letter, all_letters, wrong_attempt=None):
    # تأكد أن الحرف الخطأ ليس نفس الحرف الصحيح
    if wrong_attempt == target_letter:
        wrong_attempt = None  # تجاهله إن كان مطابقًا

    # استبعد الحرف الصحيح والخطأ من قائمة الحروف
    available_choices = [l for l in all_letters if l != target_letter]
    if wrong_attempt:
        available_choices = [l for l in available_choices if l != wrong_attempt]

    # تأكد أن عدد الحروف المتاحة يكفي
    if len(available_choices) < 3:
        raise ValueError("عدد الحروف المتبقية غير كافٍ لاختيار ثلاثة اختيارات إضافية.")

    # اختر 3 حروف عشوائية
    additional_choices = random.sample(available_choices, 3)

    # أنشئ القائمة النهائية من الخيارات
    all_choices = additional_choices + [target_letter]
    if wrong_attempt:
        all_choices.append(wrong_attempt)

    random.shuffle(all_choices)

    # أنشئ القاموس بالشكل {'1': 'أ', '2': 'ب', ...}
    choices_dict = {str(i + 1): letter for i, letter in enumerate(all_choices)}

    # المفتاح الصحيح هو الذي يحتوي على الحرف الصحيح
    correct_key = next(k for k, v in choices_dict.items() if v == target_letter)

    # إنشاء السؤال في قاعدة البيانات
    question = LetterChoice.objects.create(
        question_text=f"اختر الحرف الصحيح المرتبط بـ '{target_letter}'",
        correct_letter=correct_key,
        choices=choices_dict,
        letter=target_letter
    )

    return question


def generate_new_matching_exercise(previous_words, category):
    arabic_names = {
        "fruits": "الفواكه",
        "vegetables": "الخضار",
        "animals": "الحيوانات",
        "body": "أجزاء الجسم"
    }

    # جميع الكلمات في التصنيف
    all_items = WordImageMatch.objects.filter(category=category)

    if all_items.count() < 3:
        return {
            "exercise": None,
            "message": "لا يوجد عدد كافٍ من الكلمات لبدء هذا المستوى.",
            "level_completed": True
        }

    # استبعاد الكلمات التي استخدمها الطالب سابقًا
    new_candidates = all_items.exclude(word__in=previous_words)

    if new_candidates.count() < 2:
        return {
            "exercise": None,
            "message": f"تم إنهاء مستوى {arabic_names.get(category, category)}!",
            "level_completed": True
        }

    # اختيار كلمتين جديدتين
    selected_new = random.sample(list(new_candidates), 2)

    # اختيار كلمة قديمة واحدة عشوائية من السابقين
    old_word = random.choice(previous_words)
    old_item = all_items.filter(word=old_word).first()

    if not old_item:
        raise ValueError("الكلمة السابقة غير موجودة في قاعدة البيانات.")

    # دمج الكلمات الثلاث وتوزيعها عشوائيًا
    selected = selected_new + [old_item]
    random.shuffle(selected)

    # بناء التمرين بصيغة JSON
    exercise_data = [
        {
            "word": item.word,
            "image_url": item.image_url.url  # تم تصحيح المسار هنا
        }
        for item in selected
    ]

    return {
        "exercise": exercise_data,
        "message": "تمرين جديد",
        "level_completed": False
    }
