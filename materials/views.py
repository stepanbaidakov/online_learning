from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from rest_framework import viewsets, generics
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):

        if self.action == "retrieve":
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "update":
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "partial_update":
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        elif self.action == "create":
            self.permission_classes = [~IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.groups.filter(name='moderator').exists():
                return Course.objects.all()
            else:
                courses =[]
                for course in Course.objects.all():
                    if course.owner == self.request.user:
                        courses.append(course)
                return courses
        else:
            return Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        else:
            lessons = []
            for lesson in Lesson.objects.all():
                if lesson.owner == self.request.user:
                    lessons.append(lessons)
            return lessons


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
