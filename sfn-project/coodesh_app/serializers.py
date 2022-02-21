from dataclasses import fields
from rest_framework import serializers
from coodesh_app.models import SFNArticles,  SFNArticlesLaunches, SFNArticlesEvents


'''
    "In general, serializing means to convert an object into format like JSON, YAML or XML."
'''

class SFNArticlesSerializer(serializers.ModelSerializer):
    my_id = serializers.IntegerField(read_only=True)
    api_id = serializers.IntegerField(read_only=False)
    title = serializers.CharField(min_length=2, max_length=255)
    url = serializers.CharField(read_only=False)
    imageUrl = serializers.CharField(read_only=False)
    newsSite = serializers.CharField(read_only=False)
    summary = serializers.CharField(read_only=False)
    updatedAt = serializers.DateTimeField(read_only=False)
    publishedAt = serializers.DateTimeField(read_only=False)
    featured = serializers.BooleanField(read_only=False)
    #test = serializers.CharField(read_only=False, source='summary')
    """ The  SerializerMethodField will by default call the method get_'field name'()"""
    articleslaunches = serializers.SerializerMethodField()
    articlesevents = serializers.SerializerMethodField()
    
    class Meta:
        model = SFNArticles
        fields = ('my_id', 'api_id', 'title', 'url', 'imageUrl', 'newsSite', 'summary', 'updatedAt', 'publishedAt', 'publishedAt', 'featured', 'articleslaunches', 'articlesevents') #'test' )

    def format_article_data(self, sfn_data):

        r = {'api_id': sfn_data.api_id, 'title': sfn_data.title,
             'url': sfn_data.url, 'imageUrl': sfn_data.imageUrl,
             'newsSite': sfn_data.newsSite, 'summary': sfn_data.summary,
             'updatedAt': sfn_data.updatedAt, 'publishedAt': sfn_data.publishedAt,
             'publishedAt': sfn_data.publishedAt, 'featured': sfn_data.featured}

        r.update(SFNArticlesEventsSerializer().get_article_events(sfn_data))
        r.update(SFNArticlesLaunchesSerializer().get_article_lauches(sfn_data))

        return r

    def get_articleslaunches(self, instance):
        article_launches = SFNArticlesLaunches.objects.filter(sfnarticles=instance)
        return SFNArticlesLaunchesSerializer(article_launches, many=True).data
        

    def get_articlesevents(self, instance):
        article_events = SFNArticlesEvents.objects.filter(sfnarticles=instance)
        return SFNArticlesEventsSerializer(article_events, many=True).data


class SFNArticlesLaunchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFNArticlesLaunches
        fields = ('sfnarticles', 'article_launche_id', 'provider')

    def get_article_lauches(self, sfn_article):
        retorno = {'lauches': []}

        launches = SFNArticlesLaunches.objects.filter(sfnarticles=sfn_article)
        if launches.exists():
            retorno['lauches'] = [{'article_launche_id': launche.article_launche_id,
                                   'provider': launche.provider} for launche in launches]
        return retorno


class SFNArticlesEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFNArticlesEvents
        fields = ('sfnarticles', 'article_event_id', 'provider')

    def get_article_events(self, sfn_article):
        retorno = {'events': []}

        events = SFNArticlesEvents.objects.filter(sfnarticles=sfn_article)
        if events.exists():
            retorno['events'] = [{'article_event_id': event.article_event_id,
                                  'provider': event.provider} for event in events]
        return retorno
