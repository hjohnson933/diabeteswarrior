# Fields

The Field base [class](https://wtforms.readthedocs.io/en/3.0.x/fields/)

## class wtforms.fields.Field

### Construction

\_\_init\_\_(
    label=None,
    validators=None,
    filters=(),
    description='',
    id=None,
    default=None,
    widget=None,
    render_kw=None,
    name=None,
    \_form=None,
    \_prefix='',
    \_translations=None,
    \_meta=None
)

### Construct a new field

#### Parameters

+ label – The label of the field.

+ validators – A sequence of validators to call when validate is called.

+ filters – A sequence of filters which are run on input data by process.

+ description – A description for the field, typically used for help text.

+ id – An id to use for the field. A reasonable default is set by the form, and you shouldn’t need to set this manually.

+ default – The default value to assign to the field, if no form or object input is provided. May be a callable.

+ widget – If provided, overrides the widget used to render the field.

+ render_kw (dict) – If provided, a dictionary which provides default keywords that will be given to the widget at render time.

+ name – The HTML name of this field. The default value is the Python attribute name.

+ \_form – The form holding this field. It is passed by the form itself during construction. You should never pass this value yourself.

+ \_prefix – The prefix to prepend to the form name of this field, passed by the enclosing form during construction.

+ \_translations – A translations object providing message translations. Usually passed by the enclosing form during construction. See I18n docs for information on message translations.

+ \_meta – If provided, this is the ‘meta’ instance from the form. You usually don’t pass this yourself.

#### Properties

+ name
The HTML form name of this field. This is the name as defined in your Form prefixed with the prefix passed to the Form constructor.

+ short_name
The un-prefixed name of this field.

+ id
The HTML ID of this field. If unspecified, this is generated for you to be the same as the field name.

+ label
This is a Label instance which when evaluated as a string returns an HTML `<label for="id">` construct.

+ default
This is whatever you passed as the default to the field’s constructor, otherwise None.

+ description
A string containing the value of the description passed in the constructor to the field; this is not HTML escaped.

+ errors
A sequence containing the validation errors for this field.

+ process_errors
Errors obtained during input processing. These will be prepended to the list of errors at validation time.

+ widget
The widget used to render the field.

+ type
The type of this field, as a string. This can be used in your templates to do logic based on the type of field:

`{% for field in form %}
    <tr>
    {% if field.type == "BooleanField" %}
        <td></td>
        <td>{{ field }} {{ field.label }}</td>
    {% else %}
        <td>{{ field.label }}</td>
        <td>{{ field }}</td>
    {% endif %}
    </tr>
{% endfor %}`

+ flags
An object containing flags set either by the field itself, or by validators on the field. For example, the built-in InputRequired validator sets the required flag. An unset flag will result in None.

`{% for field in form %}
    <tr>
        <th>{{ field.label }} {% if field.flags.required %}*{% endif %}</th>
        <td>{{ field }}</td>
    </tr>
{% endfor %}`

+ meta
The same meta object instance as is available as Form.meta

+ filters
The same sequence of filters that was passed as the `filters=` to the field constructor. This is usually a sequence of callables.
