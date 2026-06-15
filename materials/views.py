from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Subscription
from rest_framework import viewsets, generics
from .serializers import CourseSerializer, LessonSerializer, CourseListSerializer
from .permissions import IsModerator, IsOwner
from .paginators import MyPaginator
from services import update_needed_check
# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = MyPaginator

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        return CourseSerializer

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

            return Course.objects.filter(owner=self.request.user)
        else:
            return Course.objects.all()

    def perform_update(self, serializer):
        course = self.get_object()
        update_needed_check(course)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MyPaginator
    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        update_needed_check(lesson.course)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class ManageSubscriptionView(APIView):

    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        course_id = self.request.data.get("course")

        subs_item = Subscription.objects.filter(course_id=course_id, user_id=user_id)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user_id=user_id, course_id=course_id)
            message = 'подписка добавлена'

        return Response({"message": message})
