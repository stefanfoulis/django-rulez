#-*- coding: utf-8 -*-

from django import template

register = template.Library()

# PermWrapper and PermLookupDict proxy the permissions system into objects that
# the template system can understand.
# they are very much inspired by django.contrib.auth.context_processors.auth


class RoleWrapper(object):
    def __init__(self, user, obj):
        self.user = user
        self.obj = obj
        self.roles = {}
        for role in obj.relevant_roles():
            if hasattr(role, 'short_name'):
                key = role.short_name
            else:
                key = role.__class__.__name__.lower()
            key = "is_%s" % key
            self.roles[key]=obj.has_role(self.user, role)

    def __getitem__(self, role_name):
        return self.roles[role_name]

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("RoleWrapper is not iterable.")


def get_roles(obj, user):
    return obj.get_roles(user)
register.filter('get_roles', get_roles)

def roles(obj, user):
    return RoleWrapper(user, obj)
