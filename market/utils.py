def getFieldValueList(Model, name):
    return [(item[name], item[name]) for item in Model.objects.values(name).distinct()]
