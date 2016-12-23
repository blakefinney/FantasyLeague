""" Some Helper Functions for the Wesbite"""


def is_logged_in(request):
    return request.user.is_active
