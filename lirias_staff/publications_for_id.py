from five import grok
import json
from zope.component import getUtility

from kuleuven.lirias.core.interfaces import IStorage
from kuleuven.lirias.core.interfaces import ILIRIASApplication

from kuleuven.lirias.staff.interfaces import IPublication, IPublicationAuthor,\
                                            IObjectEncoder
from kuleuven.lirias.staff.log import logger
from kuleuven.lirias.staff.browser.utils import process_publications

from kuleuven.lirias.staff.browser.filters import prepare_filter


class PublicationsForId(grok.View):
    grok.name('publications_for_id')
    grok.context(ILIRIASApplication)
    grok.require('zope2.View')

    def render(self):
        self.response.setHeader('Content-Type', 'application/json')

        storage = getUtility(IStorage, 'liriasstorage')
        objectencoder = getUtility(IObjectEncoder, 'objectencoder')
        storage.setup()
        storage.connect()
        interfaces_list = [IPublication, IPublicationAuthor]
        objectencoder.configure(encodable_interfaces=interfaces_list)

        filter = prepare_filter(self.request)

        logger.debug("fetching author %s" % (filter['author_ids'][0]))

        publications = storage.fetch_publications_for_author(
                                                filter=filter)

        json_input_data = dict()
        if len(publications) > 0:
            json_input_data = process_publications(publications, objectencoder,
                    filter)
            storage.disconnect()
        else:
            return "No publications available for id %s" % (
                        filter['author_ids'][0])

        json_data = json.dumps(json_input_data)

        return json_data
