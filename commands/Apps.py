import json, sys
from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError, ServerDownError

class Apps(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)

    def change_owner(self, app_id, username):
        self.client.apps.changeAppOwner(appId=app_id, userName=username)
        self.logger.complete(f"Changed owner of app '{app_id}' to {username}")

        return

    def create(self, definition_file) -> None:
        try:
            definition = json.loads(open(definition_file, "r").read())
            self.client.apps.createAppVersion(**definition)
            self.logger.success(f"App \'{definition['id']}\' created")
            return
        except (ServerDownError, InvalidInputError) as e:
            self.logger.error(e)         

    def delete(self, id) -> None:
        try:
            self.client.apps.deleteApp(appId=id)
            print(f"Deleted app with id '{id}'")
            return
        except InvalidInputError:
            print(f"App not found with id '{id}'")
            return

    def get(self, id) -> None:
        try:
            app = self.client.apps.getAppLatestVersion(appId=id)
            self.logger.log(app)
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"{e.message}")
            self.exit(1)

    def getversion(self, id, version) -> None:
        try:
            app = self.client.apps.getApp(appId=id, appVersion=version)
            self.logger.log(app)
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"{e.message}")
            self.exit(1)

    def get_permissions(self, app_id, username):
        creds = self.client.apps.getUserPerms(appId=app_id, userName=username)
        self.logger.log(creds)
        return

    def grant_permissions(self, id, username, *args):
        perms = [arg for arg in args]

        # It turns out the expected input should be a JSONArray, NOT a JSONObject
        self.client.apps.grantUserPerms(appId=id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} granted to user '{username}'")

    def list(self) -> None:
        apps = self.client.apps.getApps()
        if len(apps) > 0:
            for app in apps:
                print(app.id)
            return

        print(f"No apps found for user '{self.client.username}'")
        return

    def undelete(self, id) -> None:
        try:
            self.client.apps.undeleteApp(appId=id)
            print(f"Recovered app with id '{id}'")
            return
        except InvalidInputError:
            print(f"Deleted app not found with id '{id}'")
            return

    def update(self, definition_file) -> None:
        app_definition = json.loads(open(definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            self.client.apps.patchApp(**app_definition)
            self.logger.success(f"App {app_definition['appId']} has been updated")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error( f"{e}" )
            self.exit(1)

    # TODO test
    def put(self, definition_file) -> None:
        app_definition = json.loads(open(definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            self.client.apps.putApp(**app_definition)
            self.logger.success(f"App {app_definition['appId']} has been updated")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error( f"{e}" )
            self.exit(1)