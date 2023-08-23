from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    print("Testando se o usuário {} faz parte do grupo de {}.".format(user.username, group_name))
    try:
        group = Group.objects.get(name=group_name)
        for i in user.groups.all():
            print(i)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
