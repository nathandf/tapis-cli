from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError
import json

class Systems(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)

    def available(self, system_id) -> None:
        try:
            system = self.client.systems.isEnabled(systemId=system_id)
            status = "enabled" if system.aBool else "disabled" 
            self.logger.info(f"The system {system_id} is {status}")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")

    def change_owner(self, system_id, username):
        self.client.systems.changeSystemOwner(systemId=system_id, userName=username)
        self.logger.complete(f"Changed owner of system '{system_id}' to {username}")

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

    def disable(self, system_id) -> None:
        try:
            self.client.systems.disableSystem(systemId=system_id)
            self.logger.success(f"The system {system_id} was disabled")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")          

    def enable(self, system_id) -> None:
        try:
            self.client.systems.enableSystem(systemId=system_id)
            self.logger.success(f"The system {system_id} was enabled")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")        

    def get(self, system_id) -> None:
        try:
            system = self.client.systems.getSystem(systemId=system_id)
            self.logger.log(system)
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")

    def getcreds(self):
            self.logger.warn("get_credentials not implemented")
 
    def getperms(self, system_id, username):
        creds = self.client.systems.getUserPerms(systemId=system_id, userName=username)
        self.logger.log(creds)
        return

    def grantperms(self, id, username, *args):
        perms = [arg.upper() for arg in args]

        # It turns out the expected input should be a JSONArray, NOT a JSONObject
        self.client.systems.grantUserPerms(systemId=id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} granted to user '{username}'")

    def list(self) -> None:
        systems = self.client.systems.getSystems()
        if len(systems) > 0:
            for system in systems:
                self.logger.log(system.id)
            return

        self.logger.log(f"No systems found for user '{self.client.username}'")
        return

    def search(self, *args) -> None:
        # Multiple SQL-like queries can be done in the same set of string.
        # EX: "owner = <username> AND systemType = LINUX"
        matched = self.client.systems.searchSystemsRequestBody(search=args)
        for system in matched:
            print(system)

        return

    def revokeperms(self, id, username, *args):
        perms = [arg.upper() for arg in args]

        # It turns out the expected input should be a JSONArray, NOT a JSONObject
        self.client.systems.revokeUserPerms(systemId=id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} revoked from user '{username}'")

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