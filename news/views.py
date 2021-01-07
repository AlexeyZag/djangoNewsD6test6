from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, User, Category
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin





class AddProtectedView(PermissionRequiredMixin, CreateView):
    template_name = 'add_article.html'
    form_class = PostForm
    login_url='/accounts/login'
    permission_required = ('news.add_post')
    model = Post
    queryset = Post.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit= False)
        author = self.request.user
        id = Author.objects.get(author= User.objects.get(username = author)).id
        self.object.author_id = id
        self.object.save()
        return  super().form_valid(form)

class AuthorsList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.order_by('-id')

class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = self.request.user
        a = 'Категории: '
        c = []
        for i in Post.objects.get(pk=id).categories.all().values('tag'):
            a += (i['tag'] + ' ')
            c.append(i['tag'])

        b = {}
        for tag in c:
            for name in range(len(Category.objects.filter(tag=tag).values('subscribers__username'))):
                if str(user) in Category.objects.filter(tag=tag).values('subscribers__username')[name].values():
                    b[tag] = True
                    break
                else:
                    b[tag] = False
        context['categories'] = a
        context['user'] = user
        context['c'] = c
        context['tags'] = b
        return context

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'add_article.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchDetail(DetailView):
    model = Post
    template_name = 'search_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()








