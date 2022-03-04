from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from coodesh_app.src.get_functions import get_page, get_article_by_my_id
from coodesh_app.src.post_functions import create_new_article
from coodesh_app import api_views
from django.contrib.auth.decorators import login_required


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return render(request, "coodesh_app/home.html")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def gen_article_view(request):
    response = dict()

    if request.method == 'GET':

        page = 1
        if request.data:
            page = request.data.get('page', 1)
        response = get_page({'page': page})
    elif request.method == 'POST':
        data = request.data
        response = create_new_article(data)

    return Response(response)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_article(request, *args, **kwargs):
    if request.method == 'GET':
        if 'my_id' in kwargs.keys():
            response = get_article_by_my_id(kwargs['my_id'])
        else:
            response = {'ERROR': 'INVALID ID'}

        return Response(response)
    elif request.method == 'PUT':

        responseClass = api_views.SFNArticlesRetrieveUpdateDestroy()
        response = responseClass.update(request, *args, **kwargs)
        return Response(response)

    elif request.method == 'DELETE':
        responseClass = api_views.SFNArticlesRetrieveUpdateDestroy()
        response = responseClass.delete(request, *args, **kwargs)
        return Response(response)
