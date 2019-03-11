from rest_framework import serializers

from .models import Poet
from poem.models import Poem
from poem.serializers import PoemSerializer


class SimplePoetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ('id', 'nickname',)


class PoetSerializer(serializers.HyperlinkedModelSerializer):
    poems = PoemSerializer(read_only=True, many=True)
    class Meta:
        model = Poet
        fields = ['url', 'pk', 'nickname', 'image', 'description', 'poems',]


class PoetCreateSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    password_conf = serializers.CharField(style={'input_type': 'password'}, required=False)
    nickname = serializers.CharField()
    description = serializers.CharField(required=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=True,
                                  required=False, use_url=True)

    def create(self, validated_data):
        try:
            poet = Poet.objects.create_user(**validated_data)
        except:
            raise serializers.ValidationError("ID 또는 Nickname이 중복되거나 다른 필드에 문제가"
                                              "있습니다. 다시 입력하세요.")
        return poet
