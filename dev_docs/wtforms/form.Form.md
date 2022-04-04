# Forms

The Form [class](https://wtforms.readthedocs.io/en/3.0.x/forms/)

## class wtforms.form.Form

### Construction

\_\_init\_\_(
    formdata=None,
    obj=None,
    prefix='',
    data=None,
    meta=None,
    **kwargs
)

#### Parameters

+ formdata – Input data coming from the client, usually request.form or equivalent. Should provide a “multi dict” interface to get a list of values for a given key, such as what Werkzeug, Django, and WebOb provide.

+ obj – Take existing data from attributes on this object matching form field attributes. Only used if formdata is not passed.

+ prefix – If provided, all fields will have their name prefixed with the value. This is for distinguishing multiple forms on a single page. This only affects the HTML name for matching input data, not the Python name for matching existing data.

+ data – Take existing data from keys in this dict matching form field attributes. obj takes precedence if it also has a matching attribute. Only used if formdata is not passed.

+ meta – A dict of attributes to override on this form’s meta instance.

+ extra_filters – A dict mapping field attribute names to lists of extra filter functions to run. Extra filters run after filters passed when creating the field. If the form has `filter_<fieldname>`, it is the last extra filter.

+ kwargs – Merged with data to allow passing existing data as parameters. Overwrites any duplicate keys in data. Only used if formdata is not passed.

##### Properties

+ data
A dict containing the data for each field.

    ___Note that this is generated each time you access the property, so care should be taken when using it, as it can potentially be very expensive if you repeatedly access it. Typically used if you need to iterate all data in the form. If you just need to access the data for known fields, you should use `form.<field>.data`, not this proxy property.___

+ errors
A dict containing a list of errors for each field. Empty if the form hasn’t been validated, or there were no errors.

    ___If present, the key None contains the content of form_errors.___

+ form_errors
A list of form-level errors. Those are errors that does not concern a particuliar field, but the whole form consistency. Those errors are often set when overriding validate().

+ meta
This is an object which contains various configuration options and also ability to customize the behavior of the form. See the class Meta doc for more information on what can be customized with the class Meta options.

#### Methods

+ validate(extra_validators=None)
Validate the form by calling validate on each field. Returns True if validation passes.

  ___If the form defines a `validate_<fieldname>` method, it is appended as an extra validator for the field’s validate.___

  Parameters

  + extra_validators – A dict mapping field names to lists of extra validator methods to run. Extra validators run after validators passed when creating the field. If the form has `validate_<fieldname>`, it is the last extra validator.

+ populate_obj(obj)
Populates the attributes of the passed obj with data from the form’s fields.

  ___This is a destructive operation; Any attribute with the same name as a field will be overridden. Use with caution.___

  One common usage of this is an edit profile view:

        def edit_profile(request):
            user = User.objects.get(pk=request.session['userid'])
            form = EditProfileForm(request.POST, obj=user)

            if request.POST and form.validate():
                form.populate_obj(user)
                user.save()
                return redirect('/home')
            return render_to_response('edit_profile.html', form=form)

  In the above example, because the form isn’t directly tied to the user object, you don’t have to worry about any dirty data getting onto there until you’re ready to move it over.

+ \_\_iter\_\_()
Iterate form fields in creation order.

        {% for field in form %}
            <tr>
                <th>{{ field.label }}</th>
                <td>{{ field }}</td>
            </tr>
        {% endfor %}

+ \_\_contains\_\_(name)
Returns True if the named field is a member of this form.

### Defining Forms

To define a form, one makes a subclass of Form and defines the fields declaratively as class attributes:

    class MyForm(Form):
        first_name = StringField('First Name', validators=[validators.input_required()])
        last_name  = StringField('Last Name', validators=[validators.optional()])

Field names can be any valid python identifier, with the following restrictions:

+ Field names are case-sensitive.

+ Field names may not begin with “_” (underscore)

+ Field names may not begin with “validate”

### Form Inheritance

Forms may subclass other forms as needed. The new form will contain all fields of the parent form, as well as any new fields defined on the subclass. A field name re-used on a subclass causes the new definition to obscure the original.

    class PastebinEdit(Form):
        language = SelectField('Programming Language', choices=PASTEBIN_LANGUAGES)
        code     = TextAreaField()

    class PastebinEntry(PastebinEdit):
        name = StringField('User Name')

### In-line Validators and Filters

In order to provide custom validation for a single field without needing to write a one-time-use validator, validation can be defined inline by defining a method with the convention `validate_fieldname:`

    class SignupForm(Form):
        age = IntegerField('Age')

        def validate_age(form, field):
            if field.data < 13:
                raise ValidationError("We're sorry, you must be 13 or older to register")

The same principle applies for filters with the convention `filter_fieldname:`

    class SignupForm(Form):
        name = StringField('name')

        def filter_name(form, field):
            return field.strip()

___Note that filters are applied after processing the default and incoming data, but before validation.___

### Using Forms

A form is most often constructed in the controller code for handling an action, with the form data wrapper from the framework passed to its constructor, and optionally an ORM object. A typical view begins something like:

    def edit_article(request):
        article = Article.get(...)
        form = MyForm(request.POST, article)

The constructed form can then validate any input data and generate errors if invalid. Typically, the validation pattern in the view looks like:

    if request.POST and form.validate():
        form.populate_obj(article)
        article.save()
        return redirect('/articles')
