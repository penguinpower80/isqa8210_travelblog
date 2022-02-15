import logging
import shutil

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, Subquery, OuterRef
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from journey.forms import PostForm, CommentForm
from journey.models import Post, Comment
from journey.models.favorites import Favorites
from travelblog import settings

now = timezone.now()

'''
Small helper function to handle file uploads during the creation or editing of a post.  It uses a non-model field
to upload the file, and if it is populated in the submission, it will save the file in a folder for that post and return 
the absolute url to that file, or False if it didn't exist. 
'''
@login_required
def _handle_file_upload(request, post):
    new_image_upload = request.FILES.get('image_upload_field', False)
    if new_image_upload:
        image_file = new_image_upload
        path = str(post.id) + '/' + image_file.name
        filename = default_storage.save(path, image_file)
        return request.build_absolute_uri(default_storage.url(filename))
    return False

'''
Genate a full list of posts for the superuser.  If the "s" url parameter is detected, it will also filter
the results using that string.  It is also paginated.
'''
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
                  { 'page': page, 'posts': posts, 'search': search }
                  )

'''
Handle adding a new post to the database.  If the request is a post, it validates the form and then
inserts it into the table.  It also calls the _handle_file_upload function to detect and handle saving an image
to disk if necessary.  Since the it uses the post id to create a folder with that id, it must save it first and then 
store the file.
'''
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


'''
Handles editing an existing post.  It first makes sure the user is either a superuser or the post author, 
and then shows the post edit form.  On save, it stores the new data to the database and optionally handles the 
uploaded file. Since the post id already exists, it can do this in one step.  It then redirects to either the 
post_detail list (if superuser) or back to the edit screen (if a normal user)
'''
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            upload_url = _handle_file_upload(request, post)
            if upload_url:
                post.image_url = upload_url
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
        form = PostForm(instance=post)
    return render(request, 'journey/post_edit.html', {'form': form})


# to delete the post from the application
'''
Allows a post author or a superuser to delete a travelblog post.  It also deletes any images associated with that
post. Redirects to thepost_detail screen for the superuser or the post_list for a regular user (author). 
'''
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

'''
Retrieve the posts from the database.  This can be filtered by a search string, and sorted.  It can also be limited to 
only those marked as favorites for that user.
'''
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

'''
Retrieves a single travelblog posting for display.  If a comment form was submitted, it will add it to the comment
table.  If the user is logged in, it will also retrieve if it is in the favorite's table for that user.
'''
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

    if ( request.user.is_authenticated ):
        is_favorite = Favorites.objects.filter(
            post=post,
            user=request.user
        ).count() == 1
    else:
        is_favorite = False

    return render(request, 'journey/travelblog_post.html',
                  {
                      'post': post,
                      'comments': comments,
                      'comment_form': comment_form,
                      'is_favorite': is_favorite
                  })
