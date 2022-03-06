from django.contrib import admin
from django.urls import path, include
from coodesh_app import views, api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('articles/', views.gen_article_view, name='articles'),
    # path('articles/<int:my_id>/', views.get_article),
    path('articles/<int:my_id>/', api_views.SFNArticlesRetrieveUpdateDestroy_.as_view()),
    path('articles/', api_views.SFNArticlesList.as_view()),
    
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
