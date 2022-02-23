from django.test import TestCase
from rest_framework.test import APITestCase
from coodesh_app.models import SFNArticles
import json
import requests
import datetime
from coodesh_app.management.commands.load_api_data import DATETIME_FORMAT

# Create your tests here.
class SFNArticlesCreateTestCase(APITestCase):
    # def test_get_product(self):
    #     body = {"page": 2}
    #     response = self.client.get('http://127.0.0.1:8000/articles/', data=body)
    #     if response.status_code != 200:
    #         print(response)
    #     print("response.data", response.data)
    #     print("<"*100)
    #     self.assertEqual(len(json.dumps(response.data)), 10, msg=f"response: {response}")

    # def test_get_product_using_requests(self):
    #     body = {"page": 2}
    #     url = 'http://127.0.0.1:8000/articles/'
    #     response = requests.get(url, data=body)

    #     if response.status_code != 200:
    #         print(response)
    #     else:
    #         response_dict = json.loads(response.content)
    #         response_str_print = json.dumps(response_dict, indent=2)
    #         expected_tam = 10
    #         self.assertEqual(len(response_dict["articles_data"]), expected_tam, msg=f"response: {response_str_print}")
    
    def test_create_record(self):
        initial_product_count = SFNArticles.objects.count()
        print("initial_product_count", initial_product_count)
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
        new_product_count = SFNArticles.objects.count()
        self.assertEqual(initial_product_count + 1, new_product_count, msg=f"response.data {response.data}")
        
        for k, v in response.data.items():
            if k != 'events' and k != 'lauches' and k != 'updatedAt' and k != 'publishedAt':
                self.assertEqual(new_sfnarticle_data[k], v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, v {v}")
            elif k == 'updatedAt' or k == 'publishedAt':
                
                str_v = v.strftime(DATETIME_FORMAT)
                self.assertEqual(new_sfnarticle_data[k], str_v, msg=f"new_sfnarticle_data[k] {new_sfnarticle_data[k]}, str_v {str_v}")

            elif k == 'events':
                print(v)
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

