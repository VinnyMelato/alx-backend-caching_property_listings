from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties  # From Task 2

@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    properties = get_all_properties()  # Uses low-level cache from Task 2
    data = [{'id': p.id, 'title': p.title, 'description': p.description, 
             'price': str(p.price), 'location': p.location, 'created_at': p.created_at} 
            for p in properties]
    return JsonResponse({'properties': data})