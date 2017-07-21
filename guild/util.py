def find_apply(funs, *args):
    for f in funs:
        result = f(*args)
        if result is not None:
            return result
    return None
