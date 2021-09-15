""" Handles TAPIS functionality related to tenants. """

from core.TapipyCategory import TapipyCategory
from tapipy.errors import InvalidInputError


class Tenants(TapipyCategory):
    """ Contains all CRUD functions associated with tenants. """
    def __init__(self):
        TapipyCategory.__init__(self)

    def get(self, tenant_id) -> None:
        """ Retrieve the details of a specified tenant. """
        try:
            tenant = self.client.tenants.get_tenant(tenantId=tenant_id)
            self.logger.log(tenant)
            print()
            return
        except InvalidInputError:
            self.logger.error(f"Tenant not found with id '{tenant_id}'")

    def list(self) -> None:
        """ List every tenant on the site. """
        tenants = self.client.tenants.list_tenants()
        if len(tenants) > 0:
            print()
            for tenant in tenants:
                self.logger.log(tenant.tenant_id)
            print()
            return

        self.logger.error(f"No tenants found\n")
        return
