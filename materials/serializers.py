from materials.models import Course, Lesson
from rest_framework import serializers
from .validators import VideoValidator
from .models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator()]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "lessons_count", "lessons", "subscription")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        user = obj.owner
        course = obj
        subs_item = Subscription.objects.filter(course=course, user=user)
        return subs_item.exists()
