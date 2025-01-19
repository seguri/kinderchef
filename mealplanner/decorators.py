def short_description(description):
    def decorator(func):
        func.short_description = description
        return func

    return decorator
