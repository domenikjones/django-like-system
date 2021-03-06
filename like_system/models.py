from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseLikeAbstractModel(models.Model):
    """
    An abstract base class that any custom like models probably should subclass.
    """

    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s"
    )
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    # Metadata about the comment
    site = models.ForeignKey(Site)

    class Meta:
        abstract = True

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        try:
            return reverse("likes-url-redirect",
                           args=(self.content_type_id, self.object_pk)
            )
        except:
            return ('/')




@python_2_unicode_compatible
class Like(BaseLikeAbstractModel):
    """
    A user like about some object.
    """

    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                    blank=True, null=True, related_name="%(class)s_comments")
    user_url = models.URLField(_("user's URL"), blank=True)


    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), default=None)

    # Manager
    # objects = LikeManager()

    class Meta:
        db_table = "django_like_system"
        ordering = ('-submit_date',)
        verbose_name = _('like')
        verbose_name_plural = _('likes')

    def __str__(self):
        if self.user.username:
            return "%s" % (self.user.username)
        else:
            return "N/A"


    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = timezone.now()
        super(Like, self).save(*args, **kwargs)

    # def _get_userinfo(self):
    #     """
    #     Get a dictionary that pulls together information about the poster
    #     safely for both authenticated and non-authenticated comments.
    #
    #     This dict will have ``name``, ``email``, and ``url`` fields.
    #     """
    #     if not hasattr(self, "_userinfo"):
    #         userinfo = {
    #             "name": self.user_name,
    #             "email": self.user_email,
    #             "url": self.user_url
    #         }
    #         if self.user_id:
    #             u = self.user
    #             if u.email:
    #                 userinfo["email"] = u.email
    #
    #             # If the user has a full name, use that for the user name.
    #             # However, a given user_name overrides the raw user.username,
    #             # so only use that if this comment has no associated name.
    #             if u.get_full_name():
    #                 userinfo["name"] = self.user.get_full_name()
    #             elif not self.user_name:
    #                 userinfo["name"] = u.get_username()
    #         self._userinfo = userinfo
    #     return self._userinfo
    # userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)
    #
    # def _get_name(self):
    #     return self.userinfo["name"]
    #
    # def _set_name(self, val):
    #     if self.user_id:
    #         raise AttributeError(_("This comment was posted by an authenticated "\
    #                                "user and thus the name is read-only."))
    #     self.user_name = val
    # name = property(_get_name, _set_name, doc="The name of the user who posted this comment")
    #
    # def _get_email(self):
    #     return self.userinfo["email"]
    #
    # def _set_email(self, val):
    #     if self.user_id:
    #         raise AttributeError(_("This comment was posted by an authenticated "\
    #                                "user and thus the email is read-only."))
    #     self.user_email = val
    # email = property(_get_email, _set_email, doc="The email of the user who posted this comment")
    #
    # def _get_url(self):
    #     return self.userinfo["url"]
    #
    # def _set_url(self, val):
    #     self.user_url = val
    # url = property(_get_url, _set_url, doc="The URL given by the user who posted this comment")
    #
    # def get_absolute_url(self, anchor_pattern="#c%(id)s"):
    #     return self.get_content_object_url() + (anchor_pattern % self.__dict__)
    #
    # def get_as_text(self):
    #     """
    #     Return this comment as plain text.  Useful for emails.
    #     """
    #     d = {
    #         'user': self.user or self.name,
    #         'date': self.submit_date,
    #         'comment': self.comment,
    #         'domain': self.site.domain,
    #         'url': self.get_absolute_url()
    #     }
    #     return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d
