# Django imports
from django.core.management.commands import makemessages


class Command(makemessages.Command):
    """Wrapper command to add some extra settings:

    1. Add ``_l`` as keyword. So in same file we can use both ``ugettext as _, ugettext_lazy as _l``
    2. Add width=78 - default value in rosetta. So it will be less changes when building file by rosetta and manage.py
    3. Add ``xlwt`` and ``captain`` to ignored folders. Captain takes long to process and we do not translate it now
        XLWT just fails due to enconding problems, and we neither translate it

    See https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#customizing-the-makemessages-command
    about further modifying the command.

    TODO: width=78 seems to help not in the full way, there are many of spaces and line-breaks changes still.
    """
    xgettext_options = makemessages.Command.xgettext_options + [
        '--keyword=_l',
        '--width=78'
    ]

    def handle(self, *args, **options):
        options['ignore_patterns'].extend(['env'])
        return super(Command, self).handle(*args, **options)