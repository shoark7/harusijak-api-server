from rest_framework import serializers, validators

from .models import Poet
from poem.models import Poem


class SimplePoetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poet
        fields = ('url', 'id', 'nickname', 'image')


# class SimplePoetSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = Poet
        # fields = ('id', 'nickname',)


class BasePoetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poet
        fields = ['url', 'pk', 'identifier', 'password', 'nickname',
                  'image', 'description',]


class PoetSerializer(BasePoetSerializer):
    poems_all_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    poems_displayed_count = serializers.SerializerMethodField()
    subscribed_count = serializers.SerializerMethodField()
    keeped_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(PoetSerializer, self).__init__(*args, **kwargs)
        # Find UniqueValidator and set custom message
        unique_check_fields = ['identifier', 'nickname', 'pk',]
        unique_check_messages = ['해당 ID는 이미 존재합니다.', '해당 필명은 이미 존재합니다.',
                                '개인의 고유 PK는 변경할 수 없습니다.',]

        for field, message in zip(unique_check_fields, unique_check_messages):
            for validator in self.fields[field].validators:
                if isinstance(validator, validators.UniqueValidator):
                    validator.message = (message)

    def get_poems_all_count(self, obj):
        return Poem.objects.filter(writer=obj).count()

    def get_poems_displayed_count(self, obj):
        return Poem.objects.filter(writer=obj, displayed=True).count()

    def get_likes_count(self, obj):
        return sum(poem.likes for poem in Poem.objects.filter(writer=obj, displayed=True))

    def get_subscribed_count(self, obj):
        return obj.subscribed_by.all().count()

    def get_keeped_count(self, obj):
        return sum(poem.keeped_by.count() for poem in obj.poems.all())


    class Meta:
        model = Poet
        fields = ['url', 'pk', 'identifier', 'nickname', 'password',
                  'image', 'description',

                  'poems_all_count', 'poems_displayed_count', 'subscribed_count',
                  'keeped_count', 'likes_count', ]
