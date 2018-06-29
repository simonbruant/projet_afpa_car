Custom views
============

.. _styles:

styles
------
Here is a sample of some CSS rules, usable for :file:`postman/views.html`::

    .pm_message.pm_deleted             { text-decoration: line-through; }
    .pm_message.pm_deleted .pm_body    { display: none; }
    .pm_message.pm_archived            { font-style: italic; color: grey; }
    .pm_message.pm_unread .pm_subject  { font-weight: bolder; }
    .pm_message.pm_pending .pm_header  { background-color: #FFC; }
    .pm_message.pm_rejected .pm_header { background-color: #FDD; }

These rules are provided with the application, as an example, in a static file (See :ref:`static files`).

forms
-----

You can replace the default forms in views.

Examples::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^write/(?:(?P<recipients>[^/#]+)/)?$',
            WriteView.as_view(form_classes=(MyCustomWriteForm, MyCustomAnonymousWriteForm)),
            name='write'),
        url(r'^reply/(?P<message_id>[\d]+)/$',
            ReplyView.as_view(form_class=MyCustomFullReplyForm),
            name='reply'),
        url(r'^view/(?P<message_id>[\d]+)/$',
            MessageView.as_view(form_class=MyCustomQuickReplyForm),
            name='view'),
        # ...
    )

templates
---------

You can replace the default template name in all views.

Example::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^view/(?P<message_id>[\d]+)/$',
            MessageView.as_view(template_name='my_custom_view.html'),
            name='view'),
        # ...
    )

after submission
----------------

You can supersede the default view where to return to, after a successful submission.

The default algorithm is:

#. Return where you came from
#. If it cannot be known, fall back to the inbox view
#. But if the submission view has a ``success_url`` parameter, use it preferably
#. In all cases, a ``next`` parameter in the query string has higher precedence

The parameter ``success_url`` is available to these views:

* ``WriteView``
* ``ReplyView``
* ``ArchiveView``
* ``DeleteView``
* ``UndeleteView``

Example::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^reply/(?P<message_id>[\d]+)/$',
            ReplyView.as_view(success_url='postman:inbox'),
            name='reply'),
        # ...
    )

Example::

    <a href="{% url 'postman:reply' reply_to_pk %}?next={{ next_url|urlencode }}">Reply</a>

reply formatters
----------------

You can replace the default formatters used for replying.

Examples::

    def format_subject(subject):
        return "Re_ " + subject

    def format_body(sender, body):
        return "{0} _ {1}".format(sender, body)

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^reply/(?P<message_id>[\d]+)/$',
            ReplyView.as_view(formatters=(format_subject, format_body)),
            name='reply'),
        url(r'^view/(?P<message_id>[\d]+)/$',
            MessageView.as_view(formatters=(format_subject, format_body)),
            name='view'),
        # ...
    )

See also:

* the ``POSTMAN_QUICKREPLY_QUOTE_BODY`` setting in :ref:`optional_settings`
