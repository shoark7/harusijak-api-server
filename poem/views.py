from django.http import Http404
from django.shortcuts import render

from rest_framework import generics, mixins, serializers, status
from rest_framework.response import Response

from .models import Poem
from .serializers import PoemSerializer
from .permissions import IsWriterOrReadOnly


class PoemList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        serializer_context = {'request': request}
        serializer = PoemSerializer(poem, context=serializer_context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        poem.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
