

def account(request):

    return {'user': request.session['is_authenticated']}