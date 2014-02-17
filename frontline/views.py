from django.http import HttpResponse
from django.core.cache import cache
from .models import Entry

def save(request):
    for item in  request.POST.items():
        anchor = item[0]
        entry = Entry.objects.get_or_create(anchor=anchor)[0]
        entry.data = item[1]
        entry.save()
        cache.set('entry_%s' % anchor, entry)

    return HttpResponse('ok')