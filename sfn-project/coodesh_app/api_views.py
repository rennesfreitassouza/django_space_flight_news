from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from coodesh_app.serializers import SFNArticlesSerializer, SFNArticlesLaunchesSerializer
from coodesh_app.models import SFNArticles, Tmy_id, SFNArticlesLaunches
from datetime import datetime
from pytz import UTC
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.http import QueryDict
from rest_framework.pagination import _positive_int
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# articles/
# articles/:my_id/
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


@permission_classes([IsAuthenticated])
# test_articles/:my_id/
class SFNArticlesRetrieveUpdateDestroy_(RetrieveUpdateDestroyAPIView):
    queryset = SFNArticles.objects.all()
    lookup_field = 'my_id'
    serializer_class = SFNArticlesSerializer

    def update(self, request, *args, **kwargs):
        """THE GET REQUEST MUST BE REDONE TO VIEW THE articleslaunches FIELD UPDATED."""
        

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
                'articleslaunches': article['articleslaunches'],
                'articlesevents': article['articlesevents']    
            })
            print("request.data", request.data)
            if isinstance(request.data, dict):
                dict_request = request.data
            else:    
                dict_request = request.data.dict()
            
            self.save_or_update_launches(article['my_id'], dict_request['article_launche_id'], dict_request['article_launche_id_provider'])


        return response

    def save_or_update_launches(self, my_id, article_launche_id, article_launche_id_provider):
        article = SFNArticles.objects.get(my_id=my_id)

        article_launches = SFNArticlesLaunches()
        article_launches.sfnarticles = article
        article_launches.article_launche_id = article_launche_id
        article_launches.provider = article_launche_id_provider
        
        article_launches.save()


# test_articles/
class SFNArticlesLaunchesAux():
    queryset = SFNArticlesLaunches.objects.all()
    serializer_class = SFNArticlesLaunchesSerializer


    def create2(self, request, last_id):
        #response = CreateAPIView.create(self, request)
        
        id_ret = Tmy_id().get_latest_my_id() - 1
        
        new_request = self.copy_query_dict(request, last_id)

        
        
        dict_new_request = new_request.dict()
        
        if dict_new_request['my_id'] == id_ret:
            article = SFNArticles.objects.get(my_id=last_id)

            SFNArticlesLaunches.objects.create(
                sfnarticles=article,
                article_launche_id=dict_new_request['article_launche_id'],provider=dict_new_request['article_launche_id_provider'])

    def copy_query_dict(self, request, last_id):
        new_query_dict = QueryDict(mutable=True)
        temp_query_dict = request.data.copy()

        new_query_dict['my_id'] = last_id
        new_query_dict['article_launche_id'] = temp_query_dict.get('article_launche_id', None)
        new_query_dict['article_launche_id_provider'] = temp_query_dict.get('article_launche_id_provider', None)


        return new_query_dict


# test_articles/
class SFNArticlesPagination(LimitOffsetPagination):
    """SFNArticlesPagination inherits rest_framework LimitOffsetPagination class and overrides its paginate_queryset and get_offset methods.

    Attrs:
        default_limit: default_limit indicates the maximum number of items to return
        max_limit: max_limit indicates the maximum number of items to return
        my_offset: my_offset indicates the starting position of the query in relation to the complete set of unpaginated items.

    """

    default_limit = 20
    max_limit = 100
    my_offset = 0

    @classmethod
    def set_default_limit(cls, value=None):
        if not value is None:        
            cls.default_limit = int(value)
        else:
            cls.default_limit = 20


    @classmethod
    def set_my_offset(cls, value=None):
        if not value is None:        
            cls.my_offset = int(value)
        else:
            cls.my_offset = 0

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])


    def get_offset(self, request):
        try:
            print("request.query_params", request.query_params)
            print("request.query_params[self.offset_query_param]", request.query_params[self.offset_query_param], type(request.query_params[self.offset_query_param]))

            return _positive_int(
                request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError):
            #self.set_my_offset()
            return self.my_offset #

@permission_classes([IsAuthenticated])
# test_articles/
class SFNArticlesList(ListAPIView, CreateAPIView):
    queryset = SFNArticles.objects.all().order_by('my_id')
    serializer_class = SFNArticlesSerializer
    pagination_class = SFNArticlesPagination

    
    def get_queryset(self):
        print("self.request.data", self.request.data )
        print("self.request.query_params", self.request.query_params)
        
        if not self.request.query_params :
            self.pagination_class.set_my_offset()
        if self.request.data:
            
            limit = self.request.data.get('limit', None)
            self.pagination_class.set_default_limit(limit)
            
            my_offset = self.request.data.get('my_offset', None)
            self.pagination_class.set_my_offset(my_offset)
            
        queryset = SFNArticles.objects.all().order_by('my_id')
        
        return queryset
        
    def create(self, request, *args, **kwargs):
        last_id = Tmy_id().get_latest_my_id()
        
        new_request = self.remove_query_dict(request, last_id)
        # response =  super().create(new_request, *args, **kwargs) or:
        response = CreateAPIView.create(self, new_request, *args, **kwargs)

        new_request = self.add_and_copy_query_dict(request, last_id)
        dict_new_request = new_request.data.copy()
        if (not dict_new_request["article_launche_id"] is None
            and not dict_new_request["article_launche_id_provider"] is None):
                        
            self.create_sfnarticleslaunche(request, last_id)
        else:
            print("article_launche_id is None")
            print("article_launche_id_provider is None")

        return response

    def add_and_copy_query_dict(self, request, last_id):
        new_query_dict = QueryDict(mutable=True)
        temp_query_dict = request.data.copy()
        
        new_query_dict = temp_query_dict
        dict_new_request = new_query_dict.copy()

        if (("article_launche_id" in dict_new_request.keys())
            and ("article_launche_id_provider" in dict_new_request.keys())):
            
            if ((dict_new_request['article_launche_id'] == '')
                and (dict_new_request['article_launche_id_provider'] == '')):
                temp_query_dict.pop('article_launche_id')
                temp_query_dict.pop('article_launche_id_provider')

            new_query_dict['article_launche_id'] = temp_query_dict.get('article_launche_id', None)
            new_query_dict['article_launche_id_provider'] = temp_query_dict.get('article_launche_id_provider', None)
        else:
            new_query_dict['article_launche_id'] = None
            new_query_dict['article_launche_id_provider'] = None
        new_query_dict['my_id'] = last_id

        return Response(data=new_query_dict)

    def remove_query_dict(self, request, last_id):
        new_query_dict = QueryDict(mutable=True)
        temp_query_dict = request.data.copy()
        print("temp_query_dict", temp_query_dict)
        new_query_dict = temp_query_dict.copy()
        
        dict_new_request = request.data.copy()
        if (("article_launche_id" in dict_new_request.keys())
            and ("article_launche_id_provider" in dict_new_request.keys())):
            
            print(f"BU REST_INTERFACE type >{new_query_dict['article_launche_id']}<", type(new_query_dict['article_launche_id']))
            
            new_query_dict.pop('article_launche_id')
            new_query_dict.pop('article_launche_id_provider')
        
        new_query_dict['my_id'] = last_id

        return Response(data=new_query_dict)

    def create_sfnarticleslaunche(self, request, last_id):
        new_launche = SFNArticlesLaunchesAux()
        new_launche.create2(request, last_id)
