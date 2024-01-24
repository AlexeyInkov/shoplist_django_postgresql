from django.shortcuts import render, reverse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django_filters.views import FilterView

from .models import ShoppingListItem
from .forms import ShoppingListForm
from .filters import ShoppingListFilter

# Create your views here.


class ItemListView(FilterView):
    template_name = "shoplist/list.html"
    context_object_name = "object_list"
    filterset_class = ShoppingListFilter

    def get_user(self):
        if not self.request.user.is_anonymous:
            return self.request.user

    def get_ordering(self):
        self.order = self.request.GET.get("order", "asc")
        selected_ordering = self.request.GET.get("ordering", "count")
        if self.order == "desc":
            selected_ordering = "-" + selected_ordering
        return selected_ordering

    def get_context_data(self, *args, **kwargs):
        context = super(ItemListView, self).get_context_data(*args, **kwargs)
        context["current_order"] = self.get_ordering()
        context["order"] = self.order
        return context

    def get_queryset(self):
        return (
            ShoppingListItem.objects.all()
            .select_related("product")
            .filter(user=self.get_user())
            .order_by(self.get_ordering())
        )


class ItemCreateView(CreateView):
    template_name = "shoplist/create.html"
    model = ShoppingListItem
    fields = "product", "count"
    success_url = reverse_lazy("shoplist:list_items")

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = ShoppingListItem
    template_name = "shoplist/update.html"
    form_class = ShoppingListForm

    def get_success_url(self):
        return reverse("shoplist:list_items")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemDeleteView(DeleteView):
    model = ShoppingListItem
    template_name = "shoplist/delete.html"
    success_url = reverse_lazy("shoplist:list_items")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
