# -*- coding: utf-8 -*-
from zope.component import queryUtility

from kuleuven.publications.interfaces import IDataConnector
from plone.memoize.ram import cache


def getData(request_uri):
    """ gets the data from json or local for tests """
    data_connector = queryUtility(IDataConnector, 'dataconnector')
    data = data_connector.requestData(request_uri)
    return data


def cache_key(fun, input_indexes, fromnr, step, sortby):
    """ caches result of a function"""
    return (input_indexes, fromnr, step, sortby)


@cache(cache_key)
def fetchPubs(input_indexes, fromnr=1, step=50, sortby='scdate'):
    """ returns publications if any for the given query """
    request_uri = "institution=lirias&from=%s&step=%s&sort=%s&query=%s" % \
        (fromnr, step, sortby, input_indexes)
    pubsresponse = getData(request_uri)
    if pubsresponse['count'] == 0 or \
            not pubsresponse['data']:
        return []

    pubstotal = pubsresponse['count']
    fromnr = pubsresponse['from']
    list_of_pubs = []
    pubsdata = pubsresponse['data']
    for pubitem in pubsdata:
        onepubdata = pubitem['display']

        if 'type' in onepubdata.keys():
            ptype = onepubdata['type'].replace('_', ' ')
            ptype = ptype.replace('conference', 'conf.')
        creators = contributors = pub_info = publisher = backlink = srclink = u''
        if 'creator' in onepubdata.keys():
            creators = onepubdata['creator'].replace(' ;', ';')
        if 'contributor' in onepubdata.keys():
            contributors = onepubdata['contributor']
        if 'ispartof' in onepubdata.keys():
            pub_info = onepubdata['ispartof']
        if not pub_info:
            if 'relation' in onepubdata.keys():
                pub_info = onepubdata['relation']
            else:
                pub_info = '%s, ' % (onepubdata['creationdate'])
        if 'publisher' in onepubdata.keys():
            publisher = onepubdata['publisher']
        if 'links' in pubitem.keys():
            if 'backlink' in pubitem['links']:
                backlink = pubitem['links']['backlink']
            if 'linktorsrc' in pubitem['links']:
                srclinks = pubitem['links']['linktorsrc']
                if type(srclinks) == unicode and 'bitstream' in srclinks:
                    srclink = srclinks
                elif type(srclinks) == list:
                    srclinks = [sl for sl in srclinks if 'bitstream' in sl]
                    if len(srclinks) == 1:
                        srclink = srclinks[0]
                    else:
                        srclink = '%s?mode=full' % (backlink)
        onepubdict = dict(
            ptitle=onepubdata['title'],
            ptype=ptype,
            backlink=backlink,
            srclink=srclink,
            creators=creators,
            contributors=contributors,
            pub_info=pub_info,
            publisher=publisher,
            )
        list_of_pubs.append(onepubdict)

    return (list_of_pubs, pubstotal, fromnr)
