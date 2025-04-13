from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, Tag, Question
from .serializers import ArticleSerializer, TagSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import openai
from django.conf import settings

# Initialize OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer_from_articles(question):
    """
    Generates an Arabic answer based on available articles using OpenAI
    """
    try:
        # Get all articles and prepare context
        articles = Article.objects.all()
        context = "\n\n".join([f"العنوان: {a.title}\nالمحتوى: {a.content}" for a in articles])
        
        # Generate the answer
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "أنت مساعد ذكي يجيب على أسئلة الموظفين بناءً على المقالات المتاحة. أجب باللغة العربية."
                },
                {
                    "role": "user",
                    "content": f"السؤال: {question}\n\nالمقالات المتاحة:\n{context}"
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"عذرًا، حدث خطأ أثناء معالجة سؤالك: {str(e)}"

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'created_at']
    search_fields = ['title', 'content', 'tags__name']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-asked_at')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['asked_by', 'asked_at']
    search_fields = ['question_text']

class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question_text = request.data.get('question')
        if not question_text:
            return Response({'error': 'لم يتم تقديم سؤال'}, status=400)

        answer_text = generate_answer_from_articles(question_text)

        question = Question.objects.create(
            question_text=question_text,
            answer_text=answer_text,
            asked_by=request.user
        )

        return Response({
            'question': question_text,
            'answer': answer_text,
            'question_id': question.id,
            'asked_at': question.asked_at
        })