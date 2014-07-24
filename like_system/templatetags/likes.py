from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.contrib.contenttypes.models import ContentType

import like_system

register = template.Library()


class BaseLikeNode(template.Node):
    """
    Base helper class (abstract) for handling the get_like_* template tags.
    """

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_comment_list/count/form and return a Node."""
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            return cls(
                object_expr = parser.compile_filter(tokens[2]),
                as_varname = tokens[4],
            )

        # {% get_whatever for app.model pk as varname %}
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype = BaseLikeNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3]),
                as_varname = tokens[5]
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])

    @staticmethod
    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get_by_natural_key(app, model)
        except ValueError:
            raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tagname, app, model))

    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, like=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("Like nodes must be given either a literal object or a ctype and object pk.")
        self.like_model = like_system.get_model()
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr
        self.like = like

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''

    def get_query_set(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.like_model.objects.none()

        qs = self.like_model.objects.filter(
            content_type = ctype,
            object_pk    = smart_text(object_pk),
            site__pk     = settings.SITE_ID,
        )
        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        raise NotImplementedError



class LikeListNode(BaseLikeNode):
    """Insert a list of comments into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return list(qs)

class LikeCountNode(BaseLikeNode):
    """Insert a count of likes into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return qs.count()

class LikeLinkNode(BaseLikeNode):
    """Insert a count of likes into the context."""
    def get_context_value_from_queryset(self, context, qs):
        obj, pk = self.get_target_ctype_pk(context)

        return reverse('like_system-like', kwargs={'content_type':obj.model, 'object_pk':pk })

class UnlikeLinkNode(BaseLikeNode):
    """Insert a count of likes into the context."""
    def get_context_value_from_queryset(self, context, qs):
        obj, pk = self.get_target_ctype_pk(context)

        return reverse('like_system-unlike', kwargs={'content_type':obj.model, 'object_pk':pk })



@register.tag
def get_like_count(parser, token):
    """
    Syntax::

        {% get_like_count for [object] as [varname]  %}
        {% get_like_count for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_like_count for event as like_count %}
        {{ like_count }}
    """

    return LikeCountNode.handle_token(parser, token)

@register.tag
def get_like_list(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_like_list for [object] as [varname]  %}
        {% get_like_list for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_like_list for event as like_list %}
        {% for like in get_like_list %}
            ...
        {% endfor %}

    """
    return LikeListNode.handle_token(parser, token)


@register.tag
def get_like_link(parser, token):
    """
    Get the permalink for a comment, optionally specifying the format of the
    named anchor to be appended to the end of the URL.

    Example::
        {% get_comment_permalink comment "#c%(id)s-by-%(user_name)s" %}
    """

    return LikeLinkNode.handle_token(parser, token)

@register.tag
def get_unlike_link(parser, token):
    """
    Get the permalink for a comment, optionally specifying the format of the
    named anchor to be appended to the end of the URL.

    Example::
        {% get_comment_permalink comment "#c%(id)s-by-%(user_name)s" %}
    """

    return UnlikeLinkNode.handle_token(parser, token)