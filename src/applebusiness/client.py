import asyncio
from datetime import UTC, datetime

import aiohttp

from .auth import retrieve_oauth_token
from .errors import ClientError, ErrorResponse
from .schemas import (
    AppleCareCoverageResponse,
    AppResponse,
    AppsResponse,
    AuditEventsResponse,
    BlueprintAppsLinkagesResponse,
    BlueprintConfigurationsLinkagesResponse,
    BlueprintOrgDevicesLinkagesResponse,
    BlueprintPackagesLinkagesResponse,
    BlueprintResponse,
    BlueprintsResponse,
    BlueprintUserGroupsLinkagesResponse,
    BlueprintUsersLinkagesResponse,
    Configuration,
    ConfigurationResponse,
    ConfigurationsResponse,
    MdmDeviceDetailResponse,
    MdmDevicesResponse,
    MdmServerDevicesLinkagesResponse,
    MdmServerResponse,
    MdmServersResponse,
    OrgDeviceActivityResponse,
    OrgDeviceAssignedServerLinkageResponse,
    OrgDeviceResponse,
    OrgDevicesResponse,
    PackageResponse,
    PackagesResponse,
    UserGroupResponse,
    UserGroupsResponse,
    UserGroupUsersLinkagesResponse,
    UserResponse,
    UsersResponse,
)

__all__ = ["Client"]


class Client:
    def __init__(self, key_id: str, client_id: str, private_key_pem: str):
        self.key_id = key_id
        self.client_id = client_id
        self.private_key_pem = private_key_pem
        self.client: aiohttp.ClientSession
        self._cached_token: dict | None = None

    async def _get_cached_token(self) -> dict | None:
        """Overridable method to get cached token, can be implemented to fetch from external cache like Redis."""
        return self._cached_token

    async def _set_cached_token(self, token: dict):
        """Overridable method to set cached token, can be implemented to store in external cache like Redis."""
        self._cached_token = token

    async def _get_current_oauth_token(self) -> str:
        now = datetime.now(UTC).timestamp()
        token = await self._get_cached_token()
        # Refresh if token expires in the next minute
        if not token or token["expires_at"] < now + 60:
            token = await retrieve_oauth_token(
                self.key_id, self.client_id, self.private_key_pem
            )
            token["expires_at"] = now + token["expires_in"]
            await self._set_cached_token(token)
        return token["access_token"]

    async def __aenter__(self):
        import aiohttp

        token = await self._get_current_oauth_token()
        self.client = aiohttp.ClientSession(
            base_url="https://api-business.apple.com/",
            trust_env=False,
            headers={"Authorization": f"Bearer {token}"},
        )
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        async with self.client.request(method, path, **kwargs) as response:
            if response.status >= 400:
                error_data = await response.text()
                error_response = None
                try:
                    error_data = await response.json()
                    error_response = ErrorResponse.model_validate(error_data)
                except Exception:
                    pass
                raise ClientError(response.status, error_response, error_data)
            if response.status == 204:
                return {}
            return await response.json()

    async def get_org_devices(self) -> OrgDevicesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-org-devices"""
        data = await self._request("GET", "/v1/orgDevices")
        return OrgDevicesResponse.model_validate(data)

    async def get_org_device(self, id: str) -> OrgDeviceResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-orgdevice-information"""
        data = await self._request("GET", f"/v1/orgDevices/{id}")
        return OrgDeviceResponse.model_validate(data)

    async def get_mdm_devices(self) -> MdmDevicesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-apple-mdm-enrolled-devices"""
        data = await self._request("GET", "/v1/mdmDevices")
        return MdmDevicesResponse.model_validate(data)

    async def get_mdm_device_details(self, id: str) -> MdmDeviceDetailResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-the-details-for-apple-mdm-enrolled-device"""
        data = await self._request("GET", f"/v1/mdmDevices/{id}/details")
        return MdmDeviceDetailResponse.model_validate(data)

    async def get_mdm_servers(self) -> MdmServersResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-device-management-services"""
        data = await self._request("GET", "/v1/mdmServers")
        return MdmServersResponse.model_validate(data)

    async def get_org_device_assigned_server_id(self, id: str) -> str:
        """https://developer.apple.com/documentation/applebusinessapi/get-the-assigned-device-management-service-id-for-an-orgdevice"""
        data = await self._request(
            "GET", f"/v1/orgDevices/{id}/relationships/assignedServer"
        )
        return OrgDeviceAssignedServerLinkageResponse.model_validate(data).data.id

    async def get_org_device_assigned_server(self, id: str) -> MdmServerResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-the-assigned-device-management-service-information-for-an-orgdevice"""
        data = await self._request("GET", f"/v1/orgDevices/{id}/assignedServer")
        return MdmServerResponse.model_validate(data)

    async def _create_org_device_activity(
        self,
        activity_type: str,
        device_ids: list[str],
        server_id: str,
        wait: bool,
        timeout: float | None,
    ) -> OrgDeviceActivityResponse:
        data = await self._request(
            "POST",
            "/v1/orgDeviceActivities",
            json={
                "data": {
                    "type": "orgDeviceActivities",
                    "attributes": {"activityType": activity_type},
                    "relationships": {
                        "devices": {
                            "data": [
                                {"id": device_id, "type": "orgDevices"}
                                for device_id in device_ids
                            ]
                        },
                        "mdmServer": {"data": {"id": server_id, "type": "mdmServers"}},
                    },
                },
            },
        )
        activity = OrgDeviceActivityResponse.model_validate(data)
        if wait:
            deadline = (
                asyncio.get_running_loop().time() + timeout
                if timeout is not None
                else None
            )
            wait_seconds = 1.0
            while activity.data.attributes.status == "IN_PROGRESS":
                if (
                    deadline is not None
                    and asyncio.get_running_loop().time() >= deadline
                ):
                    raise TimeoutError(
                        f"orgDeviceActivity {activity.data.id} did not complete within {timeout}s"
                    )
                await asyncio.sleep(wait_seconds)
                activity = await self.get_org_device_activity(activity.data.id)
                wait_seconds = min(wait_seconds * 1.5, 30)
        return activity

    async def assign_devices_to_server(
        self,
        device_ids: list[str],
        server_id: str,
        wait: bool = True,
        timeout: float | None = 300,
    ) -> OrgDeviceActivityResponse:
        """https://developer.apple.com/documentation/applebusinessapi/assign-an-orgdevice-to-a-mdmserver"""
        return await self._create_org_device_activity(
            "ASSIGN_DEVICES", device_ids, server_id, wait, timeout
        )

    async def unassign_devices_from_server(
        self,
        device_ids: list[str],
        server_id: str,
        wait: bool = True,
        timeout: float | None = 300,
    ) -> OrgDeviceActivityResponse:
        """https://developer.apple.com/documentation/applebusinessapi/assign-an-orgdevice-to-a-mdmserver"""
        return await self._create_org_device_activity(
            "UNASSIGN_DEVICES", device_ids, server_id, wait, timeout
        )

    async def get_org_device_activity(self, id: str) -> OrgDeviceActivityResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-orgdeviceactivity-information"""
        data = await self._request("GET", f"/v1/orgDeviceActivities/{id}")
        return OrgDeviceActivityResponse.model_validate(data)

    async def get_blueprints(self) -> BlueprintsResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-blueprints"""
        data = await self._request("GET", "/v1/blueprints")
        return BlueprintsResponse.model_validate(data)

    async def create_blueprint(
        self,
        name: str,
        description: str = "",
        app_ids: list[str] | None = None,
        configuration_ids: list[str] | None = None,
        device_ids: list[str] | None = None,
        package_ids: list[str] | None = None,
        user_group_ids: list[str] | None = None,
        user_ids: list[str] | None = None,
    ) -> BlueprintResponse:
        """https://developer.apple.com/documentation/applebusinessapi/create-a-blueprint"""
        relationships = {}
        if app_ids:
            relationships["apps"] = {
                "data": [{"id": app_id, "type": "apps"} for app_id in app_ids]
            }
        if configuration_ids:
            relationships["configurations"] = {
                "data": [
                    {"id": config_id, "type": "configurations"}
                    for config_id in configuration_ids
                ]
            }
        if device_ids:
            relationships["orgDevices"] = {
                "data": [
                    {"id": device_id, "type": "orgDevices"} for device_id in device_ids
                ]
            }
        if package_ids:
            relationships["packages"] = {
                "data": [
                    {"id": package_id, "type": "packages"} for package_id in package_ids
                ]
            }
        if user_group_ids:
            relationships["userGroups"] = {
                "data": [
                    {"id": group_id, "type": "userGroups"}
                    for group_id in user_group_ids
                ]
            }
        if user_ids:
            relationships["users"] = {
                "data": [{"id": user_id, "type": "users"} for user_id in user_ids]
            }
        data = await self._request(
            "POST",
            "/v1/blueprints",
            json={
                "data": {
                    "type": "blueprints",
                    "attributes": {"name": name, "description": description},
                    "relationships": relationships,
                }
            },
        )
        return BlueprintResponse.model_validate(data)

    async def update_blueprint(
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
        app_ids: list[str] | None = None,
        configuration_ids: list[str] | None = None,
        device_ids: list[str] | None = None,
        package_ids: list[str] | None = None,
        user_group_ids: list[str] | None = None,
        user_ids: list[str] | None = None,
    ) -> BlueprintResponse:
        """https://developer.apple.com/documentation/applebusinessapi/update-a-blueprint"""
        attributes = {}
        if name is not None:
            attributes["name"] = name
        if description is not None:
            attributes["description"] = description
        relationships = {}
        if app_ids is not None:
            relationships["apps"] = {
                "data": [{"id": app_id, "type": "apps"} for app_id in app_ids]
            }
        if configuration_ids is not None:
            relationships["configurations"] = {
                "data": [
                    {"id": config_id, "type": "configurations"}
                    for config_id in configuration_ids
                ]
            }
        if device_ids is not None:
            relationships["orgDevices"] = {
                "data": [
                    {"id": device_id, "type": "orgDevices"} for device_id in device_ids
                ]
            }
        if package_ids is not None:
            relationships["packages"] = {
                "data": [
                    {"id": package_id, "type": "packages"} for package_id in package_ids
                ]
            }
        if user_group_ids is not None:
            relationships["userGroups"] = {
                "data": [
                    {"id": group_id, "type": "userGroups"}
                    for group_id in user_group_ids
                ]
            }
        if user_ids is not None:
            relationships["users"] = {
                "data": [{"id": user_id, "type": "users"} for user_id in user_ids]
            }
        data = await self._request(
            "PATCH",
            f"/v1/blueprints/{id}",
            json={
                "data": {
                    "type": "blueprints",
                    "id": id,
                    "attributes": attributes,
                    "relationships": relationships,
                }
            },
        )
        return BlueprintResponse.model_validate(data)

    async def delete_blueprint(self, id: str) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/delete-a-blueprint"""
        await self._request("DELETE", f"/v1/blueprints/{id}")

    async def get_configurations(self) -> ConfigurationsResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-configurations"""
        data = await self._request("GET", "/v1/configurations")
        return ConfigurationsResponse.model_validate(data)

    async def create_configuration(
        self,
        name: str,
        type: str,
        configured_for_platforms: list[str] | None = None,
        custom_profile: str | None = None,
        custom_filename: str = "settings.mobileconfig",
    ) -> ConfigurationResponse:
        """https://developer.apple.com/documentation/applebusinessapi/create-a-configuration"""
        attributes: dict = {
            "name": name,
            "type": type,
        }
        if configured_for_platforms is not None:
            attributes["configuredForPlatforms"] = configured_for_platforms
        if custom_profile is not None:
            attributes["customSettingsValues"] = {
                "configurationProfile": custom_profile,
                "filename": custom_filename,
            }
        data = await self._request(
            "POST",
            "/v1/configurations",
            json={
                "data": {
                    "type": "configurations",
                    "attributes": attributes,
                }
            },
        )
        return ConfigurationResponse.model_validate(data)

    async def get_configuration(self, id: str) -> Configuration:
        data = await self._request("GET", f"/v1/configurations/{id}")
        return Configuration.model_validate(data["data"])

    async def update_configuration(
        self,
        id: str,
        name: str | None = None,
        configured_for_platforms: list[str] | None = None,
        custom_profile: str | None = None,
        custom_filename: str = "settings.mobileconfig",
    ) -> Configuration:
        attributes = {}
        if name is not None:
            attributes["name"] = name
        if configured_for_platforms is not None:
            attributes["configuredForPlatforms"] = configured_for_platforms
        if custom_profile is not None:
            attributes["customSettingsValues"] = {
                "configurationProfile": custom_profile,
                "filename": custom_filename,
            }
        data = await self._request(
            "PATCH",
            f"/v1/configurations/{id}",
            json={
                "data": {
                    "id": id,
                    "type": "configurations",
                    "attributes": attributes,
                }
            },
        )
        return Configuration.model_validate(data["data"])

    async def delete_configuration(self, id: str) -> None:
        await self._request("DELETE", f"/v1/configurations/{id}")

    async def get_org_device_apple_care_coverage(
        self, id: str, limit: int | None = None
    ) -> AppleCareCoverageResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-applecare-coverage-for-an-orgdevice"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/orgDevices/{id}/appleCareCoverage", params=params
        )
        return AppleCareCoverageResponse.model_validate(data)

    async def get_mdm_server_device_ids(
        self, id: str, limit: int | None = None
    ) -> MdmServerDevicesLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-device-ids-for-a-device-management-service"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/mdmServers/{id}/relationships/devices", params=params
        )
        return MdmServerDevicesLinkagesResponse.model_validate(data)

    async def get_users(self, limit: int | None = None) -> UsersResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-users"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request("GET", "/v1/users", params=params)
        return UsersResponse.model_validate(data)

    async def get_user(self, id: str) -> UserResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-user-information"""
        data = await self._request("GET", f"/v1/users/{id}")
        return UserResponse.model_validate(data)

    async def get_user_groups(self, limit: int | None = None) -> UserGroupsResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-user-groups"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request("GET", "/v1/userGroups", params=params)
        return UserGroupsResponse.model_validate(data)

    async def get_user_group(self, id: str) -> UserGroupResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-usergroup-information"""
        data = await self._request("GET", f"/v1/userGroups/{id}")
        return UserGroupResponse.model_validate(data)

    async def get_user_group_user_ids(
        self, id: str, limit: int | None = None
    ) -> UserGroupUsersLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-user-ids-for-a-user-group"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/userGroups/{id}/relationships/users", params=params
        )
        return UserGroupUsersLinkagesResponse.model_validate(data)

    async def get_apps(self, limit: int | None = None) -> AppsResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-apps"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request("GET", "/v1/apps", params=params)
        return AppsResponse.model_validate(data)

    async def get_app(self, id: str) -> AppResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-app-information"""
        data = await self._request("GET", f"/v1/apps/{id}")
        return AppResponse.model_validate(data)

    async def get_packages(self, limit: int | None = None) -> PackagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-packages"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request("GET", "/v1/packages", params=params)
        return PackagesResponse.model_validate(data)

    async def get_package(self, id: str) -> PackageResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-package-information"""
        data = await self._request("GET", f"/v1/packages/{id}")
        return PackageResponse.model_validate(data)

    async def get_blueprint(self, id: str) -> BlueprintResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-blueprint-information"""
        data = await self._request("GET", f"/v1/blueprints/{id}")
        return BlueprintResponse.model_validate(data)

    async def _linkages_modify(
        self,
        method: str,
        path: str,
        ids: list[str],
        type_: str,
    ) -> None:
        await self._request(
            method,
            path,
            json={"data": [{"id": i, "type": type_} for i in ids]},
        )

    async def get_blueprint_app_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintAppsLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-app-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/blueprints/{id}/relationships/apps", params=params
        )
        return BlueprintAppsLinkagesResponse.model_validate(data)

    async def add_apps_to_blueprint(self, id: str, app_ids: list[str]) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-apps-to-a-blueprint"""
        await self._linkages_modify(
            "POST", f"/v1/blueprints/{id}/relationships/apps", app_ids, "apps"
        )

    async def remove_apps_from_blueprint(self, id: str, app_ids: list[str]) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-apps-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE", f"/v1/blueprints/{id}/relationships/apps", app_ids, "apps"
        )

    async def get_blueprint_configuration_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintConfigurationsLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-configuration-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET",
            f"/v1/blueprints/{id}/relationships/configurations",
            params=params,
        )
        return BlueprintConfigurationsLinkagesResponse.model_validate(data)

    async def add_configurations_to_blueprint(
        self, id: str, configuration_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-configurations-to-a-blueprint"""
        await self._linkages_modify(
            "POST",
            f"/v1/blueprints/{id}/relationships/configurations",
            configuration_ids,
            "configurations",
        )

    async def remove_configurations_from_blueprint(
        self, id: str, configuration_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-configurations-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE",
            f"/v1/blueprints/{id}/relationships/configurations",
            configuration_ids,
            "configurations",
        )

    async def get_blueprint_package_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintPackagesLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-package-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/blueprints/{id}/relationships/packages", params=params
        )
        return BlueprintPackagesLinkagesResponse.model_validate(data)

    async def add_packages_to_blueprint(self, id: str, package_ids: list[str]) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-packages-to-a-blueprint"""
        await self._linkages_modify(
            "POST",
            f"/v1/blueprints/{id}/relationships/packages",
            package_ids,
            "packages",
        )

    async def remove_packages_from_blueprint(
        self, id: str, package_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-packages-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE",
            f"/v1/blueprints/{id}/relationships/packages",
            package_ids,
            "packages",
        )

    async def get_blueprint_org_device_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintOrgDevicesLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-orgdevice-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/blueprints/{id}/relationships/orgDevices", params=params
        )
        return BlueprintOrgDevicesLinkagesResponse.model_validate(data)

    async def add_org_devices_to_blueprint(
        self, id: str, device_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-org-devices-to-a-blueprint"""
        await self._linkages_modify(
            "POST",
            f"/v1/blueprints/{id}/relationships/orgDevices",
            device_ids,
            "orgDevices",
        )

    async def remove_org_devices_from_blueprint(
        self, id: str, device_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-org-devices-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE",
            f"/v1/blueprints/{id}/relationships/orgDevices",
            device_ids,
            "orgDevices",
        )

    async def get_blueprint_user_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintUsersLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-user-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/blueprints/{id}/relationships/users", params=params
        )
        return BlueprintUsersLinkagesResponse.model_validate(data)

    async def add_users_to_blueprint(self, id: str, user_ids: list[str]) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-users-to-a-blueprint"""
        await self._linkages_modify(
            "POST", f"/v1/blueprints/{id}/relationships/users", user_ids, "users"
        )

    async def remove_users_from_blueprint(self, id: str, user_ids: list[str]) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-users-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE", f"/v1/blueprints/{id}/relationships/users", user_ids, "users"
        )

    async def get_blueprint_user_group_ids(
        self, id: str, limit: int | None = None
    ) -> BlueprintUserGroupsLinkagesResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-all-user-group-ids-for-a-blueprint"""
        params = {"limit": limit} if limit is not None else None
        data = await self._request(
            "GET", f"/v1/blueprints/{id}/relationships/userGroups", params=params
        )
        return BlueprintUserGroupsLinkagesResponse.model_validate(data)

    async def add_user_groups_to_blueprint(
        self, id: str, user_group_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/add-user-groups-to-a-blueprint"""
        await self._linkages_modify(
            "POST",
            f"/v1/blueprints/{id}/relationships/userGroups",
            user_group_ids,
            "userGroups",
        )

    async def remove_user_groups_from_blueprint(
        self, id: str, user_group_ids: list[str]
    ) -> None:
        """https://developer.apple.com/documentation/applebusinessapi/remove-user-groups-from-a-blueprint"""
        await self._linkages_modify(
            "DELETE",
            f"/v1/blueprints/{id}/relationships/userGroups",
            user_group_ids,
            "userGroups",
        )

    async def get_audit_events(
        self,
        start_timestamp: str,
        end_timestamp: str,
        actor_ids: list[str] | None = None,
        subject_ids: list[str] | None = None,
        types: list[str] | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AuditEventsResponse:
        """https://developer.apple.com/documentation/applebusinessapi/get-audit-events"""
        params: dict = {
            "filter[startTimestamp]": start_timestamp,
            "filter[endTimestamp]": end_timestamp,
        }
        if actor_ids:
            params["filter[actorId]"] = ",".join(actor_ids)
        if subject_ids:
            params["filter[subjectId]"] = ",".join(subject_ids)
        if types:
            params["filter[type]"] = ",".join(types)
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        data = await self._request("GET", "/v1/auditEvents", params=params)
        return AuditEventsResponse.model_validate(data)
