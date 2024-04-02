from django import template


register = template.Library()


@register.filter(name="iattr")
def iattr(value, arg):
    """Removes all values of arg from the given string"""
    return getattr(value, arg)


@register.filter(name="mfield")
def mfield(value):
    """Removes all values of arg from the given string"""
    return value.replace("_", " ").title()


@register.filter(name="gmeta")
def gmeta(value):
    """Removes all values of arg from the given string"""
    return value._meta


@register.filter(name="gmetav")
def gmetav(value, arg, default=None):
    """Removes all values of arg from the given string"""
    return getattr(value._meta, arg) if hasattr(value._meta, arg) else default


@register.filter(name="adbkpath")
def adbkpath(value):
    """Gets address book path"""
    return f"app/address-book/{value}.html"
