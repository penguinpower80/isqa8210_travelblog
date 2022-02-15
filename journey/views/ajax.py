from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from journey.models import Post
from journey.models.favorites import Favorites

'''
This function handles the submission of an ajax call to mark a particular post as a "favorite" - it stores the 
post id and the user id in the favorites cross-reference table. It first checks if it is already a favorite, and only
adds the new record if it doesn't already exist.  Returns 'ok' if it was inserted, or 'exist' if it already existed. 
'''
@login_required
def favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)

    favorite_count = Favorites.objects.filter(
        user=request.user,
        post=post
    ).count()

    if favorite_count == 0:
        thisfavorite = Favorites()
        thisfavorite.user = request.user
        thisfavorite.post = post
        r = thisfavorite.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("exist")

'''
This function handles the ajax call to remove the user-post combination from the favorites table. Returns the number of
rows changed by the call (should be either 0 or 1)
'''
@login_required
def unfavorite(request, pk):
    post = get_object_or_404(Post, pk=pk)

    result = Favorites.objects.filter(
        user=request.user,
        post=post
    ).delete()

    return HttpResponse(result[0])
