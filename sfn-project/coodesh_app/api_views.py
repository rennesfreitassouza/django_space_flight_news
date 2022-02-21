from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from coodesh_app.serializers import SFNArticlesSerializer
from coodesh_app.models import SFNArticles, Tmy_id
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from pytz import UTC
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpRequest
from rest_framework.response import Response
from django.shortcuts import render


class SFNArticlesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = SFNArticles.objects
    lookup_field = 'my_id'
    serializer_class = SFNArticlesSerializer

    def get(self, **kwargs):
        if 'my_id' in kwargs.keys():
            try:
                response = self.queryset.get(my_id=kwargs['my_id'])
            except:
                response = {'ERROR': 'ERROR TO GET RECORD'}
            return response

    def delete(self, request, *args, **kwargs):

        response = self.get(**kwargs)
        if isinstance(response, SFNArticles):
            try:
                response_repr = repr(response)
                response = response.delete()
            except:
                response = {'ERROR': 'ERROR TO DELETE RECORD'}
            else:
                response = f"record {response_repr} {kwargs['my_id']} deleted"

        return response

    def update(self, request, *args, **kwargs):
        response = self.get(**kwargs)

        if isinstance(response, SFNArticles):

            response = self.set_article(response, **request.data)
            try:
                response.save()
            except:
                response = {'ERROR': 'ERROR TO UPDATE RECORD'}
            else:
                response = self.get(**kwargs)
                print("response", response)
                response = SFNArticlesSerializer().format_article_data(response)

        return response

    def set_article(self, sfn_article, **data):
        sfn_article.api_id = data.get('api_id', sfn_article.api_id)
        sfn_article.title = data.get('title', sfn_article.title)
        sfn_article.url = data.get('url', sfn_article.url)
        sfn_article.imageUrl = data.get('imageUrl', sfn_article.imageUrl)
        sfn_article.newsSite = data.get('newsSite', sfn_article.newsSite)
        sfn_article.summary = data.get('summary', sfn_article.summary)

        raw_publishedAt = {'publishedAt': data.get(
            'publishedAt', sfn_article.publishedAt.strftime(DATETIME_FORMAT))}

        sfn_article.publishedAt = UTC.localize(
            datetime.strptime(raw_publishedAt.get('publishedAt'), DATETIME_FORMAT))

        raw_updatedAt = {'updatedAt': data.get(
            'updatedAt', sfn_article.updatedAt.strftime(DATETIME_FORMAT))}

        sfn_article.updatedAt = UTC.localize(
            datetime.strptime(raw_updatedAt.get('updatedAt'), DATETIME_FORMAT))

        sfn_article.featured = data.get('featured', sfn_article.featured)
        return sfn_article


class SFNArticlesRetrieveUpdateDestroy_(RetrieveUpdateDestroyAPIView):
    queryset = SFNArticles.objects.all()
    lookup_field = 'my_id'
    serializer_class = SFNArticlesSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            from django.core.cache import cache

            article = response.data
            cache.set('article_data_{}'.format(article['my_id']), {
                'my_id': article['my_id'],
                'api_id': article['api_id'],
                'title': article['title'],
                'url': article['url'],
                'imageUrl': article['imageUrl'],
                'newsSite': article['newsSite'],
                'summary': article['summary'],
                'updatedAt': article['updatedAt'],
                'publishedAt': article['publishedAt'],
                'featured': article['featured'],
            })
        return response


class SFNArticlesPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class SFNArticlesList(ListAPIView, CreateAPIView):
    queryset = SFNArticles.objects.all()
    serializer_class = SFNArticlesSerializer
    pagination_class = SFNArticlesPagination

    def create(self, request, *args, **kwargs):
        
        last_id = Tmy_id().get_last_my_id()
        
        new_request = self.copy_query_dict(request, last_id)
        
        # response =  super().create(new_request, *args, **kwargs)
        response = CreateAPIView.create(self, new_request, *args, **kwargs)
        
        return response

    def copy_query_dict(self, request, last_id):

        temp_query_dict = request.data.copy()
        temp_query_dict['my_id'] = last_id

        return Response(data=temp_query_dict)
