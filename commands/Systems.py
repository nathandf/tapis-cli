import json

from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError

class Systems(TapisCommand):
    """ Contains all of the CRUD functions associated with systems. """

    def __init__(self):
        TapisCommand.__init__(self)

    def available(self, system_id) -> None:
        # Check if a system is currently enabled.
        try:
            system = self.client.systems.isEnabled(systemId=system_id)
            status = "enabled" if system.aBool else "disabled" 
            self.logger.info(f"The system {system_id} is {status}")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")

    def change_owner(self, system_id, username):
        # Change the owner of a system (you may lose access to a system
        # if you change the owner to another user and they don't grant you
        # permissions).
        self.client.systems.changeSystemOwner(systemId=system_id, userName=username)
        self.logger.complete(f"Changed owner of system '{system_id}' to {username}")

        return

    def create(self, system_definition_file: str) -> None:
        # Create a new system from a system definition JSON file.
        definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createSystem(**definition)
        self.logger.success(f"System \'{definition['id']}\' created")

        return

    def create_user_creds(self, system_definition_file) -> None:
        # Create new user credentials for accessing a system. This is necessary
        # if the effective user of a system is different than the owner upon
        # system creation.
        system_definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createUserCredential(**system_definition)

        return

    def delete(self, system_id) -> None:
        # "Soft" delete a system; it will not appear in queries. 
        # Systems are still present in the environment and may be undeleted.
        try:
            self.client.systems.deleteSystem(systemId=system_id)
            self.logger.info(f"Deleted system with id '{system_id}'")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")
            return

    def disable(self, system_id) -> None:
        # Mark (all versions of) a system as unavailable for use.
        try:
            self.client.systems.disableSystem(systemId=system_id)
            self.logger.success(f"The system {system_id} was disabled")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")          

    def enable(self, system_id) -> None:
        # Mark (all versions of) a system as available for use.
        try:
            self.client.systems.enableSystem(systemId=system_id)
            self.logger.success(f"The system {system_id} was enabled")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")        

    def get(self, system_id) -> None:
        # Retrieve the details of an system's latest version.
        try:
            system = self.client.systems.getSystem(systemId=system_id)
            self.logger.log(system)
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'")

    def getcreds(self):
        # TODO
            self.logger.warn("get_credentials not implemented")
 
    def getperms(self, system_id, username):
        # Get the permissions that a specified user has on a target system.
        creds = self.client.systems.getUserPerms(systemId=system_id, userName=username)
        self.logger.log(creds)
        return

    def grantperms(self, system_id, username, *args):
        # Give permissions to a specified user on a target application.
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.systems.grantUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} granted to user '{username}'")

    def list(self) -> None:
        # List every system in this tenant and environment.
        systems = self.client.systems.getSystems()
        if len(systems) > 0:
            print()
            for system in systems:
                self.logger.log(system.id)
            print()
            return

        self.logger.log(f"No systems found for user '{self.client.username}'")
        return

    def patch(self, system_definition_file) -> None:
        # Update selected attributes of a system using a system definition
        # JSON file containing only the required and specified attributes. 
        system_definition = json.loads(open(system_definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            self.client.systems.patchSystem(**system_definition)
            self.logger.success(f"System '{system_definition.systemId}' updated")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")

    def put(self, system_definition_file) -> None:
        # Update ALL attributes of a system using a system definition JSON
        # file that contains all the same attributes used to create the system.
        system_definition = json.loads(open(system_definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            self.client.apps.putSystem(**system_definition)
            self.logger.success(f"System {system_definition['appId']} has been updated")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'")
            self.exit(1)

    def revokeperms(self, system_id, username, *args):
        # Revoke permissions from a specified user on a target system.
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject
        self.client.systems.revokeUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} revoked from user '{username}'")

    def search(self, *args) -> None:
        # Retrieve details for systems using attributes as search parameters.
        # Multiple SQL-like queries can be done in the same set of string.
        # EX: "owner = <username> AND systemType = LINUX"
        matched = self.client.systems.searchSystemsRequestBody(search=args)
        for system in matched:
            print(system)

        return

    def undelete(self, system_id) -> None:
        # Undelete an applications that has been "soft" deleted.
        try:
            self.client.systems.undeleteSystem(systemId=system_id)
            self.logger.success(f"Recovered system with id '{system_id}'")
            return
        except InvalidInputError:
            self.logger.info(f"Deleted system not found with id '{system_id}'")
            return

    def update_creds(self, file):
        # Update user credentials using a JSON definition file containing credentials.
        creds = json.loads(open(file, "r").read())
        self.client.systems.createUserCredential(**creds)