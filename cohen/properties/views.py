# coding: utf-8

"""Views to Propery"""

from django.contrib.postgres.search import SearchVector
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from .models import Property
from .forms import PropertyCreateForm, PropertyDetailForm


class PropertyCreate(CreateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'properties/property_create_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])

        return super(PropertyCreate, self).form_valid(form)


class PropertyUpdate(UpdateView):
    model = Property
    form_class = PropertyDetailForm
    template_name = 'properties/property_update_form.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])

        return super(PropertyUpdate, self).form_valid(form)


class PropertyDetail(DetailView):
    model = Property

    def get_context_data(self, **kwargs):
        qs = []

        if self.object.point:
            lat, lng = self.object.point.tuple

            coordinates = 'POINT({} {})'.format(lat, lng)

            point = GEOSGeometry(coordinates, srid=4326)

            qs = Property.objects.exclude(pk=self.object.pk).filter(
                is_available=True, point__distance_lte=(point, D(km=5)))

        context = super(PropertyDetail, self).get_context_data(**kwargs)
        context['related'] = qs
        return context


class PropertyDelete(DeleteView):
    model = Property
    success_url = reverse_lazy('property-list')


class PropertyList(ListView):
    model = Property

    def get_queryset(self):
        qs = super().get_queryset()

        param = self.request.GET.get('q', None)

        if not param:
            return qs

        return qs.annotate(search=SearchVector(
            'title', 'description', 'address')).filter(search=param)
