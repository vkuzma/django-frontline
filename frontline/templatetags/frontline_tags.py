from django import template
# from django.auth import user 
from django.template.loader import render_to_string
from django.core.cache import cache
from ..models import Entry, ImageEntry


register = template.Library()


def getEntry(name):
    # entry = cache.get('entry_%s' % name)
    # if entry:
    #     return entry
    # else:
    try:
        entry = Entry.objects.filter(name=name)[0]
        cache.set('entry_%s' % name, entry, timeout=5*60)
        return entry
    except IndexError:
        return None


def getImageEntry(name):
    # image_entry = cache.get('image_entry_%s' % name)
    # if image_entry:
    #     return image_entry
    # else:
    try:
        image_entry = ImageEntry.objects.filter(name=name)[0]
        cache.set('image_entry_%s' % name, image_entry, timeout=5*60)
        return image_entry
    except IndexError:
        return None


@register.simple_tag(takes_context=True)
def frontline_edit(context, name, editor='', embed_type='inline'):
    entry = getEntry(name)
    if context['request'].user.is_staff:
        data = entry.data if entry else 'enter_text'
        return '<span class="frontline-edit %s %s" data-name=%s><a class="frontline-edit-btn" href="#"><span class="frontline-icon-edit"></span></a><span class="frontline-content">%s</span></span>' % (editor, embed_type, name, data)
    else:
        return entry.data


@register.simple_tag(takes_context=True)
def frontline_image_edit(context, name, **kwargs):
    if context['request'].user.is_staff:
        return '<span class="frontline-image-edit" data-name="%s" data-option="%s"><a href="" class="frontline-image-edit"><span class="frontline-icon-edit"></span></a></span>' % (name, kwargs.get('option'))
    return ''


@register.simple_tag(takes_context=True)
def frontline_image(context, name, **kwargs):
    image_entry = getImageEntry(name)
    if image_entry and image_entry.data:
        if kwargs.get('render_as') == 'url':
            return image_entry.data.url
        elif kwargs.get('render_as') == 'div':
            return '<div id="%s" style="background-image: url(%s);"></div>' % (name, image_entry.data.url)
        return '<img id="%s" src="%s">' % (name, image_entry.data.url)


from feincms.module.page.models import Page
from feincms.module.medialibrary.models import MediaFile


@register.simple_tag(takes_context=True)
def frontline_media(context):
    if context['request'].user.is_staff:
        return render_to_string('frontline/media_includes.html')
    return ''

