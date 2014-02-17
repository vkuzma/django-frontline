from django import template
# from django.auth import user 
from django.conf import settings
from django.template.loader import render_to_string
from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError
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
def live_edit_simple(context, anchor, editor=''):
    entry = getEntry(anchor)
    if context['request'].user.is_authenticated():
        # if kwargs.get('tynimce', None):
        #     print "OK"
        editor = 'class="%s"' % editor
        if entry:
            return '<span %s live-editable-simple data-anchor=%s>%s</span>' % (editor, anchor, entry.data)
        return '<span %s live-editable-simple data-anchor=%s>enter_text</span>' % (editor, anchor)
    else:
        return entry.data
    

@register.simple_tag(takes_context=True)
def live_edit_richtext(context, anchor):
    entry = getEntry(anchor)
    if context['request'].user.is_authenticated():
        if entry:
            rendered_content = '<span live-editable-richtext data-anchor=%s>%s</span>' % (anchor, entry.data)
        else:
            rendered_content = '<span live-editable-richtext data-anchor=%s>enter_text</span>' % anchor
        return rendered_content + '<button href="" btn-data-anchor=%s class="live-edit-richtext-btn">edit richtext</button>' % anchor
    else:
        return entry.data


@register.simple_tag(takes_context=True)
def live_edit_ct(context, page, region):
    if context['request'].user.is_authenticated():
        return '<a class="live-edit-contenttype-edit" href="/admin/page/page/%s/#tab_%s" target="_blank">edit in cms</a>' % (page.id, region)
    return ''


@register.simple_tag(takes_context=True)
def live_edit_css(context):
    if context['request'].user.is_authenticated():
        return '<link rel="stylesheet" type="text/css" href="/static/stylesheets/style.css">'
    return ''


from feincms.module.page.models import Page
from feincms.module.medialibrary.models import MediaFile


@register.simple_tag(takes_context=True)
def live_edit_js(context):
    if context['request'].user.is_authenticated():
        content = {
            'pages': Page.objects.all(),
            'mediafiles': MediaFile.objects.all()
        }
        return render_to_string('live_edit/js_includes.html', content)
    return ''


@register.simple_tag(takes_context=True)
def live_edit_panel(context):
    if context['request'].user.is_authenticated():
        return render_to_string('live_edit/panel.html')
    return ''