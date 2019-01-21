from rest_framework import routers, serializers, viewsets

from .models import Poet
from poem.serializers import PoemSerializer
from poem.models import Poem


class SimplePoetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poet
        fields = ('id', 'nickname',)


class PoetSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    nickname = serializers.CharField()
    description = serializers.CharField(required=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=True,
                                  required=False, use_url=True)
    poems = PoemSerializer(many=True)

    def update(self, instance, validated_data):
        instance.identifier = validated_data.get('identifier', instance.identifier)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.password = validated_data.get('password', instance.password)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        return instance


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
            raise serializers.ValidationError("문제가 있습니다. 정확히 정보를 입력해주십시오.")

        return poet


class PoetViewSet(viewsets.ModelViewSet):
    queryset = Poet.objects.all()
    serializer_class = PoetSerializer
