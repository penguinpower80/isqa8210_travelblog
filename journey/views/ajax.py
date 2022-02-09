import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from journey.models import Post
from journey.models.favorites import Favorites


@login_required
def favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)

    favcount = Favorites.objects.filter(
        user=request.user,
        post=post
    ).count()

    if favcount == 0:
        thisfavorite = Favorites()
        thisfavorite.user = request.user
        thisfavorite.post = post
        r = thisfavorite.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("exist")

    return HttpResponse(status=500)

@login_required
def unfavorite(request, pk):
    post = get_object_or_404(Post, pk=pk)

    result = Favorites.objects.filter(
        user=request.user,
        post=post
    ).delete()

    return HttpResponse(result[0])