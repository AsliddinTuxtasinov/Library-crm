# Importing the necessary module for pagination.
from rest_framework import pagination, response


# Defining a custom pagination class that inherits from PageNumberPagination.
class CustomPagination(pagination.PageNumberPagination):
    # Setting the default page size for the pagination.
    page_size = 10
    # Query parameter to dynamically control the page size.
    page_size_query_param = "page_size"

    # Setting the maximum page size allowed.
    max_page_size = 100
    # Specifying the query parameter to use for controlling the page.
    page_query_param = "page"

    # Overriding the method to customize the paginated response format.
    def get_paginated_response(self, data):
        return response.Response(
            data={
                "success": True,
                # Link to the next page of results, if available.
                # "Next": self.get_next_link(),
                # "Next": self.get_https_link(self.get_next_link()),
                # Link to the previous page of results, if available.
                # "previous": self.get_previous_link(),
                # "previous": self.get_https_link(self.get_previous_link()),
                # Total count of items across all pages.
                "count": self.page.paginator.count,
                # Actual data for the current page.
                "result": data,
            }
        )

    # For https requests
    # @staticmethod
    # def get_https_link(link):
    #     if link is not None:
    #         return link.replace("http://", "https://")
    #     return None
