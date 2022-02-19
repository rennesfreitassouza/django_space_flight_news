from dataclasses import fields
from rest_framework import serializers
from coodesh_app.models import SFNArticles,  SFNArticlesLaunches, SFNArticlesEvents


'''
    "In general, serializing means to convert an object into fomrat like JSON, YAML or XML."
'''

class SFNArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFNArticles
        fields = ('api_id', 'title', 'url', 'imageUrl', 'newsSite',
                  'summary', 'updatedAt', 'publishedAt', 'publishedAt', 'featured')

    def format_article_data(self, sfn_data):

        r = {'api_id': sfn_data.api_id, 'title': sfn_data.title,
             'url': sfn_data.url, 'imageUrl': sfn_data.imageUrl,
             'newsSite': sfn_data.newsSite, 'summary': sfn_data.summary,
             'updatedAt': sfn_data.updatedAt, 'publishedAt': sfn_data.publishedAt,
             'publishedAt': sfn_data.publishedAt, 'featured': sfn_data.featured}

        r.update(SFNArticlesEventsSerializer().get_article_events(sfn_data))
        r.update(SFNArticlesLaunchesSerializer().get_article_lauches(sfn_data))

        return r


class SFNArticlesLaunchesSerializer(serializers.ModelSerializer):
    class Meta:
        Model = SFNArticlesLaunches
        fields = ('article_launche_id', 'provider')

    def get_article_lauches(self, sfn_article):
        retorno = {'lauches': []}

        launches = SFNArticlesLaunches.objects.filter(sfnarticles=sfn_article)
        if launches.exists():
            retorno['lauches'] = [{'article_launche_id': launche.article_launche_id,
                                   'provider': launche.provider} for launche in launches]
        return retorno


class SFNArticlesEventsSerializer(serializers.ModelSerializer):
    class Meta:
        Model = SFNArticlesEvents
        fields = ('article_event_id', 'provider')

    def get_article_events(self, sfn_article):
        retorno = {'events': []}

        events = SFNArticlesEvents.objects.filter(sfnarticles=sfn_article)
        if events.exists():
            retorno['events'] = [{'article_event_id': event.article_event_id,
                                  'provider': event.provider} for event in events]
        return retorno
