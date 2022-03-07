from django.core.paginator import Paginator
from coodesh_app.models import SFNArticles
from coodesh_app.serializers import SFNArticlesSerializer
from coodesh_app.src.exceptions import SFNArticlesDoesNotExistNotify

def get_page(request_data={'page': 1}):
    """deprecated"""
    space_flight_a = SFNArticles.objects.all().order_by('my_id')
    items_per_page = 10
    paginator = Paginator(space_flight_a, items_per_page)
    page_number = request_data['page']

    page_n = paginator.get_page(page_number)

    r = list(map(lambda x: SFNArticlesSerializer(
    ).format_article_data(x), page_n.object_list))

    response = {'articles_data': r,
                'has_next': page_n.has_next(), 'has_previous': page_n.has_previous(),
                'current_page_number': page_number, 'num_pages': paginator.num_pages}

    return response


def get_article_by_my_id(my_id):
    """deprecated"""
    try:
        space_flight_a = SFNArticles.objects.get(my_id=my_id)
    except SFNArticles.DoesNotExist as e:
        retorno = {'ERROR': 'RECORD DOES NOT EXIST'}
        SFNArticlesDoesNotExistNotify(__file__, e.args, retorno, notify=False)
    else:
        retorno = SFNArticlesSerializer(
        ).format_article_data(space_flight_a)
    return retorno
