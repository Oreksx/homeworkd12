from django.forms import ModelForm
from news.models import Post, Author, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class NewForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'titlepost', 'textpost', 'posts']

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


































































