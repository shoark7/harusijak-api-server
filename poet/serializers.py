from rest_framework import routers, serializers, viewsets

from .models import Poet


class PoetSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    # password = serializers.CharField(style={'input_type': 'password'})
    nickname = serializers.CharField()
    description = serializers.CharField(required=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=True,
                                  required=False, use_url=True)


class PoetCreateSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    password_conf = serializers.CharField(style={'input_type': 'password'}, required=False)
    nickname = serializers.CharField()
    description = serializers.CharField(required=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=True,
                                  required=False, use_url=True)


    def create(self, validated_data):
        poet = Poet.objects.create_user(**validated_data)
        return poet


class PoetViewSet(viewsets.ModelViewSet):
    queryset = Poet.objects.all()
    serializer_class = PoetSerializer


    """
{"identifier": "fjalfkasdf",
"password_conf": "asdfasdfljkjasdf",
"password": "asdfasdfljkjasdf",
"nickname": "afjalfkjsdlf"}
    """
