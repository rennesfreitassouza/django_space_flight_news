from django.contrib import admin
from django.urls import path, include
from coodesh_app import views, api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('articles/', views.gen_article_view, name='articles'),
    path('articles/<int:my_id>/', views.get_article),
    path('test_articles/<int:my_id>/', api_views.SFNArticlesRetrieveUpdateDestroy_.as_view()),
    path('test_articles/', api_views.SFNArticlesList.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='api_token'),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
