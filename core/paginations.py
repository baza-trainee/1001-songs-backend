# использование под вопросом

import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasicPagePaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        total_pages = math.ceil(count/self.get_page_size(self.request))
        return Response({
            'total_items': count,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


