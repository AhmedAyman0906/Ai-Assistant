from rest_framework import serializers
from .models import Article, Tag, Question, User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    tag_details = TagSerializer(
        source='tags',
        many=True,
        read_only=True
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'tags', 'tag_details', 'author', 'created_at']
        read_only_fields = ['author', 'created_at', 'tag_details']

    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        article = super().create(validated_data)
        
        # Handle tags
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            tags.append(tag)
        
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags', None)
        
        # Update other fields
        instance = super().update(instance, validated_data)
        
        # Update tags if provided
        if tag_names is not None:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name.strip())
                tags.append(tag)
            instance.tags.set(tags)
        
        return instance
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answer_text', 'asked_by', 'asked_at']
        read_only_fields = ['id', 'answer_text', 'asked_by', 'asked_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']
