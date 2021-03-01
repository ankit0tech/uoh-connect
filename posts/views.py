from django.shortcuts import render, get_object_or_404
from posts.models import Post, Comment
from accounts.models import UserProfile
from posts.forms import CreatePostForm, CreateCommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponseRedirect


class CreatePost(LoginRequiredMixin, CreateView):
    form_class= CreatePostForm
    model = Post
    # success_url = reverse_lazy('posts:details', )

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.created_at = timezone.now()
        self.object.user = self.request.user
        userprofile = UserProfile.objects.get(user=self.object.user.id)
        self.object.department = userprofile.department
        self.object.save()
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CreatePostForm
    model = Post
    success_url = reverse_lazy('posts:list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    # def get_pk(self):
    #     self.object = 

class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')

class PostList(ListView):
    model = Post

# class PostDetail(DetailView):
#     model = Post

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments

    if request.method == "POST":
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.user = request.user
            user_comment.save()
            return HttpResponseRedirect(reverse('posts:details', kwargs={'pk': post.pk}))
    else:
        comment_form = CreateCommentForm

    return render(request, 'posts/post_detail.html', {'post': post, 'comment_form': comment_form,})


#############################
#    Views for Comment      #
#############################

class CreateComment(LoginRequiredMixin, CreateView):

    form_class = CreateCommentForm
    model = Comment

    def get_success_url(self):
        return reverse_lazy('posts:details',kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.created_at = timezone.now()
        self.object.user = self.request.user
        self.object.post = Post.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return super().form_valid(form)
    


# def test_func(request):
#     comment = Comment.objects.get(pk=request.pk)
#     if request.user == comment.user:
#         return True
#     return False

# @user_passes_test(test_func)
@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return HttpResponseRedirect(reverse_lazy('posts:details', kwargs={'pk': post_pk}))
