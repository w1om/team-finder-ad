from django.core.paginator import Paginator

def paginate_queryset(request, queryset, per_page):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)