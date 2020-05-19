import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


# if I want to register with custom name.
# @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    return Post.published.count()


# used in some templates like as
# {% show_latest_posts 4 %}
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# in addition to Count, Django offers the aggregation functions Avg, Max, Min and Sum
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdonw_format(text):
    return mark_safe(markdown.markdown(text))
