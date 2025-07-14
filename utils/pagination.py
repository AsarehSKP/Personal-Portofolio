from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, per_page=6):
    """
    Paginate a queryset and return the page object.
    """
    page = request.GET.get("page", 1)
    paginator = Paginator(queryset, per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items
