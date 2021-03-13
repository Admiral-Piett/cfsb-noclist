import sys


def retry_wrapper(func):
    """
    Retry decorator for http requests

        This decorator is tested via the noclist_client tests.

    :param func: function to wrap
    :return: func return values
    """
    global retry_count
    retry_count = 0

    def retry(*args, **kwargs):
        global retry_count
        try:
            response = func(*args, **kwargs)
            # Reset retry count since this call was successful
            retry_count = 0
            return response
        except Exception as e:
            print(f"{func.__name__} FAILURE - {e}", file=sys.stderr)
            retry_count += 1
            if retry_count >= 3:
                retry_count = 0
                sys.exit(1)
            print(f"Retrying - retry_count: {retry_count}", file=sys.stderr)
            return retry(*args, **kwargs)

    return retry
