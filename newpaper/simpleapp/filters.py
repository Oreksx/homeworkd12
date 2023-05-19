from django_filters import FilterSet

from news.models import Post

class NewFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'datepost': ['gte'],
            'titlepost': ['icontains'],
            'author__user__username': ['icontains'],
        }







































































