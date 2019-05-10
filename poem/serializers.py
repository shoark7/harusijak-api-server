from rest_framework import routers, serializers

from poet.models import Poet
from poet.serializers import SimplePoetSerializer
from .models import Poem


# class SimplePoetSerializer(serializers.HyperlinkedModelSerializer):
    # class Meta:
        # model = Poet
        # fields = ('url', 'id', 'nickname', 'image')


class PoemSerializer(serializers.HyperlinkedModelSerializer):
    writer = SimplePoetSerializer(required=False)
    subject = serializers.SerializerMethodField()
    written_date = serializers.SerializerMethodField()

    def get_written_date(self, obj):
        return obj.written_date.__str__()

    def get_subject(self, obj):
        return obj.written_date.subject.__str__()


    class Meta:
        model = Poem
        fields = ('url', 'id', 'title', 'content', 'writer', 'subject', 'written_date', 'align',
                  'written_time', 'displayed', 'likes', 'dislikes',)
        # 'subject' is needed
        # 'written_date' is needed
