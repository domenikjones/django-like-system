from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from like_system.models import Like

DEFAULT_LIKES_APP = 'like_system'

def get_like_app():
    """
    Get the comment app (i.e. "django_comments") as defined in the settings
    """
    # Make sure the app's in INSTALLED_APPS
    comments_app = get_like_app_name()
    if comments_app not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("The LIKE_APP (%r) "\
                                   "must be in INSTALLED_APPS" % settings.COMMENTS_APP)

    # Try to import the package
    try:
        package = import_module(comments_app)
    except ImportError as e:
        raise ImproperlyConfigured("The LIKES APP setting refers to "\
                                   "a non-existing package. (%s)" % e)

    return package

def get_like_app_name():
    """
    Returns the name of the comment app (either the setting value, if it
    exists, or the default).
    """
    return getattr(settings, 'LIKE_APP', DEFAULT_LIKES_APP)

def get_model():
    """
    Returns the comment model class.
    """
    if get_like_app_name() != DEFAULT_LIKES_APP and hasattr(get_like_app(), "get_model"):
        return get_like_app().get_model()
    else:
        return Like

# def get_form():
#     """
#     Returns the comment ModelForm class.
#     """
#     if get_like_app_name() != DEFAULT_LIKES_APP and hasattr(get_like_app(), "get_form"):
#         return get_like_app().get_form()
#     else:
#         return LikeForm

def get_form_target():
    """
    Returns the target URL for the comment form submission view.
    """
    if get_like_app_name() != DEFAULT_LIKES_APP and hasattr(get_like_app(), "get_form_target"):
        return get_like_app().get_form_target()
    else:
        return urlresolvers.reverse("django_comments.views.comments.post_comment")

# def get_flag_url(comment):
#     """
#     Get the URL for the "flag this comment" view.
#     """
#     if get_comment_app_name() != DEFAULT_COMMENTS_APP and hasattr(get_comment_app(), "get_flag_url"):
#         return get_comment_app().get_flag_url(comment)
#     else:
#         return urlresolvers.reverse("django_comments.views.moderation.flag",
#                                     args=(comment.id,))
#
# def get_delete_url(comment):
#     """
#     Get the URL for the "delete this comment" view.
#     """
#     if get_comment_app_name() != DEFAULT_COMMENTS_APP and hasattr(get_comment_app(), "get_delete_url"):
#         return get_comment_app().get_delete_url(comment)
#     else:
#         return urlresolvers.reverse("django_comments.views.moderation.delete",
#                                     args=(comment.id,))
#
# def get_approve_url(comment):
#     """
#     Get the URL for the "approve this comment from moderation" view.
#     """
#     if get_comment_app_name() != DEFAULT_COMMENTS_APP and hasattr(get_comment_app(), "get_approve_url"):
#         return get_comment_app().get_approve_url(comment)
#     else:
#         return urlresolvers.reverse("django_comments.views.moderation.approve",
#                                     args=(comment.id,))