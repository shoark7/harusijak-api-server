from datetime import date as dt

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, mixins, serializers, status
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Dislike, Like, Poem
from .serializers import PoemSerializer
from .permissions import IsWriterOrReadOnly
from poet.permissons import ReadOnly
from date.models import Date


class PoemList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = serializer.data
        for item in data:
            item['do_like'] = Like.objects.filter(poet__pk=request.user.id, poem__pk=item['id']).exists()
            item['do_dislike'] = Dislike.objects.filter(poet__pk=request.user.id, poem__pk=item['id']).exists()

        return self.get_paginated_response(data)
        # return self.get_paginated_response(data) if page else Response(data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        today = dt.today()
        date = Date.get_or_create(today)
        if 'displayed' in serializer.initial_data \
            and serializer.initial_data['displayed'] == False:
            displayed = False
        else:
            displayed = True
        serializer.save(displayed=displayed, written_date=date, writer=self.request.user)


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

        data = serializer.data
        data['do_like'] = Like.objects.filter(poet__pk=request.user.id, poem__pk=data['id']).exists()
        data['do_dislike'] = Dislike.objects.filter(poet__pk=request.user.id, poem__pk=data['id']).exists()
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        poem = self.get_object(pk)
        self.check_object_permissions(request, poem)
        serializer_context = {'request': request}
        serializer = PoemSerializer(poem, context=serializer_context, data=request.data)
        if serializer.is_valid():
            if 'displayed' in serializer.initial_data:
                displayed = serializer.initial_data['displayed']
            else:
                displayed = poem.displayed

            serializer.save(displayed=displayed)
            data = serializer.data
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


# About poems' search by filters
class PeomSearch(generics.ListAPIView):
    permission_classes = (ReadOnly,)
    serializer_class = PoemSerializer

    def get_queryset(self):
        SUPPORTED_FILTERS = ('poet_nickname', 'content')
        FILTERS_AS_STRING = ', '.join(SUPPORTED_FILTERS)

        queryset = Poem.objects.all()
        filter_by = self.request.query_params.get('filter_by', None)
        target = self.request.query_params.get('target', None)

        if filter_by not in SUPPORTED_FILTERS:
            raise exceptions.NotFound("Supproted filters are {}".format(FILTERS_AS_STRING))
        elif filter_by == 'poet_nickname': # Filter by nickname
            queryset = queryset.filter(writer__nickname=target)
        elif filter_by == 'content':       # Filter by subject and title
            queryset = queryset.filter(
                Q(title__contains=target) | Q(written_date__subject__subject__contains=target)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# About today's information section
@api_view(['GET'])
def about_today(request):
    today = Date.get_or_create()
    return Response({'date': today.date,
                     'subject': today.subject.subject,
                     'guide_format': today.subject.guide_format,
                     'guide_type': today.subject.guide_type,
                     'count_of_poems_written': today.poem_set.count()})
