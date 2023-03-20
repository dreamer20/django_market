def get_filter_choices(Model, field_name):
    return lambda: Model.objects.values_list(field_name, field_name).distinct()
