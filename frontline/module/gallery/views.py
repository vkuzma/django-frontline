from django.views.generic import FormView


class GalleryFormView(FormView):
    def post(self, request, *args, **kwargs):
        tag_option = request.GET.get('option', None)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, tag_option)
        else:
            return self.form_invalid(form)