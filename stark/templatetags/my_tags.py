from django import template

register = template.Library()

@register.inclusion_tag('stark/list.html')
def show_list(*args,**kwargs):
    data_list = kwargs["data_list"]
    header_list = kwargs["header_list"]
    return {"data_list":data_list,"header_list":header_list}


from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.shortcuts import reverse
from stark.service.v1 import site

@register.inclusion_tag('stark/form.html')
def get_url(*args,**kwargs):
    form=kwargs["form"]
    config = kwargs["config"]
    new_form=[]
    for bfield in form:
        temp = {'is_popup': False, 'bfield': bfield}
        # field是ModelForm读取对应的models.类，然后根据每一个数据库字段，生成Form的字段
        from django.forms.models import ModelChoiceField
        if isinstance(bfield.field, ModelChoiceField):
            related_class_name = bfield.field.queryset.model
            if related_class_name in site._registry:
                app_model_name = related_class_name._meta.app_label, related_class_name._meta.model_name
                base_url = reverse("stark:%s_%s_add" % app_model_name)
                popurl = "%s?_popbackid=%s" % (base_url, bfield.auto_id)
                temp['is_popup'] = True
                temp['popup_url'] = popurl
        new_form.append(temp)
    return {"form":new_form}