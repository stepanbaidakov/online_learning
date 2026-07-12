from materials.views import CourseViewSet, LessonListAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView, LessonCreateAPIView, ManageSubscriptionView
from rest_framework import routers
from django.urls import path

app_name = "materials"

router = routers.DefaultRouter()
router.register('courses', CourseViewSet, 'courses')

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("subs/", ManageSubscriptionView.as_view(), name="subs"),
] + router.urls