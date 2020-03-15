from django.forms.widgets import Input


class SliderWidget(Input):

    input_type = "range"
    class_type = "slider"
    units = "%"
    step = 1
    template_name = "meta_subject/widgets/slider.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if attrs.get("step"):
            context["widget"]["step"] = str(attrs.get("step"))
        else:
            context["widget"]["step"] = str(self.step)
        context["widget"]["type"] = self.input_type
        context["widget"]["class"] = self.class_type
        context["widget"]["units"] = self.units
        context["widget"]["min"] = attrs.get("min")
        context["widget"]["max"] = attrs.get("max")
        return context

    class Media:
        css = {"all": ("meta_subject/slider.css",)}
