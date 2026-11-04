from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Every list endpoint is paginated: `?page=<n>&page_size=<m>`.
    Responses: {"count", "next", "previous", "results"}.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
