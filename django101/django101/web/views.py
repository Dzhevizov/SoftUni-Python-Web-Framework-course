from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render

from django101.web.models import Todo


def index(request):
    context = {
        'title': 'Function based view',
    }
    return render(request, 'index.html', context)


class IndexView(views.View):
    def get(self, request):
        context = {
            'title': 'Class based view',
        }
        return render(request, 'index.html', context)


class IndexTemplateView(views.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Class based view with template'
        return context


class RedirectToIndexView(views.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if ...:
            return 'place1'
        else:
            return 'place2'


class TodosListView(views.ListView):
    model = Todo
    template_name = 'todos-list.html'
    ordering = ('-category__name', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # queryset.prefetch_related('category_set')

        title_filter = self.request.GET.get('filter', None)
        if title_filter:
            queryset = queryset.filter(title__contains=title_filter)

        return queryset


class TodoDetailsView(views.DetailView):
    model = Todo
    template_name = 'todo-details.html'


class TodoCreateView(views.CreateView):
    model = Todo
    template_name = 'todo-create.html'
    success_url = reverse_lazy('todos list')
    fields = '__all__'

