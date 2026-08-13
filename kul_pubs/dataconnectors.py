import json
from App.config import getConfiguration
from zope.interface import implements
import logging

from kuleuven.publications.interfaces import IDataConnector

logger = logging.getLogger('publicationsLogger')


class JSONDataConnector(object):
    implements(IDataConnector)

    def __init__(self):
        configuration = self.getPubsConfiguration()
        if not configuration:
            return
        self.host_url = ""
        try:
            self.host_url = configuration.get('publications-service-url')
        except ValueError:
            logger.error("No publications-service-url found in the zope.conf")
            raise
        except AttributeError:
            logger.error("No configuration found")
            raise

    def requestData(self, uri):
        fetched_data = ""
        data = ""
        request_url = "%s?%s" % (self.host_url, uri)
        # logger.info("WMS to Libis: %s", request_url)
        import urllib2
        fetched_data = urllib2.urlopen(request_url)
        if not fetched_data:
            return None

        data = json.load(fetched_data)
        return data

    def getPubsConfiguration(self):
        config = getConfiguration()
        if not hasattr(config, 'product_config'):
            return
        product_config = config.product_config
        if config is None:
            return
        return product_config.get('kuleuven.publications', None)
