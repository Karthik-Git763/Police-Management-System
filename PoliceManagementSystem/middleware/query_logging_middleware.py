import time
from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class QueryLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Mark the start time of the request
        request.start_time = time.time()

    def process_response(self, request, response):
        # Calculate how long the request took
        total_time = time.time() - request.start_time
        queries = connection.queries

        # Log queries to a text file
        with open("db_queries.log", "a") as log_file:
            log_file.write(f"\n[REQUEST PATH]: {request.path}\n")
            log_file.write(f"[TOTAL TIME]: {total_time:.2f} seconds\n")
            log_file.write(f"[NUMBER OF QUERIES]: {len(queries)}\n")
            for query in queries:
                log_file.write(
                    f"\n[TIME]: {query['time']} seconds\n[SQL]: {query['sql']}\n"
                )

        return response
