from django.db import models
from coodesh_app.src.exceptions import SFNArticlesDoesNotExistNotify
# Create your models here.

class Tmy_id:
    """Tmy_id returns the latest id + 1  of a SFNArticles record.
    """
    def get_latest_my_id(self):
        try:
            record = SFNArticles.objects.all().latest('my_id') 
        except SFNArticles.DoesNotExist as e:
            # need an improvement: an insert query)
            response = 0
            msg = (f'ERROR: NO RECORD RETRIEVED pk = {response}')
            SFNArticlesDoesNotExistNotify(__file__, e.args, msg, notify=False)
        else:
            response = record.my_id + 1
            msg = (f'Ok: RECORD RETRIEVED. Generating new pk... = {response}')
            print(msg)
        return response


class SFNArticles(models.Model):
    my_id = models.BigIntegerField(primary_key=True)
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
        """deprecated"""
        saved = False
        infinite = 0
        while(saved is False and infinite < 120_125):
            try:
                article.save(force_insert=True)
                msg = f'return: Saved! my_id: {article.my_id}'
            except:  # IntegrityError:
                infinite += 1
                article.my_id += 1
            else:
                saved = True
        if saved is False:
            print(f'Error: infinite max value exceeded: {infinite}')
            raise Exception
        print(msg)
        return {'return': 'Saved!', 'my_id': article.my_id}

    def set_article_data_pk_0(self, article):

        

        last_ref_obj_pk = Tmy_id().get_latest_my_id()

        article.my_id = last_ref_obj_pk
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
