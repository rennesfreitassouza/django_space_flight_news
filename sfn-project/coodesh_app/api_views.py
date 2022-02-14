from codecs import lookup
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from coodesh_app.serializers import SFNArticlesSerializer
from coodesh_app.models import SFNArticles
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from pytz import UTC
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT


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
