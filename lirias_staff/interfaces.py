from zope.interface import Interface
from zope.schema import TextLine
from zope.schema import List
from zope.schema import Object


class ISchemaToJSon(Interface):
    """Marker interface for ObjectEncoder"""


class IBlah(Interface):
    """Marker interface for ObjectEncoder"""


class IObjectEncoder(Interface):
    """Marker interface for ObjectEncoder"""


class IBasePublication(Interface):
    id = TextLine(
        title=u"publication id",
        description=u"Publication id",
        required=True)

    status = TextLine(
        title=u"publication status",
        description=u"Publication status",
        required=False)

    pub_title = TextLine(
        title=u"journal, book or conf title",
        description=u"Journal, book or conf title",
        required=False)

    pub_info = TextLine(
        title=u"publisher or conference info",
        description=u"Publisher or conference info",
        required=False)

    title = TextLine(
            title=u"publication title",
            description=u"Publication title",
            required=False)

    pub_pages = TextLine(
            title=u"publication pages",
            description=u"Publication pages",
            required=False)

    date_issued = TextLine(
            title=u"publication date_issued",
            description=u"Publication date issued",
            required=False)

    pub_issn = TextLine(
            title=u"publication issn",
            description=u"Publication issn",
            required=False)

    pub_issue = TextLine(
            title=u"publication issue",
            description=u"Publication issue",
            required=False)

    pub_volume = TextLine(
            title=u"journal volume",
            description=u"Journal volume",
            required=False)

    genre = TextLine(
            title=u"genre",
            description=u"Publication genre",
            required=False)

    wos = TextLine(
            title=u"wos",
            description=u"Web os Science",
            required=False)


class IPublication(IBasePublication):
    aut = List(
        value_type=Object(Interface),
        title=u"publication author",
        description=u"Authors for publication",
        default=list(),
        required=False)


class IBaseAuthor(Interface):
    id = TextLine(
            title=u"author id",
            description=u"Author id",
            required=True)

    first_name = TextLine(
            title=u"author first name",
            description=u"Author first name",
            required=False)

    last_name = TextLine(
            title=u"author last name",
            description=u"Author last name",
            required=False)


class IAuthor(IBaseAuthor):
    publications = List(
        value_type=Object(IPublication),
        title=u"publication author",
        description=u"Authors for publication",
        default=list(),
        required=False)


class IPublicationAuthor(IBaseAuthor):
    role = TextLine(
            title=u"author role",
            description=u"Author role",
            required=False)

    author_pos = TextLine(
            title=u"author position",
            description=u"Author position",
            required=False)

IPublication['aut'].value_type.schema = IPublicationAuthor


class ICollection(Interface):
    id = TextLine(
            title=u"collection id",
            description=u"Collection id",
            required=True)

    name = TextLine(
            title=u"collection name",
            description=u"Collection name",
            required=False)
