import plone.testing
import plone.app.testing
from Products.CMFCore.utils import getToolByName
import kuleuven.publications


def create_users(portal):
    acl_users = getToolByName(portal, 'acl_users')
    acl_users.userFolderAddUser('test_sitemanager', 'secret', ['Manager'], [])
    acl_users.userFolderAddUser('test_manager', 'secret', ['Manager'], [])
    acl_users.portal_role_manager.assignRolesToPrincipal(['Manager'],
                                                        'test_manager')

PUBS_IN_WMS = plone.app.testing.PloneWithPackageLayer(
    name="PUBS_IN_WMS",
    zcml_filename="testing.zcml", zcml_package=kuleuven.publications,
    additional_z2_products=('kuleuven.publications',),
    gs_profile_id="kuleuven.publications:default")


class PubsTesting(plone.app.testing.IntegrationTesting):

    def testSetUp(self):
        super(PubsTesting, self).testSetUp()
        create_users(self['portal'])

PUBS_LAYER = PubsTesting(
    bases=(PUBS_IN_WMS, ),
    name="PUBS_LAYER")
