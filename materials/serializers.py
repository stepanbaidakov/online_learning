from materials.models import Course, Lesson
from rest_framework import serializers
from .validators import VideoValidator
from .models import Subscription
from django.urls import reverse_lazy


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator()]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()
    pay = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lessons_count", "lessons", "subscription", "pay")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        user = obj.owner
        course = obj
        subs_item = Subscription.objects.filter(course=course, user=user)
        return subs_item.exists()

    def get_pay(self, obj):
        return reverse_lazy("users:payment-create", kwargs={"pk": obj.pk})


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lessons_count", "subscription")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        user = obj.owner
        course = obj
        subs_item = Subscription.objects.filter(course=course, user=user)
        return subs_item.exists()
