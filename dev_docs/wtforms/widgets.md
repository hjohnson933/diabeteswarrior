# Widgets

Widgets are classes whose purpose are to render a field to its usable representation, usually XHTML. When a field is called, the default behaviour is to delegate the rendering to its widget. This abstraction is provided so that widgets can easily be created to customize the rendering of existing fields.

`Note All built-in widgets will return upon rendering a “HTML-safe” unicode string subclass that many templating frameworks (Jinja, Mako, Genshi) will recognize as not needing to be auto-escaped.`

## Built-in widgets

+ class wtforms.widgets.ColorInput(input_type=None) Renders an input with type “color”.

+ class wtforms.widgets.CheckboxInput(input_type=None) Render a checkbox.

    The checked HTML attribute is set if the field’s data is a non-false value.

+ class wtforms.widgets.DateTimeInput(input_type=None) Renders an input with type “datetime”.

+ class wtforms.widgets.DateTimeLocalInput(input_type=None) Renders an input with type “datetime-local”.

+ class wtforms.widgets.DateInput(input_type=None) Renders an input with type “date”.

+ class wtforms.widgets.EmailInput(input_type=None) Renders an input with type “email”.

+ class wtforms.widgets.FileInput(multiple=False) Render a file chooser input.
  + Parameters
    + multiple – allow choosing multiple files

+ class wtforms.widgets.HiddenInput(*args, **kwargs) Render a hidden input.

+ class wtforms.widgets.Input(input_type=None) Render a basic `<input>` field.

    This is used as the basis for most of the other input fields.

    By default, the _value() method will be called upon the associated field to provide the value= HTML attribute.

+ class wtforms.widgets.ListWidget(html_tag='ul', prefix_label=True) Renders a list of fields as a ul or ol list.

    This is used for fields which encapsulate many inner fields as subfields. The widget will try to iterate the field to get access to the subfields and call them to render them.

    If prefix_label is set, the subfield’s label is printed before the field, otherwise afterwards. The latter is useful for iterating radios or checkboxes.

+ class wtforms.widgets.MonthInput(input_type=None) Renders an input with type “month”.

+ class wtforms.widgets.NumberInput(step=None, min=None, max=None) Renders an input with type “number”.

+ class wtforms.widgets.PasswordInput(hide_value=True) Render a password input.

    For security purposes, this field will not reproduce the value on a form submit by default. To have the value filled in, set hide_value to False.

+ class wtforms.widgets.RangeInput(step=None) Renders an input with type “range”.

+ class wtforms.widgets.SubmitInput(input_type=None) Renders a submit button.

    The field’s label is used as the text of the submit button instead of the data on the field.

+ class wtforms.widgets.SearchInput(input_type=None) Renders an input with type “search”.

+ class wtforms.widgets.Select(multiple=False) Renders a select field.

    If multiple is True, then the size property should be specified on rendering to make the field useful.

    The field must provide an iter_choices() method which the widget will call on rendering; this method must yield tuples of (value, label, selected). It also must provide a has_groups() method which tells whether choices are divided into groups, and if they do, the field must have an iter_groups() method that yields tuples of (label, choices), where choices is a iterable of (value, label, selected) tuples.

+ class wtforms.widgets.TableWidget(with_table_tag=True) Renders a list of fields as a set of table rows with th/td pairs.

    If with_table_tag is True, then an enclosing `<table>` is placed around the rows.

    Hidden fields will not be displayed with a row, instead the field will be pushed into a subsequent table row to ensure XHTML validity. Hidden fields at the end of the field list will appear outside the table.

+ class wtforms.widgets.TelInput(input_type=None) Renders an input with type “tel”.

+ class wtforms.widgets.TextArea Renders a multi-line text area.

    rows and cols ought to be passed as keyword args when rendering.

+ class wtforms.widgets.TextInput(input_type=None) Render a single-line text input.

+ class wtforms.widgets.TimeInput(input_type=None) Renders an input with type “time”.

+ class wtforms.widgets.URLInput(input_type=None) Renders an input with type “url”.

+ class wtforms.widgets.WeekInput(input_type=None) Renders an input with type “week”.
