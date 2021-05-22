from django import template

register = template.Library()


@register.simple_tag()
def liked_comment(user_like, comment_like):
    like = list(set(user_like) & set(comment_like))
    if len(like) > 0:
        return like[0]
    return False

