import json

from django.shortcuts import render
from .api_parser import ApiParser
from django.conf import settings


def walk_endpoints(tree, endpoints=None):
    if endpoints is None:
        endpoints = []

    for k, v in tree.items():
        if type(v) == dict:
            walk_endpoints(v, endpoints)
        else:
            endpoints.append({
                'path': v.complete_path,
                'auth': v.authentication_classes,
                'methods': v.methods,
                'input': v.input_fields if hasattr(v, 'input_fields') else None,
                'doc': v.docstring,
            })

    return endpoints


def get_endpoints(request):
    api_parser = ApiParser()
    api_parser.parse()
    endpoints = walk_endpoints(api_parser.endpoints)

    force_script_name = getattr(settings, 'FORCE_SCRIPT_NAME', '')
    if force_script_name.endswith('/'):
        force_script_name = force_script_name[:-1]
    return render(request, 'redocs/index.html', {
        'force_script_name': force_script_name,
        'endpoints': json.dumps(endpoints),
    })
