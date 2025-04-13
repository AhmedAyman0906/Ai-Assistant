from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TagListView, QuestionListView, AskQuestionView

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    # Router-generated URLs for ArticleViewSet
    path('', include(router.urls)),
    
    # Other API endpoints
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('ask/', AskQuestionView.as_view(), name='ask-question'),
    
    # Include this if you want API docs just for knowledge app
    # path('docs/', include_docs_urls(title='Knowledge API')),
]