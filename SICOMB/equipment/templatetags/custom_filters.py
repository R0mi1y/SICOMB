from django import template

register = template.Library()

@register.filter
def model_class(model):
    model_name = {
        'Model_armament': 'Armamento',
        'Model_accessory': 'Acessório',
        'Model_wearable': 'Vestimentos',
        'Model_grenada': 'Granadas',
        'Bullet': 'Munição',
    }
    
    return model_name[model.__class__.__name__]
