from z3c.schema2json.tools import serialize_to_dict

from kuleuven.lirias.staff.log import logger
from kuleuven.lirias.staff.interfaces import IPublication, ICollection


def process_publications(publications, objectencoder, filter):
    json_input_data = dict()
    logger.debug("++++ Total publications: %s ++++" % (len(publications)))
    for publication in publications:
        logger.debug("adapting publication %s" % publication.id)
        publication_object = IPublication(publication)
        logger.debug("encoding publication %s" % publication.id)
        encoded_object = serialize_to_dict(IPublication, publication_object)
        json_input_data[publication.id] = encoded_object
    logger.info("++++ Total publications: %s ++++" % (len(publications)))
    return json_input_data


def process_collections(collections, objectencoder, filter):
    json_input_data = dict()
    logger.debug("++++ Total collections: %s ++++" % (len(collections)))
    for collection in collections:
        logger.debug("adapting collection %s" % collection.id)
        collection_object = ICollection(collection)
        logger.debug("encoding collection %s" % collection.id)
        encoded_object = serialize_to_dict(ICollection, collection_object)
        json_input_data[collection.id] = encoded_object
    logger.info("++++ Total collections: %s ++++" % (len(collections)))
    return json_input_data


def str2bool(v):
    if isinstance(v, str):
        if v.lower() in ('no', 'n', 'false', 'f', '0', 'none', '[]', '{}', ''):
            return False
        else:
            return True
    if v:
        if len(v) > 0:
            return True
        else:
            return False
    else:
        return False
