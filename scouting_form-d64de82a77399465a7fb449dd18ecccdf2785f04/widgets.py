# Customized versions of WTForms fields
# Note that all of the Field classes defined in this file render labels as well,
# while default Field classes do not
import wtforms.widgets as widgets
from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.widgets import *

class CustomClassMixin(widgets.Input):
    custom_classes = []
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = ' '.join([c] + self.custom_classes)
        return super(CustomClassMixin, self).__call__(field, **kwargs)

class _BootstrapGridDefaults:
    # This class is just used to give default attributes to BootstrapGridFieldMixin objects
    col_xs = 12
    col_sm = 6
    col_md = 4
    col_lg = None
    label_col_xs = 4
    label_col_sm = 4
    label_col_md = 5
    label_col_lg = None

class IntegerInput(widgets.html5.NumberInput, CustomClassMixin):
    def __init__(self, *args, **kwargs):
        self.custom_classes = ['form-control']
        self.buttons = kwargs.pop('buttons', True)
        super(IntegerInput, self).__init__(*args, **kwargs)
        if not self.buttons:
            self.custom_classes.append('no-buttons')
    def __call__(self, field, **kwargs):
        html = super(IntegerInput, self).__call__(field, **kwargs)
        return HTMLString('<span class="input-group">') + html + HTMLString('</span>')

class BootstrapGridField(Field, _BootstrapGridDefaults):
    custom_classes = []
    label_classes = []
    field_classes = []
    def __init__(self, *args, **kwargs):
        # Copy col_* and label_col_* keyword arguments to the corresponding
        # attributes of this instance
        for k, v in list(kwargs.items()):
            if hasattr(_BootstrapGridDefaults, k):
                setattr(self, k, v)
                del kwargs[k]
            elif k in ('class', 'class_'):
                self.custom_classes.extend(k)
                del kwargs[k]
        super(BootstrapGridField, self).__init__(*args, **kwargs)
        self.custom_classes = self.custom_classes[:]
        self.label_classes = self.label_classes[:]
        self.field_classes = self.field_classes[:]

    def __call__(self, **kwargs):
        classes = self.custom_classes[:]
        label_classes = self.label_classes[:]
        # Extend and filter out blank classes
        field_classes = list(filter(bool, self.field_classes[:] +
            [kwargs.pop('class', '') or kwargs.pop('class_', '') or None]))
        for attr in dir(_BootstrapGridDefaults):
            name = attr.split('_')[-1]
            value = getattr(self, attr)
            if attr.startswith('col_') and value is not None:
                classes.append('col-%s-%i' % (name, value))
            if attr.startswith('label_col_') and value is not None:
                label_classes.append('col-%s-%i' % (name, value))

        kwargs['class'] = ' '.join(field_classes)
        html = super(BootstrapGridField, self).__call__(**kwargs)
        return HTMLString(self.generate_html(html, classes, label_classes))

    def generate_html(self, html, classes, label_classes):
        return (('<div class="%s">' % ' '.join(classes)) +
                '<div class="form-field">' +
                    self.label(class_ = ' '.join(label_classes)) +
                    html +
                '</div>' +
            '</div>')

class IntegerField(IntegerField, BootstrapGridField):
    def __init__(self, *args, **kwargs):
        buttons = kwargs.pop('buttons', True)
        super(IntegerField, self).__init__(*args, **kwargs)
        self.widget = IntegerInput(buttons=buttons)

class CheckboxButtonField(BooleanField, BootstrapGridField):
    def generate_html(self, html, classes, label_classes):
        classes.extend(['btn-group', 'checkbox-button-field'])
        return (('<div class="%s" data-toggle="buttons">' % ' '.join(classes)) +
                '<label class="btn btn-default">' +
                    html +
                    self.label.text +
                '</label>' +
            '</div>')

class TextAreaField(TextAreaField, BootstrapGridField):
    field_classes = ['form-control']
