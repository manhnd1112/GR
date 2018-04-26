def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def is_num(data):
    try:
        int(data)
        return True
    except ValueError:
        return False