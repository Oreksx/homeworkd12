from django.urls import path
from simpleapp.views import NewsSearch

urlpatterns = [
    path('', NewsSearch.as_view()),
]


















