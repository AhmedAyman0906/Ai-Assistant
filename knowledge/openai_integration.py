import openai
from django.conf import settings
from .models import Article

def generate_answer_from_articles(question):
    """
    Generates an answer in Arabic based on available articles using OpenAI
    """
    try:
        # Initialize the client with the API key
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Get all articles and prepare context
        articles = Article.objects.all()
        context = "\n\n".join([f"العنوان: {a.title}\nالمحتوى: {a.content}" for a in articles])
        
        # Generate the answer using OpenAI
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
        
    except openai.APIError as e:
        return f"حدث خطأ في الاتصال ب OpenAI: {str(e)}"
    except Exception as e:
        return f"حدث خطأ غير متوقع: {str(e)}"