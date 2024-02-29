from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http.response import HttpResponse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    View,
)
from django.db.models import OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Apartment, Photo, Video
from django.contrib.auth import get_user_model
from . import forms

# Create your views here.


class ApartmentView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = Apartment
    template_name = "apartments/home.html"
    context_object_name = "apartment_list"

    def get_queryset(self):
        queryset = super(ApartmentView, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)

        first_photo_subquery = Subquery(
            Photo.objects.filter(apartment_id=OuterRef("pk"))
            .order_by("pk")
            .values("photo")[:1]
        )
        queryset = queryset.annotate(first_photo=first_photo_subquery)

        return queryset


class ViewApartmentView(DetailView):
    model = Apartment
    template_name = "apartments/view_apart.html"
    context_object_name = "apartment"

    def get_queryset(self):
        return Apartment.objects.filter(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = Photo.objects.filter(apartment=context["apartment"])
        context["videos"] = Video.objects.filter(apartment=context["apartment"])
        context["paying_dates"] = context["apartment"].get_contract_paying_dates()
        return context


class AddApartmentView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    form_class = forms.AddApartmentForm
    template_name = "apartments/add_apartment.html"
    success_url = "/"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddApartmentView, self).form_valid(form)


class EditApartmentView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "apartments/edit_apart.html"
    model = Apartment
    fields = [
        "country",
        "city",
        "notes",
        "rent_price",
    ]
    
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Apartment, pk=kwargs['pk'], owner=request.user)
        return super(EditApartmentView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(EditApartmentView, self).save(form)


class ReversePublicityView(View):
    def get(self, *args, **kwargs):
        request = self.request
        pk = kwargs["pk"]
        apartment = Apartment.objects.get(pk=pk)
        if request.htmx and request.user == apartment.owner:
            apartment.reverse_public_visibility()
        return HttpResponse("")

class DeleteApartmentView(View):
    def post(self, *args, **kwargs):
        request = self.request
        pk = kwargs["pk"]
        apartment = Apartment.objects.get(pk=pk)
        if request.user == apartment.owner:
            apartment.delete()
        response = HttpResponse()
        response["HX-Redirect"] = "/"
        return response


class AddMediaView(View):
    def get(self, *args, **kwargs):
        request = self.request
        pk = kwargs["pk"]
        apartment = get_object_or_404(Apartment, pk=pk)
        if apartment.owner != request.user:
            return redirect("/")
        videos = Video.objects.filter(apartment=apartment)
        context = {
            "photos": Photo.objects.filter(apartment=apartment),
            "videos": videos,
            "pk": pk,
        }
        return render(request, "apartments/add_media.html", context)


class AddMediaObjectView(View):
    def post(self, *args, **kwargs):
        request = self.request
        pk = kwargs["pk"]
        data = request.FILES
        apartment = get_object_or_404(Apartment, pk=pk)
        if apartment.owner != request.user:
            return redirect("/")

        content_type = data.get("media").content_type

        if "image" in content_type:
            photo = Photo.objects.create(apartment=apartment, photo=data.get("media"))
            return render(
                request, "apartments/components/htmx-add-photo.html", {"photo": photo}
            )
        elif "video" in content_type:
            video = Video.objects.create(apartment=apartment, video=data.get("media"))
            return render(
                request, "apartments/components/htmx-add-video.html", {"video": video}
            )


class DeleteMediaView(View):
    def post(self, *args, **kwargs):
        request = self.request
        pk = kwargs["pk"]
        if request.htmx.target[0] == "p":
            photo = Photo.objects.get(pk=pk)
            if request.user == photo.apartment.owner:
                photo.delete()

        elif request.htmx.target[0] == "v":
            video = Video.objects.get(pk=pk)
            if request.user == video.apartment.owner:
                video.delete()

        return HttpResponse("")
