from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError

class Tenants(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)

    def get(self, tenant_id) -> None:
        try:
            tenant = self.client.tenants.get_tenant(tenantId=tenant_id)
            self.logger.log(tenant)
            return
        except InvalidInputError:
            self.logger.error(f"Tenant not found with id '{tenant_id}'")

    def list(self) -> None:
        tenants = self.client.tenants.list_tenants()
        if len(tenants) > 0:
            for tenant in tenants:
                self.logger.log(tenant.tenant_id)
            return

        print(f"No tenants found")
        return
