from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError
import json

class Systems(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)

    def change_owner(self, system_id, username):
        self.client.systems.changeSystemOwner(systemId=system_id, userName=username)
        
        return

    def create(self, definition_file: str) -> None:
        system_definition = json.loads(open(definition_file, "r").read())
        self.client.systems.createSystem(**system_definition)

        return

    def create_user_creds(self, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createUserCredential(**system_definition)

        return

    def delete(self, system_id) -> None:
        try:
            self.client.systems.deleteSystem(systemId=system_id)
            self.logger.info(f"Deleted system with id '{system_id}'")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")
            return

    def get(self, system_id) -> None:
        try:
            system = self.client.systems.getSystem(systemId=system_id)
            self.logger.log(system)
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")

    def get_credentials(self):
            self.logger.warn("get_credentials not implemented")

    def grant_perms(self, id, username, *args):
        perms = { "permissions": [] }
        for arg in args:
            perms.permissions.append(arg.upper())

        self.client.grantUserPerms(systemId=id, userName=username, permissions=json.dumps(perms))
        self.logger.info(f"Permissions {args} granted to user '{username}'")

    def get_permissions(self, system_id, username):
        creds = self.client.systems.getUserPerms(systemId=system_id, userName=username)
        self.logger.log(creds)
        return

    def list(self) -> None:
        systems = self.client.systems.getSystems()
        if len(systems) > 0:
            for system in systems:
                self.logger.log(system.id)
            return

        self.logger.log(f"No systems found for user '{self.client.username}'")
        return

    def undelete(self, system_id) -> None:
        try:
            self.client.systems.undeleteSystem(systemId=system_id)
            self.logger.success(f"Recovered system with id '{system_id}'")
            return
        except InvalidInputError:
            self.logger.info(f"Deleted system not found with id '{system_id}'")
            return

    def update(self, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            self.client.systems.patchSystem(**system_definition)
            self.logger.success(f"System '{system_definition.systemId}' updated")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")

    def update_creds(self, file):
        creds = json.loads(open(file, "r").read())
        self.client.systems.createUserCredential(**creds)