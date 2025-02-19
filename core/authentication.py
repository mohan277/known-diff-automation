from account.models import Users


def authenticate(email_id, password):
    try:
        return Users.objects.get(email_id=email_id, password=password)
    except:
        return None
