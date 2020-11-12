from django.shortcuts import render


def catalog_list (request):
    s = 'catalog_list'
    return render(request, 'catalog/catalog_list.html', context={'s': s})
