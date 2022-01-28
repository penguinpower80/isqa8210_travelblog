from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, Subquery, OuterRef
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from journey.forms import PostForm, CommentForm
from journey.models import Post, Comment

now = timezone.now()


# to view details of the post from the application
@login_required
def post_detail(request):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    search = request.GET.get('s')
    if search:
        object_list = Post.objects.filter(
            Q(title__icontains=search) |
            Q(visited_places__icontains=search) |
            Q(favorite_place__icontains=search) |
            Q(address__icontains=search) |
            Q(favorite_activity__icontains=search) |
            Q(description__icontains=search) |
            Q(author__email__icontains=search) |
            Q(author__first_name__icontains=search) |
            Q(author__last_name__icontains=search)
        ).order_by('-created')
    else:
        object_list = Post.objects.all().order_by('-publish')

    paginator = Paginator(object_list, 15)  # 15 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'journey/post_detail.html',
                  {
                      'page': page,
                      'posts': posts,
                      'search': search
                  })


# to add new post from the application
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('journey:post_list')
    else:
        form = PostForm()
    return render(request, 'journey/post_new.html', {'form': form})


# to edit the post from the application
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        # update
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_date = timezone.now()
            post.save()
            if request.user.is_superuser:
                return redirect('journey:post_detail')
            else:
                newrequest = HttpRequest()
                newrequest.method = 'GET'
                newrequest.user = request.user
                return travelblog_post(newrequest, post.pk)
    else:
        # edit
        form = PostForm(instance=post)
    return render(request, 'journey/post_edit.html', {'form': form})


# to delete the post from the application
@login_required
def post_delete(request, pk):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    if request.user.is_superuser:
        return redirect('journey:post_detail')
    else:
        return redirect('journey:post_list')


def post_list(request):
    search = request.GET.get('s')
    sort_param = request.GET.get('sort')
    # doing this to not expose details of the database (vs just using real column names in the links)
    if sort_param == '-date':
        sort = '-publish'
    elif sort_param == 'date':
        sort = 'publish'
    elif sort_param == 'comment_count':
        sort = 'comment_count'
    elif sort_param == '-comment_count':
        sort = '-comment_count'
    elif sort_param == 'latest_comment':
        sort = 'latest_comment'
    elif sort_param == '-latest_comment':
        sort = '-latest_comment'
    else:
        sort = '-publish'

    newest = Comment.objects.filter(post=OuterRef('pk')).order_by('-created')
    if search:
        object_list = Post.objects.filter(
            Q(title__icontains=search) |
            Q(visited_places__icontains=search) |
            Q(favorite_place__icontains=search) |
            Q(address__icontains=search) |
            Q(favorite_activity__icontains=search) |
            Q(description__icontains=search) |
            Q(author__email__icontains=search) |
            Q(author__first_name__icontains=search) |
            Q(author__last_name__icontains=search)
        ).annotate(
            comment_count=Count('comments'),
            latest_comment=Subquery(newest.values('created'))
        ).order_by(sort)
    else:
        object_list = Post.objects.all().annotate(
            comment_count=Count('comments'),
            latest_comment=Subquery(newest.values('created'))
        ).order_by(sort)

    paginator = Paginator(object_list, 9)  # 6 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page 
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results 
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'journey/post_list.html',
                  {
                      'page': page,
                      'posts': posts,
                      'search': search,
                      'sort': sort_param
                  })


def travelblog_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # List of active comments for this post 
    comments = post.comments.all().order_by('-created')
    new_comment = None
    if request.method == 'POST':
        # A comment was posted 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet 
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment 
            new_comment.post = post
            new_comment.name = request.user.first_name
            new_comment.email = request.user.email
            # Save the comment to the database 
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'journey/travelblog_post.html',
                  {'post': post, 'comments': comments,
                   'comment_form': comment_form})
