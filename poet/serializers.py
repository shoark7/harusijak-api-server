from rest_framework import serializers
from rest_framework import validators

from .models import Poet
from poem.models import Poem
from poem.serializers import PoemSerializer


class SimplePoetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ('id', 'nickname',)


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
        unique_check_fields = ['identifier', 'nickname', 'pk']
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
        fields = ['url', 'pk', 'identifier', 'password', 'nickname',
                  'image', 'description',

                  'poems_all_count', 'poems_displayed_count', 'subscribed_count',
                  'keeped_count', 'likes_count', ]
























# class PoetCreateSerializer(serializers.Serializer):
    # identifier = serializers.CharField()
    # password = serializers.CharField(style={'input_type': 'password'})
    # password_conf = serializers.CharField(style={'input_type': 'password'}, required=False)
    # nickname = serializers.CharField()
    # description = serializers.CharField(required=False)
    # image = serializers.ImageField(max_length=None, allow_empty_file=True,
                                  # required=False, use_url=True)

    # def create(self, validated_data):
        # try:
            # poet = Poet.objects.create_user(**validated_data)
        # except:
            # raise serializers.ValidationError("ID 또는 Nickname이 중복되거나 다른 필드에 문제가"
                                              # "있습니다. 다시 입력하세요.")
        # return poet
