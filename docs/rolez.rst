==================
Using roles
==================

Writing a new role
==================

Just as writing new object-level permissions is really easy with django-rulez,
we wanted to provide a simple way to handle user roles.

Writing a role consists of doing the following::

  class GuestRole(object):
    def is_member(user, object):
        """Determine wether the passed user is a member of this group"""
        if user.is_anonymous:
            return True:
        else:
            return False

That's it! a role must simply be a class defining an "is_member" method that
accepts a user and an object instace, and the role must answer True or False,
depending on wether the passed user is a member of the group or not.

Using roles with models
========================

To make use of roles with your objects, you should use the ModelRoleMixin model
provided in rulez.rolez.models.
On top of extending the Mixin, your class should declare an array of roles
classes that are relevant to it in self.roles (or override the relevant_roles method)

This ensures that when a user's roles are not found in the cache, the program
doesn't spend time checking every possible role defined but limits itself to
those roles that are relevant to the model at hand.

Checking for roles in rules
============================

The most crucial part of roles is of course to be able to use them to limit
access to some resources.   
In order to do so, simply call the has_role() method on the model extending
ModelRoleMixin.

Accessing roles and permissions in templates
============================================

.. Warning::
   Do **NOT** use this for application logic. These template filters are made
   available purely for presentational reasons. The template is not the place
   to put application logic.

Access roles and permissions in templates::
    
    {% load rolez_tags %}
    {% if obj|has_role:'administrator' %}You are an admin!{% endif %}
    
    {{ user }} (you) has these roles for {{ obj }}:
    <ul>
    {% for role in obj|get_roles %}
        <li>{{ role.name }}</li>
    {% endif %}
    </ul>

    