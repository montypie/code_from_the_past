import grokcore.component as grok

from zope.schema._bootstrapfields import Field
from zope.schema._field import AbstractCollection, Dict

from kuleuven.lirias.staff.interfaces import IObjectEncoder


class ObjectEncoder(grok.GlobalUtility):
    grok.implements(IObjectEncoder)
    grok.name('objectencoder')

    def configure(self, encodable_interfaces):
        self.encodable_interfaces = []
        self.encodable_interfaces.extend(encodable_interfaces)

    def encode(self, input_object):
        object_interface = None
        output_data = dict()
        # detect the object interface
        for iface in self.encodable_interfaces:
            if iface.providedBy(input_object):
                object_interface = iface
                break

        # now loop over the object attributes
        # to create the output dictionary
        for obj_attr in object_interface:
            # check if the attribute is a zope.schema object type
            # if so, try to encode it on it's own
            # get the zope.schema class from the attribute
            attr_type = object_interface[obj_attr]

            # encode lists, sets, typles, ...
            if isinstance(attr_type, AbstractCollection):
                sequence_data = self.encode_sequence(
                        object_interface=object_interface,
                        attr_name=obj_attr,
                        attrs_sequence=input_object.__getattribute__(obj_attr))
                output_data[obj_attr] = sequence_data[obj_attr]

            # encode dictionaries
            if isinstance(attr_type, Dict):

                self.encode_dict(object_interface=object_interface,
                        attr_name=obj_attr,
                        attr=input_object.__getattribute__(obj_attr))

            # all types derived from Field can be encoded directly
            # except for the ones listed above
            if isinstance(attr_type, Field) \
                            and not isinstance(attr_type, Dict)\
                            and not isinstance(attr_type, AbstractCollection):
                output_data[obj_attr] = input_object.__getattribute__(obj_attr)

        return output_data

    def encode_sequence(self, object_interface, attr_name, attrs_sequence):
        # check if the attribute is a zope.schema object type
        # if so, try to encode it on it's own
        sequence_data = list()
        output_data = dict()
        if attr_name in object_interface._InterfaceClass__attrs.keys():
            for object in attrs_sequence:
                pass
                value = self.encode(object)
                sequence_data.append(value)

            output_data[attr_name] = sequence_data
        else:
            raise NotImplemented

        return output_data

    def encode_dict(self, object_interface, attr_name, attr):
        pass
