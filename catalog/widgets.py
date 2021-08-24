from django.forms.widgets import ClearableFileInput


class ImageWidget(ClearableFileInput):
    clear_checkbox_label = "Don't change photo"
    template_name = 'custom_widgets/ImageWidget.html'
