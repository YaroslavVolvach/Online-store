from django.http import HttpResponse


def catalog_list (request):
    return HttpResponse('<h1>Hello world</h1>')
