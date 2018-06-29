.. _quickstart:

Quick start guide
=================

Requisites and dependances
--------------------------

Python version >= 2.6 or >= 3.3

Some reasons:

* (2.6) use of ``str.format()``

Django version >= 1.5 on py2, >= 1.5.5 on py3

Some reasons:

* (1.5/py2) ``url`` template tag syntax
* (1.5.5/py3) Six version >= 1.4.0
* (1.4.2) use of the Six library for supporting Python 2 and 3 in a single codebase

Installation
------------
Get the code from the repository, which is hosted at `Bitbucket <https://bitbucket.org/>`_.

You have two main ways to obtain the latest code and documentation:

With the version control software Mercurial installed, get a local copy by typing::

    hg clone https://bitbucket.org/psam/django-postman/

Or download a copy of the package, which is available in several compressed formats,
either from the ``Download`` tab or from the ``get source`` menu option.

In both case, make sure the directory is accessible from the Python import path.

Configuration
-------------

Required settings
~~~~~~~~~~~~~~~~~

Add ``postman`` to the ``INSTALLED_APPS`` setting of your project.

Run a :command:`manage.py migrate` (or for Django <= 1.6 :command:`manage.py syncdb`)

Include the URLconf ``postman.urls`` in your project's root URL configuration.

.. _optional_settings:

Optional settings
~~~~~~~~~~~~~~~~~

If you want to make use of a ``postman_unread_count`` context variable in your templates,
add ``postman.context_processors.inbox`` to the ``TEMPLATE_CONTEXT_PROCESSORS`` setting
of your project.

You may specify some additional configuration options in your :file:`settings.py`:

``POSTMAN_I18N_URLS``
    *New in version 3.5.0.*

    Set it to True if you want the internationalization of URL patterns.
    Translations are provided by the language files.

    *Defaults to*: False.

``POSTMAN_DISALLOW_ANONYMOUS``
    Set it to True if you do not allow visitors to write to users.
    That way, messaging is restricted to a User-to-User exchange.

    *Defaults to*: False.

``POSTMAN_DISALLOW_MULTIRECIPIENTS``
    Set it to True if you do not allow more than one username in the recipient field.

    *Defaults to*: False.

``POSTMAN_DISALLOW_COPIES_ON_REPLY``
    Set it to True if you do not allow additional recipients when replying.

    *Defaults to*: False.

``POSTMAN_DISABLE_USER_EMAILING``
    Set it to True if you do not want basic email notification to users.
    This setting does not apply to visitors (refer to ``POSTMAN_DISALLOW_ANONYMOUS``),
    nor to a notifier application (refer to ``POSTMAN_NOTIFIER_APP``)

    *Defaults to*: False.

``POSTMAN_FROM_EMAIL``
    *New in version 3.6.0.*

    Set it if you want to override the default 'from' field value.

    *Defaults to*: DEFAULT_FROM_EMAIL.

``POSTMAN_PARAMS_EMAIL``
    *New in version 3.6.0.*

    You can customize the sending of emails by this means.
    The value is a function, receiving one parameter: a dictionary with the same context variables
    as for the subject and body template rendering: {'site': ..., 'object': ..., 'action': ...}.
    The return must be a dictionary, possibly empty, with django.core.mail.EmailMessage parameters as keys.

    *Defaults to*: None.

    Example::

        def get_params_email(context):
            return {
                'reply_to': ['someone@domain.tld'],
                'headers': {'X-my-choice': 'my-value'}
            } if context['action'] == 'acceptance' else {}
        POSTMAN_PARAMS_EMAIL = get_params_email  # default is None

    Notes:

    * 'reply_to' is available as of Django 1.8. For previous versions, you can embed it under 'headers' as:
      ``{'Reply-To': 'someone@domain.tld'}``
    * In case of use of django-mailer (v1.2.2), only 'headers' is supported and
      to the condition that a HTML-version email template is involved.

``POSTMAN_AUTO_MODERATE_AS``
    The default moderation status when no auto-moderation functions, if any, were decisive.

    * ``True`` to accept messages.
    * ``False`` to reject messages.
    * ``None`` to leave messages to a moderator review.

    *Defaults to*: None.

    To disable the moderation feature (no control, no filter):

    * Set this option to True
    * Do not provide any auto-moderation functions

``POSTMAN_SHOW_USER_AS``
    How to represent a User for display, in message properties: ``obfuscated_recipient`` and ``obfuscated_sender``,
    and in the ``or_me`` filter. The value can be specified as:

    * The name of a property of User. For example: 'last_name'.
    * The name of a method of User. For example: 'get_full_name'.
    * A function, receiving the User instance as the only parameter. For example: ``lambda u: u.get_profile().nickname``.
    * *New in version 3.3.0.* The full path to a function, as a string, whose import will be deferred. For example: 'myapp.mymodule.myfunc'.
      The function is given the User object as the only parameter. This sort of reference can be useful when resolving
      circular import dependencies between applications or modules. Another approach, not promoted but compatible, is
      to specify a class instead of a function, like 'myapp.mymodule.MyClass'. In that case, an instance of the class
      is initialized with the User object and its representation is the final result.
    * ``None`` : the default text representation of the User (username) is used.

    *Defaults to*: None.

    The default behaviour is used as a fallback when: the value names an attribute and the result is false
    (misspelled attribute name, empty result, ...), or the value names a function and an exception is raised
    (but any result, even empty, is valid).

``POSTMAN_NAME_USER_AS``
    *New in version 3.3.0.*

    How to name a User as a recipient. The value can be specified as:

    * The name of a property of User. For example: 'last_name' (in auth.User)  or 'nick_name' (in a Custom User Model).
    * ``None`` : the default User model attributes are used: USERNAME_FIELD and get_username().

    *Defaults to*: None.

``POSTMAN_QUICKREPLY_QUOTE_BODY``
    *New in version 3.2.0.*

    Set it to True if you want the original message to be quoted when replying directly from the display view.
    This setting does not apply to the reply view in which quote is the basic behaviour.

    *Defaults to*: False.

``POSTMAN_NOTIFIER_APP``
    A notifier application name, used in preference to the basic emailing,
    to notify users of their rejected or received messages.

    *Defaults to*: 'notification', as in django-notification.

    Note: django-notification v0.2.0 works with Django version 1.3. As of Django 1.4, switch to at least django-notification v1.0.

    If you already have a notifier application with the default name in the installed applications
    but you do not want it to be used by this application, set the option to None.

``POSTMAN_MAILER_APP``
    An email application name, used in preference to the basic django.core.mail, to send emails.

    *Defaults to*: 'mailer', as in django-mailer.

    If you already have a mailer application with the default name in the installed applications
    but you do not want it to be used by this application, set the option to None.

``POSTMAN_AUTOCOMPLETER_APP``
    An auto-completer application specification, useful for recipient fields.
    To enable the feature, define a dictionary with these keys:

    * 'name'
        The name of the auto-completer application.
        Defaults to 'ajax_select'.
    * 'field'
        The model class name.
        Defaults to 'AutoCompleteField'.
    * 'arg_name'
        The name of the argument.
        Defaults to 'channel'.
    * 'arg_default'
        No default value. This is a mandatory default value, but you may supersede it in the field
        definition of a custom form or pass it in the url pattern definitions.

    *Defaults to*: an empty dictionary.

Templates
~~~~~~~~~
A complete set of working templates is provided with the application.
You may use it as it is with a CSS design of yours, re-use it or extend some parts of it,
or only view it as an example.

Don't forget that you shouldn't modify the templates provided into the package
(changes are lost with an application update) but use a copied set pointed to by the ``DIRS`` entry in TEMPLATES setting.

You may need to adjust some templates to match your version of Django.
Permute the comment tags for the lines denoted by the marks: ``{# dj v1.x #}`` in:

* (currently no case)

Relations between templates::

    base.html
    |_ base_folder.html
    |  |_ inbox.html
    |  |_ sent.html
    |  |_ archives.html
    |  |_ trash.html
    |_ base_write.html
    |  |_ write.html
    |  |_ reply.html
    |_ view.html

The :file:`postman/base.html` template extends a :file:`base.html` site template,
in which some blocks are expected:

* title: in <html><head><title>, at least for a part of the entire title string
* extrahead: in <html><head>, to put some <script> and <link> elements
* content: in <html><body>, to put the page contents
* postman_menu: in <html><body>, to put a navigation menu

.. _static files:

Static Files
~~~~~~~~~~~~

A CSS file is provided with the application, for the Admin site: :file:`postman/css/admin.css`.
It is not mandatory but makes the display more comfortable.

A basic CSS file is provided to style the views: :file:`postman/css/postman.css`.
You may use it as a starting point to make your own design.

These files are provided under :file:`postman/static/`.

See also :ref:`styles` for the stylesheets of views.

For Django 1.3+, just follow the instructions related to the staticfiles app.

Examples
--------

:file:`settings.py`::

    INSTALLED_APPS = (
        # 'dj_pagination'  # has to be before postman
        # ...
        'postman',
        # ...
        # 'ajax_select'
        # 'notification'
        # 'mailer'
    )
    # POSTMAN_I18N_URLS = True  # default is False
    # POSTMAN_DISALLOW_ANONYMOUS = True  # default is False
    # POSTMAN_DISALLOW_MULTIRECIPIENTS = True  # default is False
    # POSTMAN_DISALLOW_COPIES_ON_REPLY = True  # default is False
    # POSTMAN_DISABLE_USER_EMAILING = True  # default is False
    # POSTMAN_FROM_EMAIL = 'from@host.tld'  # default is DEFAULT_FROM_EMAIL
    # POSTMAN_PARAMS_EMAIL = get_params_email  # default is None
    # POSTMAN_AUTO_MODERATE_AS = True  # default is None
    # POSTMAN_SHOW_USER_AS = 'get_full_name'  # default is None
    # POSTMAN_NAME_USER_AS = 'last_name'  # default is None
    # POSTMAN_QUICKREPLY_QUOTE_BODY = True  # default is False
    # POSTMAN_NOTIFIER_APP = None  # default is 'notification'
    # POSTMAN_MAILER_APP = None  # default is 'mailer'
    # POSTMAN_AUTOCOMPLETER_APP = {
        # 'name': '',  # default is 'ajax_select'
        # 'field': '',  # default is 'AutoCompleteField'
        # 'arg_name': '',  # default is 'channel'
        # 'arg_default': 'postman_friends',  # no default, mandatory to enable the feature
    # }  # default is {}

:file:`urls.py`::

    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
