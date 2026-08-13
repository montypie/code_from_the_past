"""
Schema of the KULPublist content type
"""

from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from plone.autoform import directives as form
from z3c.form.browser.radio import RadioFieldWidget
from zope.schema.vocabulary import SimpleVocabulary
from kuleuven.publications import MessageFactory as _


class IKULPublist(model.Schema):
    """ Publication list as a result of a query """

    colsearch = schema.TextLine(
        title=_(u"Collection name"),
        description=_(u"Full title of a collection from LIRIAS"),
        required=True,
        )

    yearrange = schema.TextLine(
        title=_(u"Year range"),
        description=_(u"Format: XXXX-XXXX. Default 5 last years."),
        max_length=9,
        required=False,
        )

    subkeywords = schema.TextLine(
        title=_(u"Additional keyword(s) from LIRIAS"),
        description=_(u"If several: comma-separated"),
        max_length=50,
        required=False,
        )

    pubsonpage = schema.Choice(
        title=_(u"Number of publications per page"),
        default='25',
        vocabulary=SimpleVocabulary.fromValues(['10', '25', '50', '100']),
        required=True,
        )

    introtext = RichText(
        title=_(u"Introduction"),
        description=_(u"Text preceeding the publication list"),
        required=False,
        )

    language = schema.Choice(
        title=_(u"Language"),
        default='en',
        vocabulary=SimpleVocabulary.fromValues(['en', 'nl']),
        required=True,
        )
    form.widget(language=RadioFieldWidget)
