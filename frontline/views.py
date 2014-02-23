from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.views.generic.edit import FormView
from .models import Entry, ImageEntry

def save(request):
    for item in  request.POST.items():
        name = item[0]
        entry = Entry.objects.get_or_create(name=name)[0]
        entry.data = item[1]
        entry.save()
        cache.set('entry_%s' % name, entry)

    return HttpResponse('ok')


from .forms import RichtextForm


def richtext_form(request, name):
    entry = Entry.objects.get_or_create(name=name)[0]
    print entry.data
    form = RichtextForm(initial={'data': entry.data})
    return render_to_response('frontline/forms/richtext.html',
                              {'form': form},
                              context_instance=RequestContext(request))

class RichtextFormView(FormView):
    form_class = RichtextForm
    template_name = 'frontline/forms/richtext.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(self.object.data)


    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        try:
            entry = Entry.objects.filter(name=self.kwargs['name'])[0]
            kwargs['instance'] = entry
        except IndexError:
            kwargs['initial'] = {'name': self.kwargs['name']}
        return form_class(**kwargs)


from .forms import ImageUploadForm


class ImageUploadFormView(FormView):
    form_class = ImageUploadForm
    template_name = 'frontline/forms/image_upload_form.html'

    def form_valid(self, form, tag_option=None):
        self.object = form.save()
        if tag_option == 'need_reload':
            return render_to_response('frontline/need_reload.html')
        return HttpResponse('ok')

    def post(self, request, *args, **kwargs):
        tag_option = request.GET.get('option', None)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, tag_option)
        else:
            return self.form_invalid(form)
        

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        try:
            image_entry = ImageEntry.objects.filter(name=self.kwargs['name'])[0]
            kwargs['instance'] = image_entry
        except IndexError:
            kwargs['initial'] = {'name': self.kwargs['name']}
        return form_class(**kwargs)