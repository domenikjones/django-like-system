from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.http.response import HttpResponse, HttpResponseRedirect

from like_system.models import Like


def like(request, content_type=None, object_pk=None):
    # validate the url parameters
    try:
        ct = ContentType.objects.get(model=content_type)
        site = get_current_site(request)
    except:
        return HttpResponse(False)

    # make this unique
    try:
        like = Like.objects.get(user=request.user,
                                content_type=ct,
                                site=site,
                                object_pk=object_pk
        )
    except:
        like = Like(user=request.user,
                    content_type=ct,
                    site=site,
                    object_pk=object_pk,
        )
        like.save()

    # return path given in url
    try:
        return HttpResponseRedirect(request.GET.get('return'))
    except:
        pass

    return HttpResponse(like)


def unlike(request, content_type=None, object_pk=None):
    # validate the url parameters
    try:
        ct = ContentType.objects.get(model=content_type)
        site = get_current_site(request)
        # delete unique like
        Like.objects.get(user=request.user,
                         content_type=ct,
                         site=site,
                         object_pk=object_pk
        ).delete()
    except:
        pass

    # return path given in url
    try:
        return HttpResponseRedirect(request.GET.get('return'))
    except:
        pass

    return HttpResponse(True)