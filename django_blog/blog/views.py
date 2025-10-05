# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q
from .models import Post, Tag
from .forms import PostForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')
    
#POST CRUD VIEW
class PostListView(ListView):
    """Public view: List all posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    """Public view: View a single post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post (only logged-in users)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a post (only by its author)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post (only by its author)"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a comment for a specific post.
    URL: /posts/<post_pk>/comments/new/
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # used if user visits the 'new' page directly
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # cache the post on the view instance for use in form_valid/get_context_data
        self.post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # assign the post and the author automatically before saving
        form.instance.post = self.post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.post.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post'] = self.post
        return ctx


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit a comment. Only the comment author can edit.
    URL: /comments/<pk>/edit/
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    raise_exception = True  # unauthorized -> 403

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment. Only the comment author can delete.
    URL: /comments/<pk>/delete/
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    raise_exception = True

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('author').prefetch_related('tags')
        q = self.request.GET.get('q', '').strip()
        tag = self.request.GET.get('tag', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        if tag:
            # allow tag slug or name
            qs = qs.filter(tags__slug=tag) | qs.filter(tags__name__iexact=tag)
            qs = qs.distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['tag_param'] = self.request.GET.get('tag', '')
        return ctx


class TagPostListView(PostListView):
    """
    ListView for posts filtered by tag slug in URL.
    """
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=slug)
        qs = super().get_queryset().filter(tags=tag)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_tag'] = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)  # saves instance
        tags_csv = form.cleaned_data.get('tags', '')
        self._assign_tags_to_post(self.object, tags_csv)
        return response

    def _assign_tags_to_post(self, post, tags_csv):
        tag_names = [t.strip() for t in tags_csv.split(',') if t.strip()]
        tags_objs = []
        from .models import Tag
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            # ensure slug creation
            if tag_obj.name != name:
                tag_obj.name = name
                tag_obj.save()
            tags_objs.append(tag_obj)
        post.tags.set(tags_objs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        tags_csv = form.cleaned_data.get('tags', '')
        self._assign_tags_to_post(self.object, tags_csv)
        return response

    def _assign_tags_to_post(self, post, tags_csv):
        tag_names = [t.strip() for t in tags_csv.split(',') if t.strip()]
        tags_objs = []
        from .models import Tag
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            if tag_obj.name != name:
                tag_obj.name = name
                tag_obj.save()
            tags_objs.append(tag_obj)
        post.tags.set(tags_objs)
