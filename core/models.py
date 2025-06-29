from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class WordImageMatch(models.Model):
    word = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='image/')

class LetterChoice(models.Model):
    question_text = models.CharField(max_length=200)
    correct_letter = models.CharField(max_length=1)
    choices = models.JSONField()  # {"A": "أ", "B": "ب", "C": "ت"}
    letter = models.CharField(max_length=1,null=True,blank=True)  # ← الحرف المستهدف مثل: "أ"


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)  # مثل: "الحروف", "الكلمات"
    p_know = models.FloatField(default=0.1)  # احتمالية المعرفة الحالية
    p_transit = models.FloatField(default=0.3)  # احتمالية التعلم بعد محاولة ناجحة
    p_guess = models.FloatField(default=0.2)
    p_slip = models.FloatField(default=0.1)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50)  # "word" أو "letter"
    question_id = models.IntegerField()
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
