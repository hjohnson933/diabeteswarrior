# Validators

A [validator](https://wtforms.readthedocs.io/en/3.0.x/validators/) simply takes an input, verifies it fulfills some criterion, such as a maximum length for a string and returns. Or, if the validation fails, raises a ValidationError. This system is very simple and flexible, and allows you to chain any number of validators on fields.

___If StopValidation is raised, no more validators in the validation chain are called. If raised with a message, the message will be added to the errors list.___

## Built-in validators

+ class wtforms.validators.DataRequired(message=None)
Checks the field’s data is ‘truthy’ otherwise stops the validation chain.
  + Parameters
    + message – Error message to raise in case of a validation error.

    This validator checks that the data attribute on the field is a ‘true’ value (effectively, it does `if field.data`.) Furthermore, if the data is a string type, a string containing only whitespace characters is considered false.

    If the data is empty, also removes prior errors (such as processing errors) from the field.

    ___NOTE this validator used to be called Required but the way it behaved (requiring coerced data, not input data) meant it functioned in a way which was not symmetric to the Optional validator and furthermore caused confusion with certain fields which coerced data to ‘falsey’ values like 0, Decimal(0), time(0) etc. Unless a very specific reason exists, we recommend using the InputRequired instead.___

+ class wtforms.validators.Email(message=None, granular_message=False, check_deliverability=False, allow_smtputf8=True, allow_empty_local=False)
  + Parameters
    + message – Error message to raise in case of a validation error.
    + granular_message – Use validation failed message from email_validator library (Default False).
    + check_deliverability – Perform domain name resolution check (Default False).
    + allow_smtputf8 – Fail validation for addresses that would require SMTPUTF8 (Default True).
    + allow_empty_local – Allow an empty local part (i.e. @example.com), e.g. for validating Postfix aliases (Default False).

      Validates an email address. Requires email_validator package to be installed. For ex: pip install wtforms.

+ class wtforms.validators.EqualTo(fieldname, message=None)
Compares the values of two fields.
  + Parameters
    + fieldname – The name of the other field to compare to.
    + message – Error message to raise in case of a validation error. Can be interpolated with %(other_label)s and %(other_name)s to provide a more helpful error.

+ class wtforms.validators.InputRequired(message=None) Validates that input was provided for this field.

    `Note there is a distinction between this and DataRequired in that InputRequired looks that form-input data was provided, and DataRequired looks at the post-coercion data.`

+ class wtforms.validators.IPAddress(ipv4=True, ipv6=False, message=None) Validates an IP address.
  + Parameters
    + ipv4 – If True, accept IPv4 addresses as valid (default True)
    + ipv6 – If True, accept IPv6 addresses as valid (default False)
    + message – Error message to raise in case of a validation error.

+ class wtforms.validators.Length(min=- 1, max=- 1, message=None) Validates the length of a string.
  + Parameters
    + min – The minimum required length of the string. If not provided, minimum length will not be checked.
    + max – The maximum length of the string. If not provided, maximum length will not be checked.
    + message – Error message to raise in case of a validation error. Can be interpolated using %(min)d and %(max)d if desired. Useful defaults are provided depending on the existence of min and max.

  When supported, sets the minlength and maxlength attributes on widgets.

+ class wtforms.validators.MacAddress(message=None)
Validates a MAC address.
  + Parameters
    + message – Error message to raise in case of a validation error.

+ class wtforms.validators.NumberRange(min=None, max=None, message=None) Validates that a number is of a minimum and/or maximum value, inclusive. This will work with any comparable number type, such as floats and decimals, not just integers.
  + Parameters
    + min – The minimum required value of the number. If not provided, minimum value will not be checked.
    + max – The maximum value of the number. If not provided, maximum value will not be checked.
    + message – Error message to raise in case of a validation error. Can be interpolated using %(min)s and %(max)s if desired. Useful defaults are provided depending on the existence of min and max.

    When supported, sets the min and max attributes on widgets.

+ class wtforms.validators.Optional(strip_whitespace=True) Allows empty input and stops the validation chain from continuing.
  + Parameters
    + strip_whitespace – If True (the default) also stop the validation chain on input which consists of only whitespace.

    If input is empty, also removes prior errors (such as processing errors) from the field.

    Sets the optional attribute on widgets.

    This also sets the optional flag on fields it is used on.

+ class wtforms.validators.Regexp(regex, flags=0, message=None) Validates the field against a user provided regexp.
  + Parameters
    + regex – The regular expression string to use. Can also be a compiled regular expression pattern.
    + flags – The regexp flags to use, for example re.IGNORECASE. Ignored if regex is not a string.
    + message – Error message to raise in case of a validation error.

+ class wtforms.validators.URL(require_tld=True, message=None) Simple regexp based url validation. Much like the email validator, you probably want to validate the url later by other means if the url must resolve.
  + Parameters
    + require_tld – If true, then the domain-name portion of the URL must contain a .tld suffix. Set this to false if you want to allow domains like localhost.
    + message – Error message to raise in case of a validation error.

+ class wtforms.validators.UUID(message=None) Validates a UUID.
  + Parameters
    + message – Error message to raise in case of a validation error.

+ class wtforms.validators.AnyOf(values, message=None, values_formatter=None) Compares the incoming data to a sequence of valid inputs.
  + Parameters
    + values – A sequence of valid inputs.
    + message – Error message to raise in case of a validation error. %(values)s contains the list of values.
    + values_formatter – Function used to format the list of values in the error message.

+ class wtforms.validators.NoneOf(values, message=None, values_formatter=None) Compares the incoming data to a sequence of invalid inputs.
  + Parameters
    + values – A sequence of invalid inputs.
    + message – Error message to raise in case of a validation error. %(values)s contains the list of values.
    + values_formatter – Function used to format the list of values in the error message.
