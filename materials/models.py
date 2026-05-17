from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to="course_preview", blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_preview", blank=True, null=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title}-{self.title}"

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
