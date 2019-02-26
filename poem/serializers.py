from rest_framework import routers, serializers

from poet.models import Poet
from .models import Poem


class SimplePoetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poet
        fields = ('url', 'id', 'nickname', 'image')


class PoemSerializer(serializers.HyperlinkedModelSerializer):
    writer = SimplePoetSerializer(required=False)
    class Meta:
        model = Poem
        fields = ('url', 'id', 'title', 'content', 'subject', 'writer', 'written_date',
                  'written_time', 'displayed', 'likes', 'dislikes',)
