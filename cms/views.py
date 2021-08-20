from django.contrib.auth.decorators import login_required
from  django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone

from cms.models import Post, Comment
from cms.forms import PostForm, CommentForm
#from cms.models import Post

# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request,"post_list.html", {'posts': posts})

def about(request):
    return render(request, "about.html")

# def page(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # return HttpResponse(post)
#     return render(request, "page.html", {'post': post})

@login_required
def post_create(request):
    form = PostForm()
    if (request.method == 'POST'):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post= form.save(commit=False)
            post.author = request.user
            post.published_date =  timezone.now()
            post.save()
            return redirect('home')

    return render(request, "post_create.html", {'form': form})


def post_detail(request, pk):
    template_name = 'page.html'
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})