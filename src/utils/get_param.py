from fastapi import Request


def get_params(request: Request) -> dict:
    params = {}
    for key, value in request.query_params.items():
        new_key = key[:-len(']')].split('[')
        if len(new_key) == 2:
            params.setdefault(new_key[0], {}).update({new_key[1]: value})
            continue
        params[key] = value
    return params

