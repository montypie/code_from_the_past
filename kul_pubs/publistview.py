from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from kuleuven.publications.datafetcher import fetchPubs
from Products.statusmessages.interfaces import IStatusMessage


class PublistView(BrowserView):
    """ Publications list view """

    __call__ = ViewPageTemplateFile('templates/publist.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.step = int(self.context.pubsonpage)
        self.fromnr = request.get('fromnr', 1)
        self.sortby = request.get('sortby', 'scdate')

    def buildPubQuery(self):
        """ form query uri """
        query_params = ""
        index_prefix = "any:Collection"
        col_input = self.context.colsearch
        col_value = ''.join(i for i in col_input if i not in
                            (',', '-', '(', ')', ' ', '&', '/', '@'))
        if col_value:
            query_params += "%s%s" % (index_prefix, col_value.lower())
        from datetime import date
        current_year = date.today().year
        begin_year = current_year - 4
        end_year = current_year
        if self.context.yearrange:
            years = self.context.yearrange.replace(' ', '').split('-')
            if len(years[0]) == 4:
                begin_year = years[0]
            if len(years[1]) == 4:
                end_year = years[1]
        query_params += "+year:[%s+TO+%s]" % (begin_year, end_year)
        if self.context.subkeywords:
            subkwds = self.context.subkeywords.replace(' ', '').lower()
            query_params += "+subject:%s" % (subkwds)
        return query_params

    def getPubsData(self):
        pubsquery = self.buildPubQuery()
        try:
            response = fetchPubs(pubsquery, self.fromnr, self.step, self.sortby)
        except:
            IStatusMessage(self.request).addStatusMessage(
                '(Remote) Service is temporarily unavailable.\
                Please retry later.',
                type='error')
            return None
        return response

    def computePagination(self, total, request_total):
        """ computes total number of pages, as well as
        current, next and previous numbers
        """
        fromnr = int(self.fromnr)
        stepnr = self.step
        pagination = {'pages': 1,
                      'current': 1,
                      'nextnr': None,
                      'prevnr': None,
                      'lastnr': None,
                      }
        if total <= request_total:
            return pagination
        pages = (total+stepnr)/stepnr
        pagination['pages'] = pages
        pagination['lastnr'] = stepnr * (pages - 1) + 1
        current = fromnr/stepnr + 1
        pagination['current'] = current
        if fromnr > 1:
            pagination['prevnr'] = fromnr - stepnr
        if current < pages:
            pagination['nextnr'] = fromnr + stepnr
        return pagination
