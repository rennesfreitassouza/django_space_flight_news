from django.test import TestCase
from rest_framework.test import APITestCase
from coodesh_app.models import SFNArticles, SFNArticlesLaunches
import json
from datetime import datetime
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT



# Create your tests here.
class SFNArticlesCreateTestCase(APITestCase):

    def test_create_record(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)
        new_sfnarticle_data = {
            "api_id": 1,
            "title": "EMPTY",
            "url": "EMPTY",
            "imageUrl": "EMPTY",
            "newsSite": "EMPTY",
            "summary": "EMPTY",
            "updatedAt": "2022-02-13T13:34:02",
            "publishedAt": "2022-02-13T13:34:02",
            "featured": True,
            "event_id": "EMPTY",
            "event_provider": "EMPTY",
            "launche_id": "EMPTY",
            "launche_provider": "EMPTY",
        }
        response = self.client.post('http://127.0.0.1:8000/articles/', data=new_sfnarticle_data)
        if response.status_code != 200:
            print(response.data)
        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(initial_sfnarticles_count + 1, new_sfnarticles_count, msg=f"response.data {response.data}")
        
        # print("new_sfnarticles_count", new_sfnarticles_count)

        for k, v in response.data.items():
            if k != 'events' and k != 'lauches' and k != 'updatedAt' and k != 'publishedAt':
                self.assertEqual(new_sfnarticle_data[k], v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, v {v}")
            elif k == 'updatedAt' or k == 'publishedAt':
                
                str_v = v.strftime(DATETIME_FORMAT)
                # print(f"str_v {str_v}")
                self.assertEqual(new_sfnarticle_data[k], str_v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, str_v {str_v}")

            elif k == 'events':
                # print(v)
                for eventKey, eventValue in v[0].items():
                    if eventKey == 'article_event_id':
                        self.assertEqual(new_sfnarticle_data["event_id"], eventValue, msg=f"new_sfnarticle_data['article_event_id'] {new_sfnarticle_data['event_id']}, eventValue {eventValue}")
                    else:
                        self.assertEqual(new_sfnarticle_data['event_provider'], eventValue, msg=f"new_sfnarticle_data['event_provider'] {new_sfnarticle_data['event_provider']}, eventValue {eventValue}")
            elif k == 'lauches':
                for lauchesKey, lauchesValue in v[0].items():
                    if lauchesKey == 'article_launche_id':
                        self.assertEqual(new_sfnarticle_data["launche_id"], lauchesValue, msg=f"new_sfnarticle_data['article_launche_id'] {new_sfnarticle_data['launche_id']}, lauchesValue {lauchesValue}")
                    else:
                        self.assertEqual(new_sfnarticle_data['launche_provider'], lauchesValue, msg=f"new_sfnarticle_data['launche_provider'] {new_sfnarticle_data['launche_provider']}, lauchesValue {lauchesValue}")

    def test_create_record_new_route(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)
        new_sfnarticle_data = {
            "api_id": 0,
            "title": "ff",
            "url": "f2",
            "imageUrl": "f2",
            "newsSite": "f",
            "summary": "f",
            "updatedAt": "2021-02-13T13:34:02",
            "publishedAt": "2021-02-13T13:34:02",
            "featured": True,

            "article_launche_id": "article_launche_idarticle_launche_id",
            "article_launche_id_provider": "article_launche_id_providerarticle_launche_id_provider"
        }
        response = self.client.post('http://127.0.0.1:8000/test_articles/', data=new_sfnarticle_data)
        if response.status_code != 201:
            print(response.data)
        else:
            # response = self.client.get(f'http://127.0.0.1:8000/test_articles/')#{response.data["my_id"]}') # OrderedDict with count
            response = self.client.get(f'http://127.0.0.1:8000/test_articles/{response.data["my_id"]}/') # dict

        
        # print("response.data", response.data)
        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(initial_sfnarticles_count + 1, new_sfnarticles_count, msg=f"response.data {response.data}")
        
        # print("new_sfnarticles_count", new_sfnarticles_count)

        for k, v in response.data.items():
            if k != 'my_id' and k != 'articleslaunches' and k != 'articlesevents' and k != 'updatedAt' and k != 'publishedAt':
                self.assertEqual(new_sfnarticle_data[k], v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, v {v}")
            elif k == 'updatedAt' or k == 'publishedAt':
                # print("type(v)", type(v))
                
                datetime_v = datetime.strptime(v, DATETIME_FORMAT)
                str_v = datetime_v.strftime(DATETIME_FORMAT)
                
                # print("str_v", str_v)
                self.assertEqual(new_sfnarticle_data[k], str_v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, str_v {str_v}")

            elif k == 'articlesevents':
                # print(f'NO CORRESPONDING VALUE k {k}  v {v} INSERTED')
                #
                self.assertEqual([], v, msg=f"EXPECTED: {list()}")
            elif k == 'articleslaunches':
                for lauchesKey, lauchesValue in v[0].items():
                    if lauchesKey == 'article_launche_id':
                        self.assertEqual(new_sfnarticle_data["article_launche_id"], lauchesValue, msg=f"new_sfnarticle_data['article_launche_id'] {new_sfnarticle_data['article_launche_id']}, lauchesValue {lauchesValue}")
                    elif lauchesKey == 'provider':
                        self.assertEqual(new_sfnarticle_data['article_launche_id_provider'], lauchesValue, msg=f"new_sfnarticle_data['article_launche_id_provider'] {new_sfnarticle_data['article_launche_id_provider']}, lauchesValue {lauchesValue}")
                    elif lauchesKey == 'sfnarticles':
                        self.assertEqual(response.data['my_id'], lauchesValue, msg=f"response.data['my_id'] {response.data['my_id']}, lauchesValue {lauchesValue}")

class SFNArticlesDestroyTestCase(APITestCase):

    def create_sfnarticle_article(self):

        new_sfnarticle_data = {
            "api_id": 1,
            "title": "EMPTY",
            "url": "EMPTY",
            "imageUrl": "EMPTY",
            "newsSite": "EMPTY",
            "summary": "EMPTY",
            "updatedAt": "2022-02-13T13:34:02",
            "publishedAt": "2022-02-13T13:34:02",
            "featured": True,
            "event_id": "EMPTY",
            "event_provider": "EMPTY",
            "launche_id": "EMPTY",
            "launche_provider": "EMPTY",
        }
        response = self.client.post('http://127.0.0.1:8000/articles/', data=new_sfnarticle_data)
        if response.status_code != 200:
            print(response.data)
        
        return response
    
    def test_delete_sfnarticles(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)

        response = self.create_sfnarticle_article()
        
        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(new_sfnarticles_count - 1, initial_sfnarticles_count, msg=f"response.data {response.data}")
        # print("new_sfnarticles_count", new_sfnarticles_count)

        sfnarticles_my_id = SFNArticles.objects.first().my_id
        self.client.delete('http://127.0.0.1:8000/articles/{}/'.format(sfnarticles_my_id))
        self.assertEqual(
            SFNArticles.objects.count(),
            new_sfnarticles_count - 1
        )
        self.assertRaises(
            SFNArticles.DoesNotExist,
            SFNArticles.objects.get, my_id=sfnarticles_my_id,
        )

    def create_sfnarticle_article_new_route(self):

        new_sfnarticle_data = {
            "f": "ff",
            "api_id": 14024,
            "title": "ff",
            "url": "ff",
            "imageUrl": "fff",
            "newsSite": "fffff",
            "summary": "ff",
            "updatedAt": "2022-02-21T11:59:55",
            "publishedAt": "2022-02-21T11:59:50",
            "featured": True
        }
        payload = json.dumps(new_sfnarticle_data)

        response = self.client.post('http://127.0.0.1:8000/test_articles/', 
                   data=payload,
                   content_type="application/json")

        if response.status_code != 201:
            print(response.data)
        else:
            # response = self.client.get(f'http://127.0.0.1:8000/test_articles/')#{response.data["my_id"]}') # OrderedDict with count
            response = self.client.get(f'http://127.0.0.1:8000/test_articles/{response.data["my_id"]}/') # dict

        return response
    
    def test_delete_sfnarticles_new_route(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)
        
        response = self.create_sfnarticle_article_new_route()

        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(initial_sfnarticles_count + 1, new_sfnarticles_count, msg=f"response.data {response.data}")
        
        # print("new_sfnarticles_count", new_sfnarticles_count)

        sfnarticles_my_id = SFNArticles.objects.first().my_id
        self.client.delete('http://127.0.0.1:8000/articles/{}/'.format(sfnarticles_my_id))
        self.assertEqual(
            SFNArticles.objects.count(),
            new_sfnarticles_count - 1
        )
        self.assertRaises(
            SFNArticles.DoesNotExist,
            SFNArticles.objects.get, my_id=sfnarticles_my_id,
        )


class SFNArticlesListTestCase(APITestCase):

    def test_list_sfnarticles(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)
        response = self.client.get('http://127.0.0.1:8000/articles/')
        # print('response.data', response.data)
        self.assertListEqual(list(), response.data['articles_data'])
        self.assertFalse(response.data['has_next'])
        self.assertFalse(response.data['has_previous'])
        self.assertEqual(response.data['current_page_number'], 1)
        self.assertEqual(response.data['num_pages'], 1)

    def test_list_sfnarticles_new_route(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)
        response = self.client.get('http://127.0.0.1:8000/test_articles/')
        # print('response.data', response.data)
        self.assertListEqual(list(), response.data['results'])
        self.assertIsNone(response.data['previous'])
        self.assertIsNone(response.data['next'])
        self.assertEqual(response.data['count'], 0)

class SFNArticlesUpdateTestCase(APITestCase):

    def create_sfnarticle_article(self):

        new_sfnarticle_data = {
            "api_id": 1,
            "title": "EMPTY",
            "url": "EMPTY",
            "imageUrl": "EMPTY",
            "newsSite": "EMPTY",
            "summary": "EMPTY",
            "updatedAt": "2022-02-13T13:34:02",
            "publishedAt": "2022-02-13T13:34:02",
            "featured": True,
            "event_id": "EMPTY",
            "event_provider": "EMPTY",
            "launche_id": "EMPTY",
            "launche_provider": "EMPTY",
        }
        response = self.client.post('http://127.0.0.1:8000/articles/', data=new_sfnarticle_data)
        if response.status_code != 200:
            print(response.data)
        
        return response

    def test_update_product(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)

        response = self.create_sfnarticle_article()
        
        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(new_sfnarticles_count - 1, initial_sfnarticles_count, msg=f"response.data {response.data}")
        # print("new_sfnarticles_count", new_sfnarticles_count)

        sfnarticles = SFNArticles.objects.first()

        payload = json.dumps({"title": "!!!!NOT_EMPTY!!!",
                            "launche_id": "!!!!NOT_EMPTY!!!",
                            })

        response = self.client.put(
            path='http://127.0.0.1:8000/articles/{}/'.format(sfnarticles.my_id),
            data=payload,
            content_type="application/json"
        )
        # print("response.data", response.data)

        self.assertEqual(# "Campo" não é atualidado
            "EMPTY",
            SFNArticlesLaunches.objects.all().first().article_launche_id
        )
        self.assertEqual(# Campo é atualidado
            "!!!!NOT_EMPTY!!!",
            SFNArticles.objects.all().first().title
        )

    def create_sfnarticle_article_new_route(self):

        new_sfnarticle_data = {
            "api_id": 0,
            "title": "ff",
            "url": "f2",
            "imageUrl": "f2",
            "newsSite": "f",
            "summary": "f",
            "updatedAt": "2021-02-13T13:34:02",
            "publishedAt": "2021-02-13T13:34:02",
            "featured": True
        }

        response = self.client.post('http://127.0.0.1:8000/test_articles/', data=new_sfnarticle_data)
        if response.status_code != 201:
            print(response.data)
        else:
            # response = self.client.get(f'http://127.0.0.1:8000/test_articles/')#{response.data["my_id"]}') # OrderedDict with count
            response = self.client.get(f'http://127.0.0.1:8000/test_articles/{response.data["my_id"]}/') # dict

        return response
    
    
    def test_update_product_new_route(self):
        initial_sfnarticles_count = SFNArticles.objects.count()
        # print("initial_sfnarticles_count", initial_sfnarticles_count)

        response = self.create_sfnarticle_article_new_route()
        
        new_sfnarticles_count = SFNArticles.objects.count()
        self.assertEqual(new_sfnarticles_count - 1, initial_sfnarticles_count, msg=f"response.data {response.data}")
        # print("new_sfnarticles_count", new_sfnarticles_count)

        sfnarticles = SFNArticles.objects.first()
        
        payload = response.data # required
        payload.update({"title": "!!!!NOT_EMPTY!!!",
                        "article_launche_id": "!!!!NOT_EMPTY!!!", # required with article_launche_id_provider
                        "article_launche_id_provider": "!!!!NOT_EMPTY!!!" # required
                        })
        new_payload = json.dumps(payload)
        # print("type(new_payload)",type(new_payload),'new_payload', new_payload)

        response = self.client.put(
            path='http://127.0.0.1:8000/test_articles/{}/'.format(sfnarticles.my_id),
            data=new_payload,
            content_type="application/json"
        )

        response = self.client.get(path='http://127.0.0.1:8000/test_articles/{}/'.format(sfnarticles.my_id))

        
        # print("response.data", response.data)

        self.assertEqual( # "Campo" não é atualidado, apenas inserido
            "!!!!NOT_EMPTY!!!",
            SFNArticlesLaunches.objects.all().first().article_launche_id
        )
        self.assertEqual( # "Campo" não é atualidado, apenas inserido
            "!!!!NOT_EMPTY!!!",
            SFNArticlesLaunches.objects.all().first().provider
        )
        self.assertEqual(# Campo é atualidado
            "!!!!NOT_EMPTY!!!",
            SFNArticles.objects.all().first().title
        )
