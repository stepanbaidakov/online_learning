from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription

# Create your tests here.


class LessonsCreateTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.moderator_group = Group.objects.create(name="moderator")
        self.user = User.objects.create_user(email="test@email.com", password="123")
        self.course = Course.objects.create(title="test", description="test")
        self.client.force_authenticate(user=self.user)
        self.data = {
            "title": "beginning",
            "description": "course on python programming",
            "video_link": "https://youtube.com",
            "course": self.course.id,
        }

    def test_lesson_create(self):
        self.data = {
            "title": "beginning",
            "description": "course on python programming",
            "video_link": "https://youtube.com",
            "course": self.course.id,
        }
        response = self.client.post("/lessons/create/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "title": "beginning",
                "description": "course on python programming",
                "preview": None,
                "video_link": "https://youtube.com",
                "course": 1,
                "owner": 1,
            },
        )

    def test_lesson_create_invalid(self):
        self.data = {
            "title": "beginning",
            "description": "course on python programming",
            "video_link": "https://lajflajl.com",
            "course": self.course.id,
        }

        response = self.client.post("/lessons/create/", self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя использовать ссылки на сторонние образовательные платформы или личные сайты"
                ]
            },
        )

    def test_lesson_create_moderator(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="email@email.com", password="123")
        self.user.groups.add(self.moderator_group)
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/lessons/create/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})


class LessonsTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.moderator_group = Group.objects.create(name="moderator")
        self.user_owner = User.objects.create_user(email="test@email.com", password="123")
        self.user_moderator = User.objects.create_user(email="email@email.com", password="123")
        self.user_outsider = User.objects.create_user(email="email@gmail.com", password="123")
        self.user_moderator.groups.add(self.moderator_group)
        self.course = Course.objects.create(title="test", description="test")
        self.lesson = Lesson.objects.create(
            title="beginning",
            description="test",
            video_link="https://youtube.com",
            course=self.course,
            owner=self.user_owner,
        )

    def test_lesson_list_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": "beginning",
                        "description": "test",
                        "preview": None,
                        "video_link": "https://youtube.com",
                        "course": self.course.id,
                        "owner": self.user_owner.id,
                    }
                ],
            },
        )

    def test_lesson_list_outsider(self):
        self.client.force_authenticate(user=self.user_outsider)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"count": 0, "next": None, "previous": None, "results": []})

    def test_lesson_list_moderator(self):
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": "beginning",
                        "description": "test",
                        "preview": None,
                        "video_link": "https://youtube.com",
                        "course": self.course.id,
                        "owner": self.user_owner.id,
                    }
                ],
            },
        )

    def test_lesson_retrieve_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "title": "beginning",
                "description": "test",
                "preview": None,
                "video_link": "https://youtube.com",
                "course": self.course.id,
                "owner": self.user_owner.id,
            },
        )

    def test_lesson_retrieve_outsider(self):
        self.client.force_authenticate(user=self.user_outsider)
        response = self.client.get(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})

    def test_lesson_retrieve_moderator(self):
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "title": "beginning",
                "description": "test",
                "preview": None,
                "video_link": "https://youtube.com",
                "course": self.course.id,
                "owner": self.user_owner.id,
            },
        )

    def test_lesson_update_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        self.data_valid = {"description": "new desc"}
        response = self.client.patch(f"/lessons/{self.lesson.id}/update/", self.data_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "title": "beginning",
                "description": "new desc",
                "preview": None,
                "video_link": "https://youtube.com",
                "course": self.course.id,
                "owner": self.user_owner.id,
            },
        )
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_update_invalid(self):
        self.client.force_authenticate(user=self.user_owner)
        self.data_invalid = {
            "video_link": "https://lajflajl.com",
        }
        response = self.client.patch(f"/lessons/{self.lesson.id}/update/", self.data_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя использовать ссылки на сторонние образовательные платформы или личные сайты"
                ]
            },
        )

    def test_lesson_update_moderator(self):
        self.client.force_authenticate(user=self.user_moderator)
        self.data_valid = {"description": "new desc"}
        response = self.client.patch(f"/lessons/{self.lesson.id}/update/", self.data_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "title": "beginning",
                "description": "new desc",
                "preview": None,
                "video_link": "https://youtube.com",
                "course": self.course.id,
                "owner": self.user_owner.id,
            },
        )
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_update_outsider(self):
        self.client.force_authenticate(user=self.user_outsider)
        self.data_valid = {"description": "new desc"}
        response = self.client.patch(f"/lessons/{self.lesson.id}/update/", self.data_valid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})

    def test_lesson_destroy_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(f"/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_destroy_outsider(self):
        self.client.force_authenticate(user=self.user_outsider)
        response = self.client.delete(f"/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_destroy_moderator(self):
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.delete(f"/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionsTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="test@email.com", password="123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="test", description="test")
        self.data = {"user": self.user.id, "course": self.course.id}

    def test_subscribe(self):
        response = self.client.post("/subs/", self.data)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        self.assertTrue(Subscription.objects.filter(user=self.user).exists())

    def test_unsubscribe(self):
        self.client.post("/subs/", self.data)
        response = self.client.post("/subs/", self.data)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        self.assertFalse(Subscription.objects.filter(user=self.user).exists())
