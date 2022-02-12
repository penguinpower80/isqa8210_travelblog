from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from journey.forms import CommentForm
from journey.models import Comment


'''
Create a list of all comments in the system, restricted to the super user.  If the s parameter is passed,
it will filter on the comment body, the name, and email fields.  It uses pagination.
'''
@login_required
def comment_list(request):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    search = request.GET.get('s')
    if search:
        # search on body, commentor name, or commentor email
        object_list = Comment.objects.filter(
            Q(body__icontains=search) | Q(name__icontains=search) | Q(email__icontains=search)).order_by('-created')
    else:
        object_list = Comment.objects.all().order_by('-created')
    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request,
                  'journey/comment_list.html',
                  {
                      'page': page,
                      'comments': comments,
                      'search': search
                  })


'''
Retrieve a comment from the database and handle submission of the comment edit form.  Restricted to the superuser.
'''
@login_required
def comment_edit(request, pk):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updated_date = timezone.now()
            comment.save()
            return redirect('journey:comment_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'journey/comment_edit.html', {'form': form})


'''
Allows a super user to delete a comment from the database and redirects back to the comment list.
'''
@login_required
def comment_delete(request, pk):
    if not request.user.is_superuser:
        return redirect("journey:post_list")
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('journey:comment_list')
