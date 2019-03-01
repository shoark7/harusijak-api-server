from django.http import Http404
from django.shortcuts import get_object_or_404, render

from rest_framework import generics, mixins, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Dislike, Like, Poem
from .serializers import PoemSerializer
from .permissions import IsWriterOrReadOnly


class PoemList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = list(serializer.data)
            for item in data:
                item['do_like'] = request.user.is_authenticated and \
                                    Like.objects.filter(poet=request.user, poem__pk=item['id']).exists()
                item['do_dislike'] = request.user.is_authenticated and \
                                    Dislike.objects.filter(poet=request.user, poem__pk=item['id']).exists()
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = list(serializer.data)
        for item in data:
            item['do_like'] = request.user.is_authenticated and \
                                    Like.objects.filter(poet=request.user, poem__pk=item['id']).exists()
            item['do_dislike'] = request.user.is_authenticated and \
                                    Dislike.objects.filter(poet=request.user, poem__pk=item['id']).exists()
        return Response(data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
        serializer.save(displayed=True)


class PoemDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = (IsWriterOrReadOnly,)

    def get_object(self, pk):
        try:
            return Poem.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        serializer_context = {'request': request}
        serializer = PoemSerializer(poem, context=serializer_context)

        data = dict(serializer.data)
        data['do_like'] = request.user.is_authenticated and \
                            Like.objects.filter(poet=request.user, poem__pk=data['id']).exists()
        data['do_dislike'] = request.user.is_authenticated and \
                            Dislike.objects.filter(poet=request.user, poem__pk=data['id']).exists()
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        serializer_context = {'request': request}
        serializer = PoemSerializer(poem, context=serializer_context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = dict(serializer.data)
            data['do_like'] = Like.objects.filter(poet=request.user, poem__pk=data['id']).exists()
            data['do_dislike'] = Dislike.objects.filter(poet=request.user, poem__pk=data['id']).exists()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        poem.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# Like and dislike sections
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def toggle_like(request, pk):
    poem = get_object_or_404(Poem, pk=pk)
    if Like.objects.filter(poet=request.user, poem=poem).exists():
        Like.objects.get(poet=request.user, poem=poem).delete()
        poem.likes -= 1
        poem.save()
        return Response({"message": "Successfully Like toggled off"}, status=status.HTTP_200_OK)
    else:
        Like.objects.create(poet=request.user, poem=poem)
        poem.likes += 1
        poem.save()
        return Response({"message": "Successfully Like toggled on"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def toggle_dislike(request, pk):
    poem = get_object_or_404(Poem, pk=pk)
    if Dislike.objects.filter(poet=request.user, poem=poem).exists():
        Dislike.objects.get(poet=request.user, poem=poem).delete()
        poem.dislikes -= 1
        poem.save()
        return Response({"message": "Successfully Dislike toggled off"}, status=status.HTTP_200_OK)
    else:
        Dislike.objects.create(poet=request.user, poem=poem)
        poem.dislikes += 1
        poem.save()
        return Response({"message": "Successfully Dislike toggled on"}, status=status.HTTP_200_OK)
