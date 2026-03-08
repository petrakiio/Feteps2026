from model.user import User

def get_user(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None