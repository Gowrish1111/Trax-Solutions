from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import (
    Login,
    Student,
    Trainer,
    Course,
    Enrollment,
    Assessment,
    Grade
)


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data['password']
        )
        return Login.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password']
            )

        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'