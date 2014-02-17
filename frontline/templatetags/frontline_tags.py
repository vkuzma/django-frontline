from django import template
# from django.auth import user 
from django.template.loader import render_to_string
from django.core.cache import cache
from ..models import Entry


register = template.Library()


def getEntry(anchor):
    entry = cache.get('entry_%s' % anchor)
    if entry:
        return entry
    else:
        try:
            entry = Entry.objects.filter(anchor=anchor)[0]
            cache.set('entry_%s' % anchor, entry, timeout=5*60)
            return entry
        except IndexError:
            return None


@register.simple_tag(takes_context=True)
def frontline_edit(context, anchor, editor='', embed_type='inline'):
    entry = getEntry(anchor)
    if context['request'].user.is_staff:
        data = entry.data if entry else 'enter_text'
        return '<span class="frontline-edit %s %s" data-anchor=%s>%s</span>' % (editor, embed_type, anchor, data)
    else:
        return entry.data


@register.simple_tag(takes_context=True)
def live_edit_ct(context, page, region):
    if context['request'].user.is_staff:
        return '<a class="live-edit-contenttype-edit" href="/admin/page/page/%s/#tab_%s" target="_blank">edit in cms</a>' % (page.id, region)
    return ''


from feincms.module.page.models import Page
from feincms.module.medialibrary.models import MediaFile


@register.simple_tag(takes_context=True)
def frontline_media(context):
    if context['request'].user.is_staff:
        content = {
            'pages': Page.objects.all(),
            'mediafiles': MediaFile.objects.all()
        }
        return render_to_string('frontline/media_includes.html', content)
    return ''
