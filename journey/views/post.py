import logging
import shutil

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from journey.forms import PostForm, CommentForm
from journey.models import Post, Comment
from journey.models.favorites import Favorites
from travelblog import settings

now = timezone.now()


@login_required
def _handle_file_upload(request, post):
    new_image_upload = request.FILES.get('image_upload_field', False)
    if new_image_upload:
        image_file = new_image_upload
        path = str(post.id) + '/' + image_file.name
        filename = default_storage.save(path, image_file)
        return request.build_absolute_uri(default_storage.url(filename))
    return False


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


# Saves the new posts form to the database.
# If a file is being uploaded, saves the file and stores the url in the image_url field
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            upload_url = _handle_file_upload(request, post)
            if upload_url:
                post.image_url = upload_url
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
        form = PostForm(request.POST, request.FILES, instance=post)
        logging.warning(request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.updated_date = timezone.now()
            post.save()
            upload_url = _handle_file_upload(request, post)
            if upload_url:
                post.image_url = upload_url
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
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect("journey:post_list")

    # cleanup any files that were uploaded to this particular post
    if default_storage.exists(settings.MEDIA_ROOT + '/' + str(post.id) + '/'):
        shutil.rmtree(settings.MEDIA_ROOT + '/' + str(post.id) + '/', ignore_errors=True)

    post.delete()
    if request.user.is_superuser:
        return redirect('journey:post_detail')
    else:
        return redirect('journey:post_list')


def post_list(request):
    search = request.GET.get('s')
    sort_param = request.GET.get('sort')
    favorite_flag = int(request.GET.get('favorite', 0))
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

    newest = Comment.objects.filter(post=OuterRef('pk')).order_by('-created')[:1]
    object_list = Post.objects.annotate(
        comment_count=Count('comments', distinct=True),
        latest_comment=Subquery(newest.values('created')),
    ).order_by(sort)

    if search:
        object_list = object_list.filter(
            Q(title__icontains=search) |
            Q(visited_places__icontains=search) |
            Q(favorite_place__icontains=search) |
            Q(address__icontains=search) |
            Q(favorite_activity__icontains=search) |
            Q(description__icontains=search) |
            Q(author__email__icontains=search) |
            Q(author__first_name__icontains=search) |
            Q(author__last_name__icontains=search)
        )

    if (request.user.is_authenticated):
        object_list = object_list.annotate(
            is_favorite=Count('favorites', distinct=True, filter=Q(favorites__user=request.user))
        )

        if favorite_flag == 1:
            object_list = object_list.filter(
                is_favorite=1
            )

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

    is_favorite = Favorites.objects.filter(
        post=post,
        user=request.user
    ).count() == 1

    logging.warning(is_favorite)
    return render(request, 'journey/travelblog_post.html',
                  {
                      'post': post,
                      'comments': comments,
                      'comment_form': comment_form,
                      'is_favorite': is_favorite
                  })
