# Template Designer

Below is a minimal [template](https://jinja.palletsprojects.com/en/3.0.x/templates/) that illustrates a few basics using the default Jinja configuration. We will cover the details later in this document:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>My Webpage</title>
    </head>
    <body>
        <ul id="navigation">
        {% for item in navigation %}
            <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
        {% endfor %}
        </ul>

        <h1>My Webpage</h1>
        {{ a_variable }}

        {# a comment #}
    </body>
    </html>

+ {% ... %} for Statements
+ {{ ... }} for Expressions to print to the template output
+ {# ... #} for Comments not included in the template output

## Variables

Template variables are defined by the context dictionary passed to the template.

You can use a dot (.) to access attributes of a variable in addition to the standard Python __getitem__ “subscript” syntax ([]).

The following lines do the same thing:

    {{ foo.bar }}
    {{ foo['bar'] }}

It’s important to know that the outer double-curly braces are not part of the variable, but the print statement. If you access variables inside tags don’t put the braces around them.

If a variable or attribute does not exist, you will get back an undefined value. What you can do with that kind of value depends on the application configuration: the default behavior is to evaluate to an empty string if printed or iterated over, and to fail for every other operation.

### Implementation

For the sake of convenience, foo.bar in Jinja does the following things on the Python layer:

check for an attribute called bar on foo (getattr(foo, 'bar'))

if there is not, check for an item 'bar' in foo (foo.\_\_getitem\_\_('bar'))

if there is not, return an undefined object.

foo['bar'] works mostly the same with a small difference in sequence:

check for an item 'bar' in foo. (foo.\_\_getitem\_\_('bar'))

if there is not, check for an attribute called bar on foo. (getattr(foo, 'bar'))

if there is not, return an undefined object.

This is important if an object has an item and attribute with the same name. Additionally, the attr() filter only looks up attributes.

## Filters

Variables can be modified by filters. Filters are separated from the variable by a pipe symbol (|) and may have optional arguments in parentheses. Multiple filters can be chained. The output of one filter is applied to the next.

For example, `{{ name|striptags|title }}` will remove all HTML Tags from variable name and title-case the output (title(striptags(name))).

Filters that accept arguments have parentheses around the arguments, just like a function call. For example: `{{ listx|join(', ') }}` will join a list with commas `(str.join(', ', listx))`.

The [List of Builtin Filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

+ abs()
+ float()
+ lower()
+ round()
+ tojson()
+ attr()
+ forceescape()
+ map()
+ safe()
+ trim()
+ batch()
+ format()
+ max()
+ select()
+ truncate()
+ capitalize()
+ groupby()
+ min()
+ selectattr()
+ unique()
+ center()
+ indent()
+ pprint()
+ slice()
+ upper()
+ default()
+ int()
+ random()
+ sort()
+ urlencode()
+ dictsort()
+ join()
+ reject()
+ string()
+ urlize()
+ escape()
+ last()
+ rejectattr()
+ striptags()
+ wordcount()
+ filesizeformat()
+ length()
+ replace()
+ sum()
+ wordwrap()
+ first()
+ list()
+ reverse()
+ title()
+ xmlattr()

Filter sections allow you to apply regular Jinja filters on a block of template data. Just wrap the code in the special filter section:

    {% filter upper %}
        This text becomes uppercase
    {% endfilter %}

## Tests

Beside filters, there are also so-called “tests” available. Tests can be used to test a variable against a common expression. To test a variable or expression, you add is plus the name of the test after the variable. For example, to find out if a variable is defined, you can do name is defined, which will then return true or false depending on whether name is defined in the current template context.

Tests can accept arguments, too. If the test only takes one argument, you can leave out the parentheses. For example, the following two expressions do the same thing:

{% if loop.index is divisibleby 3 %}
{% if loop.index is divisibleby(3) %}
The [List of Builtin Tests](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-tests) below.

+ boolean()
+ even()
+ in()
+ mapping()
+ sequence()
+ callable()
+ false()
+ integer()
+ ne()
+ string()
+ defined()
+ filter()
+ iterable()
+ none()
+ test()
+ divisibleby()
+ float()
+ le()
+ number()
+ true()
+ eq()
+ ge()
+ lower()
+ odd()
+ undefined()
+ escaped()
+ gt()
+ lt()
+ sameas()
+ upper()

## List of Control Structures

A control structure refers to all those things that control the flow of a program - conditionals (i.e. if/elif/else), for-loops, as well as things like macros and blocks. With the default syntax, control structures appear inside {% ... %} blocks.

### For

Loop over each item in a sequence. For example, to display a list of users provided in a variable called users:

+ loop.index
    The current iteration of the loop. (1 indexed)
+ loop.index0
  The current iteration of the loop. (0 indexed)
+ loop.revindex
    The number of iterations from the end of the loop (1 indexed)
+ loop.revindex0
    The number of iterations from the end of the loop (0 indexed)
+ loop.first
    True if first iteration.
+ loop.last
    True if last iteration.
+ loop.length
    The number of items in the sequence.
+ loop.cycle
    A helper function to cycle between a list of sequences. See the explanation below.
+ loop.depth
    Indicates how deep in a recursive loop the rendering currently is. Starts at level 1
+ loop.depth0
    Indicates how deep in a recursive loop the rendering currently is. Starts at level 0
+ loop.previtem
    The item from the previous iteration of the loop. Undefined during the first iteration.
+ loop.nextitem
    The item from the following iteration of the loop. Undefined during the last iteration.
+ loop.changed(*val)
    True if previously called with a different value (or not called at all).

### If

The if statement in Jinja is comparable with the Python if statement. In the simplest form, you can use it to test if a variable is defined, not empty and not false:

    {% if users %}
    <ul>
    {% for user in users %}
        <li>{{ user.username|e }}</li>
    {% endfor %}
    </ul>
    {% endif %}

For multiple branches, elif and else can be used like in Python. You can use more complex Expressions there, too:

    {% if kenny.sick %}
        Kenny is sick.
    {% elif kenny.dead %}
        You killed Kenny!  You bastard!!!
    {% else %}
        Kenny looks okay --- so far
    {% endif %}

If can also be used as an [inline expression](https://jinja.palletsprojects.com/en/3.0.x/templates/#if-expression) and for [loop filtering](https://jinja.palletsprojects.com/en/3.0.x/templates/#loop-filtering).

### Macros

Macros are comparable with functions in regular programming languages. They are useful to put often used idioms into reusable functions to not repeat yourself (“DRY”).

Here’s a small example of a macro that renders a form element:

    {% macro input(name, value='', type='text', size=20) -%}
        <input type="{{ type }}" name="{{ name }}" value="{{
            value|e }}" size="{{ size }}">
    {%- endmacro %}

The macro can then be called like a function in the namespace:

    <p>{{ input('username') }}</p>
    <p>{{ input('password', type='password') }}</p>

If the macro was defined in a different template, you have to import it first.

Inside macros, you have access to three special variables:

+ varargs
    If more positional arguments are passed to the macro than accepted by the macro, they end up in the special varargs variable as a list of values.
+ kwargs
    Like varargs but for keyword arguments. All unconsumed keyword arguments are stored in this special variable.
+ caller
    If the macro was called from a call tag, the caller is stored in this variable as a callable macro.

Macros also expose some of their internal details. The following attributes are available on a macro object:

+ name
    The name of the macro. {{ input.name }} will print input.
+ arguments
    A tuple of the names of arguments the macro accepts.
+ catch_kwargs
    This is true if the macro accepts extra keyword arguments (i.e.: accesses the special kwargs variable).
+ catch_varargs
    This is true if the macro accepts extra positional arguments (i.e.: accesses the special varargs variable).
+ caller
    This is true if the macro accesses the special caller variable and may be called from a call tag.

If a macro name starts with an underscore, it’s not exported and can’t be imported.

### Assignments

Inside code blocks, you can also assign values to variables. Assignments at top level (outside of blocks, macros or loops) are exported from the template like top level macros and can be imported by other templates.

Assignments use the set tag and can have multiple targets:

    {% set navigation = [('index.html', 'Index'), ('about.html', 'About')] %}
    {% set key, value = call_something() %}

### Scoping Behavior

Please keep in mind that it is not possible to set variables inside a block and have them show up outside of it. This also applies to loops. The only exception to that rule are if statements which do not introduce a scope. As a result the following template is not going to do what you might expect:

    {% set iterated = false %}
    {% for item in seq %}
        {{ item }}
        {% set iterated = true %}
    {% endfor %}
    {% if not iterated %} did not iterate {% endif %}

It is not possible with Jinja syntax to do this. Instead use alternative constructs like the loop else block or the special loop variable:

    {% for item in seq %}
        {{ item }}
    {% else %}
        did not iterate
    {% endfor %}

As of version 2.10 more complex use cases can be handled using namespace objects which allow propagating of changes across scopes:

    {% set ns = namespace(found=false) %}
    {% for item in items %}
        {% if item.check_something() %}
            {% set ns.found = true %}
        {% endif %}
        * {{ item.title }}
    {% endfor %}

Found item having something: {{ ns.found }}
Note that the obj.attr notation in the set tag is only allowed for namespace objects; attempting to assign an attribute on any other object will raise an exception.

## Block Assignments

Starting with Jinja 2.8, it’s possible to also use block assignments to capture the contents of a block into a variable name. This can be useful in some situations as an alternative for macros. In that case, instead of using an equals sign and a value, you just write the variable name and then everything until {% endset %} is captured.

Example:

    {% set navigation %}
        <li><a href="/">Index</a>
        <li><a href="/downloads">Downloads</a>
    {% endset %}

The navigation variable then contains the navigation HTML source.

Starting with Jinja 2.10, the block assignment supports filters.

Example:

    {% set reply | wordwrap %}
        You wrote:
        {{ message }}
    {% endset %}

### Extends

The extends tag can be used to extend one template from another. You can have multiple extends tags in a file, but only one of them may be executed at a time.

See the section about [Template Inheritance](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance) above.

### Blocks

Blocks are used for inheritance and act as both placeholders and replacements at the same time. They are documented in detail in the [Template Inheritance](Blocks
Blocks are used for inheritance and act as both placeholders and replacements at the same time. They are documented in detail in the Template Inheritance section.) section.

### Include

The include tag is useful to include a template and return the rendered contents of that file into the current namespace:

    {% include 'header.html' %}
        Body
    {% include 'footer.html' %}

Included templates have access to the variables of the active context by default. For more details about context behavior of imports and includes, see Import Context Behavior.

From Jinja 2.2 onwards, you can mark an include with ignore missing; in which case Jinja will ignore the statement if the template to be included does not exist. When combined with with or without context, it must be placed before the context visibility statement. Here are some valid examples:

    {% include "sidebar.html" ignore missing %}
    {% include "sidebar.html" ignore missing with context %}
    {% include "sidebar.html" ignore missing without context %}

You can also provide a list of templates that are checked for existence before inclusion. The first template that exists will be included. If ignore missing is given, it will fall back to rendering nothing if none of the templates exist, otherwise it will raise an exception.

Example:

    {% include ['page_detailed.html', 'page.html'] %}
    {% include ['special_sidebar.html', 'sidebar.html'] ignore missing %}

### Import

Jinja supports putting often used code into macros. These macros can go into different templates and get imported from there. This works similarly to the import statements in Python. It’s important to know that imports are cached and imported templates don’t have access to the current template variables, just the globals by default. For more details about context behavior of imports and includes, see [Import Context Behavior](https://jinja.palletsprojects.com/en/3.0.x/templates/#import-visibility).

There are two ways to import templates. You can import a complete template into a variable or request specific macros / exported variables from it.

Imagine we have a helper module that renders forms (called forms.html):

    {% macro input(name, value='', type='text') -%}
        <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
    {%- endmacro %}

    {%- macro textarea(name, value='', rows=10, cols=40) -%}
        <textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols
            }}">{{ value|e }}</textarea>
    {%- endmacro %}

The easiest and most flexible way to access a template’s variables and macros is to import the whole template module into a variable. That way, you can access the attributes:

    {% import 'forms.html' as forms %}
    <dl>
        <dt>Username</dt>
        <dd>{{ forms.input('username') }}</dd>
        <dt>Password</dt>
        <dd>{{ forms.input('password', type='password') }}</dd>
    </dl>
    <p>{{ forms.textarea('comment') }}</p>

Alternatively, you can import specific names from a template into the current namespace:

    {% from 'forms.html' import input as input_field, textarea %}
    <dl>
        <dt>Username</dt>
        <dd>{{ input_field('username') }}</dd>
        <dt>Password</dt>
        <dd>{{ input_field('password', type='password') }}</dd>
    </dl>
    <p>{{ textarea('comment') }}</p>

Macros and variables starting with one or more underscores are private and cannot be imported.

### Expressions

Jinja allows basic expressions everywhere. These work very similarly to regular Python; even if you’re not working with Python you should feel comfortable with it.

#### Literals

The simplest form of expressions are literals. Literals are representations for Python objects such as strings and numbers. The following literals exist:

+ "Hello World"
Everything between two double or single quotes is a string. They are useful whenever you need a string in the template (e.g. as arguments to function calls and filters, or just to extend or include a template).

+ 42 / 123_456
Integers are whole numbers without a decimal part. The ‘_’ character can be used to separate groups for legibility.

+ 42.23 / 42.1e2 / 123_456.789
Floating point numbers can be written using a ‘.’ as a decimal mark. They can also be written in scientific notation with an upper or lower case ‘e’ to indicate the exponent part. The ‘_’ character can be used to separate groups for legibility, but cannot be used in the exponent part.

+ ['list', 'of', 'objects']
Everything between two brackets is a list. Lists are useful for storing sequential data to be iterated over. For example, you can easily create a list of links using lists and tuples for (and with) a for loop:

`<ul>
{% for href, caption in [('index.html', 'Index'), ('about.html', 'About'), ('downloads.html', 'Downloads')] %}<li><a href="{{ href }}">{{ caption }}</a></li>{% endfor %}</ul>`

+ ('tuple', 'of', 'values')
Tuples are like lists that cannot be modified (“immutable”). If a tuple only has one item, it must be followed by a comma (('1-tuple',)). Tuples are usually used to represent items of two or more elements. See the list example above for more details.

+ {'dict': 'of', 'key': 'and', 'value': 'pairs'}
A dict in Python is a structure that combines keys and values. Keys must be unique and always have exactly one value. Dicts are rarely used in templates; they are useful in some rare cases such as the xmlattr() filter.

+ true / false
true is always true and false is always false.

___Note The special constants true, false, and none are indeed lowercase. Because that caused confusion in the past, (True used to expand to an undefined variable that was considered false), all three can now also be written in title case (True, False, and None). However, for consistency, (all Jinja identifiers are lowercase) you should use the lowercase versions.___

#### Math

Jinja allows you to calculate with values. This is rarely useful in templates but exists for completeness’ sake. The following operators are supported:

`+`
Adds two objects together. Usually the objects are numbers, but if both are strings or lists, you can concatenate them this way. This, however, is not the preferred way to concatenate strings! For string concatenation, have a look-see at the ~ operator. `{{ 1 + 1 }}` is 2.

`-`
Subtract the second number from the first one. `{{ 3 - 2 }}` is 1.

`/`
Divide two numbers. The return value will be a floating point number. `{{ 1 / 2 }}` is `{{ 0.5 }}`.

`//`
Divide two numbers and return the truncated integer result. `{{ 20 // 7 }}` is 2.

`%`
Calculate the remainder of an integer division. `{{ 11 % 7 }}` is 4.

`*`
Multiply the left operand with the right one. `{{ 2 * 2 }}` would return 4. This can also be used to repeat a string multiple times. `{{ '=' * 80 }}` would print a bar of 80 equal signs.

`**`
Raise the left operand to the power of the right operand. `{{ 2**3 }}` would return 8.

Unlike Python, chained pow is evaluated left to right. `{{ 3**3**3 }}` is evaluated as `(3**3)**3` in Jinja, but would be evaluated as `3**(3**3)` in Python. Use parentheses in Jinja to be explicit about what order you want. It is usually preferable to do extended math in Python and pass the results to render rather than doing it in the template.

This behavior may be changed in the future to match Python, if it’s possible to introduce an upgrade path.

#### Comparisons

`==`
Compares two objects for equality.

`!=`
Compares two objects for inequality.

`>`
true if the left hand side is greater than the right hand side.

`>=`
true if the left hand side is greater or equal to the right hand side.

`<`
true if the left hand side is lower than the right hand side.

`<=`
true if the left hand side is lower or equal to the right hand side.

#### Logic

For if statements, for filtering, and if expressions, it can be useful to combine multiple expressions:

`and`
Return true if the left and the right operand are true.

`or`
Return true if the left or the right operand are true.

`not`
negate a statement (see below).

`(expr)`
Parentheses group an expression.

___Note The is and in operators support negation using an infix notation, too: foo is not bar and foo not in bar instead of not foo is bar and not foo in bar. All other expressions require a prefix notation: not (foo and bar).___

#### Other Operators

The following operators are very useful but don’t fit into any of the other two categories:

`in`
Perform a sequence / mapping containment test. Returns true if the left operand is contained in the right. {{ 1 in [1, 2, 3] }} would, for example, return true.

`is`
Performs a test.

`|` (pipe, vertical bar)
Applies a filter.

`~` (tilde)
Converts all operands into strings and concatenates them.
`{{ "Hello " ~ name ~ "!" }}` would return (assuming name is set to 'John') Hello John!.

`()`
Call a callable: {{ post.render() }}. Inside of the parentheses you can use positional arguments and keyword arguments like in Python:
`{{ post.render(user, full=true) }}.`

`. / []`
Get an attribute of an object. (See Variables)

#### If Expression

It is also possible to use inline if expressions. These are useful in some situations. For example, you can use this to extend from one template if a variable is defined, otherwise from the default layout template:

`{% extends layout_template if layout_template is defined else 'default.html' %}`

The general syntax is `<do something> if <something is true> else <do something else>`.

The else part is optional. If not provided, the else block implicitly evaluates into an Undefined object (regardless of what undefined in the environment is set to):

`{{ "[{}]".format(page.title) if page.title }}`

#### Python Methods

You can also use any of the methods defined on a variable’s type. The value returned from the method invocation is used as the value of the expression. Here is an example that uses methods defined on strings (where page.title is a string):

`{{ page.title.capitalize() }}`
This works for methods on user-defined types. For example, if variable f of type Foo has a method bar defined on it, you can do the following:

`{{ f.bar(value) }}`
Operator methods also work as expected. For example, % implements printf-style for strings:

`{{ "Hello, %s!" % name }}`
Although you should prefer the .format method for that case (which is a bit contrived in the context of rendering a template):

`{{ "Hello, {}!".format(name) }}`
