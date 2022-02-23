from django.db import models
from django.db.utils import IntegrityError
from django.db.models import BigAutoField
# Create your models here.

class Tmy_id:

    def get_latest_my_id(self):
        try:
            record = SFNArticles.objects.all().latest('my_id') 
        except SFNArticles.DoesNotExist:
            response = {'ERROR': 'RECORD DOES NOT EXIST'}
            print(response)
            response = 0
        else:
            response = record.my_id + 1

        return response


class SFNArticles(models.Model):
    my_id = models.BigIntegerField(primary_key=True, default=Tmy_id().get_latest_my_id)
    api_id = models.IntegerField(unique=False)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    imageUrl = models.CharField(max_length=255)
    newsSite = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    updatedAt = models.DateTimeField()
    publishedAt = models.DateTimeField()
    featured = models.BooleanField()

     

    def set_article_data_pk_1(self, article):
        saved = False
        infite = 0
        while(saved is False and infite < 120_125):
            try:
                article.save()
            except:  # IntegrityError:
                infite += 1
                article.my_id += 1
            else:
                saved = True
        if saved is False:
            return {'return': 'NOT saved!'}
        return {'return': 'Saved!', 'my_id': article.my_id}

    def set_article_data_pk_0(self, article):

        ref_query_set = SFNArticles.objects.all()

        last_ref_obj_pk = 0
        if ref_query_set:
            if ref_query_set.exists():
                ref_obj = ref_query_set.last()
                last_ref_obj_pk = ref_obj.my_id

        article.my_id = last_ref_obj_pk + 1
        return self.set_article_data_pk_1(article)

    def __repr__(self):
        return f'''< SFNArticles object ({self.my_id})\
            api_id: {self.api_id},\
            title: {self.title},\
            url: {self.url},\
            imageUrl: {self.imageUrl},\
            newsSite: {self.newsSite},\
            summary: {self.summary},\
            updatedAt: {self.updatedAt},\
            publishedAt: {self.publishedAt},\
            publishedAt: {self.publishedAt},\
            featured: {self.featured} >'''


class SFNArticlesLaunches(models.Model):
    sfnarticles = models.ForeignKey(SFNArticles, on_delete=models.CASCADE)
    article_launche_id = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)


class SFNArticlesEvents(models.Model):
    sfnarticles = models.ForeignKey(SFNArticles, on_delete=models.CASCADE)
    article_event_id = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
