from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError

from apps.core.models import Article


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_article(request):
    try:
        title = request.POST.get('title')
        title_description = request.POST.get('title_description') if 'title_description' in request.POST else ''
        content = request.POST.get('content')
        category = request.POST.get('category') if 'category' in request.POST else None
        tags = request.POST.get('tags') if 'tags' in request.POST else None

        if None in (title, content):
            raise ValidationError

        article = Article.objects.create(
            title=title,
            title_description=title_description,
            author=request.user,
            content=content,
            category=category,
            slug=f'{title}{id}',
            tags=tags,
        )

        return Response({'detail': 'True'}, status=201)
    except ValidationError as e:
        return Response({'detail': f'{e} is required!'}, status=422)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)
    