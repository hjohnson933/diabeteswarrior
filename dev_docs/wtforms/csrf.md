# CSRF Protection

The CSRF package includes tools that help you implement checking against cross-site request forgery (“csrf”). Due to the large number of variations on approaches people take to CSRF (and the fact that many make compromises) the base implementation allows you to plug in a number of CSRF validation approaches.

CSRF implementations are made by subclassing CSRF. For utility, we have provided one possible CSRF implementation in the package that can be used with many frameworks for session-based hash secure keying, SessionCSRF.

## Using CSRF

CSRF in WTForms 2.0 is now driven through a number of variables on class Meta. After choosing a CSRF implementation, import it and configure it on the class Meta of a subclass of Form like such:

`from somemodule import SomeCSRF`

    class MyBaseForm(Form):
        class Meta:
            csrf = True  # Enable CSRF
            csrf_class = SomeCSRF  # Set the CSRF implementation
            csrf_secret = b'foobar'  # Some implementations need a secret key.
            # Any other CSRF settings here.

And once you’ve got this set up, you can define your forms as a subclass of MyBaseForm:

    class UserForm(MyBaseForm):
        name = StringField()
        age = IntegerField()

    def view():
        form = UserForm(request.POST)
        if request.POST and form.validate():
            pass # Form is valid and CSRF succeeded

        return render('user.html', form=form)

There is a special field inside the CSRF form (called csrf_token by default) which you need to make sure you render in your template:

    <form action="/user" method="POST">
    {{ form.csrf_token }}
    {% if form.csrf_token.errors %}
        <div class="warning">You have submitted an invalid CSRF token</div>
    {% endif %}
    <div>{{ form.name }} {{ form.name.label }}</div>
    <div>{{ form.age }}{{ form.age.label }}</div>

Remember, with the class Meta you can always override variables in a sub-class or at the constructor for special-cases:

    class SearchForm(MyBaseForm):
        """
        We expect search queries to come externally, thus we don't want CSRF
        even though it's set up on the base form.
        """
        class Meta:
            # This overrides the value from the base form.
            csrf = False

## How WTForms CSRF works

Most CSRF implementations hinge around creating a special token, which is put in a hidden field on the form named csrf_token, which must be rendered in your template to be passed from the browser back to your view. There are many different methods of generating this token, but they are usually the result of a cryptographic hash function against some data which would be hard to forge.

+ class wtforms.csrf.core.CSRFTokenField(*args, **kwargs) A subclass of HiddenField designed for sending the CSRF token that is used for most CSRF protection schemes.

    Notably different from a normal field, this field always renders the current token regardless of the submitted value, and also will not be populated over to object data via populate_obj

    \_\_init\_\_(*args, **kw) Construct a new field.

  + Parameters
    + label – The label of the field.
    + validators – A sequence of validators to call when validate is called.
    + filters – A sequence of filters which are run on input data by process.
    + description – A description for the field, typically used for help text.
    + id – An id to use for the field. A reasonable default is set by the form, and you shouldn’t need to set this manually.
    + default – The default value to assign to the field, if no form or object input is provided. May be a callable.
    + widget – If provided, overrides the widget used to render the field.
    + render_kw (dict) – If provided, a dictionary which provides default keywords that will be given to the widget at render time.
    + name – The HTML name of this field. The default value is the Python attribute name.
    + _form – The form holding this field. It is passed by the form itself during construction. You should never pass this value yourself.
    + _prefix – The prefix to prepend to the form name of this field, passed by the enclosing form during construction.
    + _translations – A translations object providing message translations. Usually passed by the enclosing form during construction. See I18n docs for information on message translations.
    + _meta – If provided, this is the ‘meta’ instance from the form. You usually don’t pass this yourself.

  If _form isn’t provided, an UnboundField will be returned instead. Call its bind() method with a form instance and a name to construct the field.

  current_token = None

  _value() We want to always return the current token on render, regardless of whether a good or bad token was passed.

  populate_obj(*args) Don’t populate objects with the CSRF token

  pre_validate(form) Handle validation of this token field.

  process(*args, **kwargs) Process incoming data, calling process_data, process_formdata as needed, and run filters.

  If data is not provided, process_data will be called on the field’s default.

  Field subclasses usually won’t override this, instead overriding the process_formdata and process_data methods. Only override this for special advanced processing, such as when a field encapsulates many inputs.

  + Parameters
    + extra_filters – A sequence of extra filters to run.

+ class wtforms.csrf.core.CSRF setup_form(form) Receive the form we’re attached to and set up fields.

  The default implementation creates a single field of type field_class with name taken from the csrf_field_name of the class meta.

  + Parameters
    + form – The form instance we’re attaching to.

  + Returns
    A sequence of (field_name, unbound_field) 2-tuples which are unbound fields to be added to the form.

+ generate_csrf_token(csrf_token_field) Implementations must override this to provide a method with which one can get a CSRF token for this form.

    A CSRF token is usually a string that is generated deterministically based on some sort of user data, though it can be anything which you can validate on a subsequent request.

  + Parameters
    + csrf_token_field – The field which is being used for CSRF.
  + Returns
    A generated CSRF string.

+ validate_csrf_token(form, field) Override this method to provide custom CSRF validation logic.

    The default CSRF validation logic simply checks if the recently generated token equals the one we received as formdata.

  + Parameters
    + form – The form which has this CSRF token.
    + field – The CSRF token field.
    + field_class = `<class 'wtforms.csrf.core.CSRFTokenField'>` The class of the token field we’re going to construct. Can be overridden in subclasses if need be.

## Creating your own CSRF implementation

Here we will sketch out a simple theoretical CSRF implementation which generates a hash token based on the user’s IP.

___Note This is a simplistic example meant to illustrate creating a CSRF implementation. This isn’t recommended to be used in production because the token is deterministic and non-changing per-IP, which means this isn’t the most secure implementation of CSRF.___

First, let’s create our CSRF class:

    from wtforms.csrf.core import CSRF
    from hashlib import md5

SECRET_KEY = '1234567890'

    class IPAddressCSRF(CSRF):
        """
        Generate a CSRF token based on the user's IP. I am probably not very
        secure, so don't use me.
        """
        def setup_form(self, form):
            self.csrf_context = form.meta.csrf_context
            return super(IPAddressCSRF, self).setup_form(form)

        def generate_csrf_token(self, csrf_token):
            token = md5(SECRET_KEY + self.csrf_context).hexdigest()
            return token

        def validate_csrf_token(self, form, field):
            if field.data != field.current_token:
                raise ValueError('Invalid CSRF')

Now that we have this taken care of, let’s write a simple form and view which would implement this:

    class RegistrationForm(Form):
        class Meta:
            csrf = True
            csrf_class = IPAddressCSRF

        name = StringField('Your Name')
        email = StringField('Email', [validators.email()])

    def register(request):
        form = RegistrationForm(
            request.POST,
            meta={'csrf_context': request.ip}
        )

        if request.method == 'POST' and form.validate():
            pass # We're all good, create a user or whatever it is you do
        elif form.csrf_token.errors:
            pass # If we're here we suspect the user of cross-site request forgery
        else:
            pass # Any other errors

        return render('register.html', form=form)

And finally, a simple template:

    <form action="register" method="POST">
        {{ form.csrf_token }}
        <p>{{ form.name.label }}: {{ form.name }}</p>
        <p>{{ form.email.label }}: {{ form.email }}</p>
        <input type="submit" value="Register">
    </form>

Please note that implementing CSRF detection is not fool-proof, and even with the best CSRF protection implementation, it’s possible for requests to be forged by expert attackers. However, a good CSRF protection would make it infeasible for someone from an external site to hijack a form submission from another user and perform actions as them without additional a priori knowledge.

In addition, it’s important to understand that very often, the more strict the CSRF protection, the higher the chance of false positives occurring (ie, legitimate users getting blocked by your CSRF protection) and choosing a CSRF implementation is actually a matter of compromise. We will attempt to provide a handful of usable reference algorithms built in to this library in the future, to allow that choice to be easy.

Some tips on criteria people often examine when evaluating CSRF implementations:

Reproducability If a token is based on attributes about the user, it gains the advantage that one does not need secondary storage in which to store the value between requests. However, if the same attributes can be reproduced by an attacker, then the attacker can potentially forge this information.

Reusability. It might be desired to make a completely different token every use, and disallow users from re-using past tokens. This is an extremely powerful protection, but can have consequences on if the user uses the back button (or in some cases runs forms simultaneously in multiple browser tabs) and submits an old token, or otherwise. A possible compromise is to allow reusability in a time window (more on that later).

Time Ranges Many CSRF approaches use time-based expiry to make sure that a token cannot be (re)used beyond a certain point. Care must be taken in choosing the time criteria for this to not lock out legitimate users. For example, if a user might walk away while filling out a long-ish form, or to go look for their credit card, the time for expiry should take that into consideration to provide a balance between security and limiting user inconvenience.

Requirements Some CSRF-prevention methods require the use of browser cookies, and some even require client-side scripting support. The webmaster implementing the CSRF needs to consider that such requirements (though effective) may lock certain legitimate users out, and make this determination whether it is a good idea to use. For example, for a site already using cookies for login, adding another for CSRF isn’t as big of a deal, but for other sites it may not be feasible.

Session-based CSRF implementation
A provided CSRF implementation which puts CSRF data in a session.

This can be used fairly comfortably with many request.session type objects, including the Werkzeug/Flask session store, Django sessions, and potentially other similar objects which use a dict-like API for storing session keys.

The basic concept is a randomly generated value is stored in the user’s session, and an hmac-sha1 of it (along with an optional expiration time, for extra security) is used as the value of the csrf_token. If this token validates with the hmac of the random value + expiration time, and the expiration time is not passed, the CSRF validation will pass.

class wtforms.csrf.session.SessionCSRF Meta Values

csrf_secret A byte string which is the master key by which we encode all values. Set to a sufficiently long string of characters that is difficult to guess or bruteforce (recommended at least 16 characters) for example the output of os.urandom(16).

csrf_time_limit if None, tokens last forever (not recommended.) Otherwise, set to a datetime.timedelta that will define how long CSRF tokens are valid for. Defaults to 30 minutes.

csrf_context This should be a request.session-style object. Usually given in the Form constructor.

### Example

from wtforms.csrf.session import SessionCSRF
from datetime import timedelta

    class MyBaseForm(Form):
        class Meta:
            csrf = True
            csrf_class = SessionCSRF
            csrf_secret = b'EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym'
            csrf_time_limit = timedelta(minutes=20)

    class Registration(MyBaseForm):
        name = StringField()

    def view(request):
        form = Registration(request.POST, meta={'csrf_context': request.session})
        # rest of view here

___Note that request.session is passed as the csrf_context override to the meta info, this is so that the CSRF token can be stored in your session for comparison on a later request.___

### Example Integration

WTForms primitives are designed to work with a large variety of frameworks, and as such sometimes things seem like they are more work to use, but with some smart integration, you can actually clean up your code substantially.

For example, if you were going to integrate with Flask, and wanted to use the SessionCSRF implementation, here’s one way to get the CSRF context to be available without passing it all the time:

    from flask import session
    from wtforms.csrf.session import SessionCSRF

    class MyBaseForm(Form):
        class Meta:
            csrf = True
            csrf_class = SessionCSRF
            csrf_secret = app.config['CSRF_SECRET_KEY']

            @property
            def csrf_context(self):
                return session

Now with any subclasses of MyBaseForm, you don’t need to pass in the csrf context, and on top of that, we grab the secret key out of your normal app configuration.
