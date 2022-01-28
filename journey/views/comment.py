from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from journey.forms import CommentForm
from journey.models import Comment


# comment list view from the application
@login_required
def comment_list(request):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    search = request.GET.get('s')
    if search:
        object_list = Comment.objects.filter(
            Q(body__icontains=search) | Q(name__icontains=search) | Q(email__icontains=search)).order_by('-created')
    else:
        object_list = Comment.objects.all().order_by('-created')
    paginator = Paginator(object_list, 15)  # 15 posts in each page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)

    return render(request,
                  'journey/comment_list.html',
                  {
                      'page': page,
                      'comments': comments,
                      'search': search
                  })


# to edit the comment from the application
@login_required
def comment_edit(request, pk):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        # update
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updated_date = timezone.now()
            comment.save()
            return redirect('journey:comment_list')
    else:
        # edit
        form = CommentForm(instance=comment)
    return render(request, 'journey/comment_edit.html', {'form': form})


# to delete the comment from the application
@login_required
def comment_delete(request, pk):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('journey:comment_list')
