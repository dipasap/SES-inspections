# noinspection PyPep8Naming
import json as JSON
import re
from collections import OrderedDict
from urllib.parse import urlencode
from django import template
from django.apps import apps
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
register = template.Library()

@register.simple_tag(takes_context=True)
def active_if(context, *view_name):
    if context.request.resolver_match.view_name in view_name:
        return 'active'
    return ''

@register.simple_tag(takes_context=True)
def menu_open_if(context, *view_name):
    if context.request.resolver_match.view_name in view_name:
        return 'menu-is-opening menu-open'
    return ''
