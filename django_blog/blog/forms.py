from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import post
from .models import Comment
from taggit.forms import TagWidget

class UserRegisterForm(UserCreationForm):
    """
    Extends UserCreationForm to include email field.
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    Simple form to update User fields (email, first/last name optionally).
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """
    Update profile related fields (bio, avatar).
    """
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

class PostForm(forms.ModelForm):
    """
    ModelForm for Post. We do not include author field in the form:
    author is set automatically from request.user in the view.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your content here...'}),
          
        }


class CommentForm(forms.ModelForm):
    """
    Simple ModelForm for comments. The 'content' field is required,
    and we strip whitespace in clean_content.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a public comment...'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment is too long (max 2000 characters).")
        return content

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g. django, python)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),  # ✅ use TagWidget here
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if editing existing post, show current tags as CSV
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

