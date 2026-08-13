from five import grok
from zope.component.hooks import getSite
from kuleuven.wiwo.staff.interfaces import IStaffContainer
from kuleuven.wiwo.staff.browser.base import BaseView


class PersonsList(BaseView):
    grok.name('personslist')
    grok.template('personslist')
    grok.context(IStaffContainer)
    grok.require('zope2.View')

    def getPersonIds(self):
        site = getSite()
        asyncpersonstorage = site.get("persons.async")
        syncpersonstorage = site.get("persons.sync")
        persons_list = list()

        for person in asyncpersonstorage.items():
            persons_list.append(person[0])

        for person in syncpersonstorage.items():
            persons_list.append(person[0])

        return persons_list
