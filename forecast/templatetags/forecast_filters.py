from django import template

register = template.Library()


@register.filter
def get_range(value):
    """
    Returns a range from 0 to the given value
    """
    return range(value)


@register.filter
def get_item(list_object, index):
    """
    Returns the item at the given index in the list
    """
    try:
        return list_object[index]

    except:

        return None
