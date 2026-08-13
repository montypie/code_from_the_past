from kuleuven.lirias.staff.browser.utils import str2bool


def prepare_filter(request):
    filter = dict()

    #fetching data from request
    # a list of author_ids is provided, comma separated
    if "author_ids" in request.keys():
        author_ids = request.get('author_ids', list())
        if author_ids:
            list_author_ids = author_ids.split(',')
            author_ids = [id.upper() for id in list_author_ids]
            filter['author_ids'] = author_ids

    # one single author_id is provided
    if "author_id" in request.keys():
        author_id = request.get('author_id', list())
        if author_id:
            author_id = author_id.upper()
        filter['author_ids'] = [author_id, ]

    first_author = str2bool(request.get('first_author', None))
    key_publications = request.get('key_publications', list())
    from_date = request.get('from_date', None)
    until_date = request.get('until_date', None)
    international = str2bool(request.get('international', None))
    wos = str2bool(request.get('wos', None))
    genres = request.get('genres', list())
    status = str2bool(request.get('status', None))
    collection = request.get('collection', None)

    #storing it in the filter dict
    filter['first_author'] = first_author
    filter['key_publications'] = key_publications
    if key_publications:
        filter['key_publications'] = \
            filter["key_publications"].replace(" ", "").split(',')
    filter['from_date'] = from_date
    filter['until_date'] = until_date
    filter['international'] = international
    filter['wos'] = wos
    filter['collection'] = collection
    if genres:
        filter['genres'] = \
            genres.split(',')
    filter['status'] = status

    return filter
