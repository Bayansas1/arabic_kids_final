
from rest_framework import serializers
from .models import User, WordImageMatch, LetterChoice, UserSkill, UserAnswer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WordImageMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordImageMatch
        fields = '__all__'

class LetterChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetterChoice
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
