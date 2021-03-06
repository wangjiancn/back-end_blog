import json
import os

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from acl.auth_wrap import token_optional
from acl.auth_wrap import token_required
from utils.api_response import APIResponse
from utils.tool import parse_query_string
from .action import actions
from .models import Category
from .models import Post
from .models import Tag


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, r, *args, **kwargs):
        if kwargs.get('cat_id'):
            cat = Category.objects.active().get_or_api_404(id=kwargs.get('cat_id'))
            return APIResponse(cat.to_dict())
        else:
            cats = Category.objects.active().all().pagination()
            return APIResponse(cats)


@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):

    def get(self, r, *args, **kwargs):
        pagination, order_by, filters, defer, search = parse_query_string(r.GET, 'post')
        if kwargs.get('tag_id'):
            tag = Post.objects.active().defer(*defer).get_or_api_404(id=kwargs.get('tag_id'))
            return APIResponse(tag.to_dict())
        else:
            tags = Tag.objects.active().defer(*defer).order_by(*order_by).pagination(**pagination)
            return APIResponse(tags)


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):
    @method_decorator(token_optional, name='dispatch')
    def get(self, r, *args, **kwargs):
        pagination, order_by, filters, defer, search = parse_query_string(r.GET, 'post')
        if kwargs.get('post_id'):
            post = Post.objects.active().defer(*defer).get_or_api_404(id=kwargs.get('post_id'))
            post.add_view_count()
            return APIResponse(post.to_dict())
        else:
            if r.user and r.user.username:
                share_filters = {k: v for k, v in filters.items()
                                 if k not in ['private', 'is_publish','rate__gt']}
                query = search & (Q(**filters) | Q(author=r.user, **share_filters))
            else:
                query = search & Q(**filters)
            posts = Post.objects.active(query).defer(*defer).order_by(*order_by).pagination(
                **pagination)
            return APIResponse(posts)

    @method_decorator(token_required, name='dispatch')
    def post(self, r, *args, **kwargs):
        data = json.loads(r.body)
        # tags = data.pop('tags') if 'tags' in data.keys() else []
        if kwargs.get('post_id'):
            post = Post.objects.get_or_api_404(id=kwargs.get('post_id')).update_fields(**data)
        else:
            post = Post.create(**data, author=r.user)
        return APIResponse(post.to_dict())

    @method_decorator(token_required, name='dispatch')
    def delete(self, r, *args, **kwargs):
        if kwargs.get('post_id'):
            Post.objects.active(id=kwargs.get('post_id')).delete()
            return APIResponse()
        else:
            return APIResponse(code=10003)


def index(r):
    return APIResponse(dict(name='hello world', hostname=os.environ.get('HOSTNAME', 'none')))


@require_POST
@csrf_exempt
def action(r, *args, **kwargs):
    return actions.run_action(r, *args, **kwargs)
