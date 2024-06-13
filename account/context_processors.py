
def user_status(request):
    return {
        'is_user_authenticated': request.user.is_authenticated,
        'current_user': request.user,
    }