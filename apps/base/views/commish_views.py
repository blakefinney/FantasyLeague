from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test(lambda u: u.is_superuser)
def commish_home(request):
    """ Story View """
    template_context = {}

    return render(request, 'base/commish_home.html', context=template_context)
