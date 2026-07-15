import re

from rest_framework import serializers


class VideoValidator:

    def __call__(self, attrs):
        pattern = r"youtube\.com"
        url = attrs.get("video_link")
        if url and not re.search(pattern, url):
            raise serializers.ValidationError(
                "Нельзя использовать ссылки на сторонние образовательные платформы или личные сайты"
            )
