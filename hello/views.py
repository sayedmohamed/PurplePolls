from django.http import HttpResponse


def say_hello(request):
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
    else:
        name = 'world'

    return HttpResponse('Hello %s' % name)