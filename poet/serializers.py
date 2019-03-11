from rest_framework import serializers

from .models import Poet
from poem.models import Poem
from poem.serializers import PoemSerializer


class SimplePoetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ('id', 'nickname',)


class PoetSerializer(serializers.HyperlinkedModelSerializer):
    poems_all_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    poems_displayed_count = serializers.SerializerMethodField()
    subscribed_count = serializers.SerializerMethodField()
    keeped_count = serializers.SerializerMethodField()

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
        # First block: model field
        # Second block: custom field
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
