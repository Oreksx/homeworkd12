from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from news.models import Post
from django.contrib.auth.mixins import PermissionRequiredMixin

class News(View):

    def get(self, request):
        news = Post.objects.order_by('-datepost')
        p = Paginator(news, 10)
        news = p.get_page(request.GET.get('page', 1))
        data = {
            'news': news,
        }
        return render(request, 'news.html', data)



































































