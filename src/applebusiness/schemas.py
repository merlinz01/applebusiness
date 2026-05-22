from datetime import datetime
from typing import Literal

from pydantic import BaseModel

__all__ = [
    "App",
    "AppAttributes",
    "AppResponse",
    "AppsResponse",
    "AppleCareCoverage",
    "AppleCareCoverageAttributes",
    "AppleCareCoverageResponse",
    "AuditEvent",
    "AuditEventCommonAttributes",
    "AuditEventsResponse",
    "Blueprint",
    "BlueprintAppsLinkagesRequest",
    "BlueprintAppsLinkagesResponse",
    "BlueprintAttributes",
    "BlueprintConfigurationsLinkagesRequest",
    "BlueprintConfigurationsLinkagesResponse",
    "BlueprintOrgDevicesLinkagesRequest",
    "BlueprintOrgDevicesLinkagesResponse",
    "BlueprintPackagesLinkagesRequest",
    "BlueprintPackagesLinkagesResponse",
    "BlueprintRelationships",
    "BlueprintRelationshipsApps",
    "BlueprintRelationshipsAppsData",
    "BlueprintRelationshipsConfigurations",
    "BlueprintRelationshipsConfigurationsData",
    "BlueprintRelationshipsOrgDevices",
    "BlueprintRelationshipsOrgDevicesData",
    "BlueprintRelationshipsPackages",
    "BlueprintRelationshipsPackagesData",
    "BlueprintRelationshipsUsers",
    "BlueprintRelationshipsUsersData",
    "BlueprintRelationshipsUserGroups",
    "BlueprintRelationshipsUserGroupsData",
    "BlueprintResponse",
    "BlueprintUserGroupsLinkagesRequest",
    "BlueprintUserGroupsLinkagesResponse",
    "BlueprintUsersLinkagesRequest",
    "BlueprintUsersLinkagesResponse",
    "BlueprintsResponse",
    "Configuration",
    "ConfigurationCommon",
    "ConfigurationCustomSetting",
    "ConfigurationResponse",
    "ConfigurationsResponse",
    "CustomSettingsValues",
    "DocumentLinks",
    "MdmDevice",
    "MdmDeviceAttributes",
    "MdmDeviceDetail",
    "MdmDeviceDetailAttributes",
    "MdmDeviceDetailResponse",
    "MdmDeviceRelationships",
    "MdmDeviceRelationshipsDetails",
    "MdmDeviceResponse",
    "MdmDevicesResponse",
    "MdmServer",
    "MdmServerAttributes",
    "MdmServerDevicesLinkagesResponse",
    "MdmServerRelationships",
    "MdmServerRelationshipsDevices",
    "MdmServerRelationshipsDevicesData",
    "MdmServerResponse",
    "MdmServersResponse",
    "OrgDevice",
    "OrgDeviceActivity",
    "OrgDeviceActivityAttributes",
    "OrgDeviceActivityResponse",
    "OrgDeviceAssignedServerLinkage",
    "OrgDeviceAssignedServerLinkageResponse",
    "OrgDeviceAttributes",
    "OrgDeviceRelationships",
    "OrgDeviceResponse",
    "OrgDevicesResponse",
    "PagedDocumentLinks",
    "PagingInformation",
    "PagingInformationPaging",
    "Package",
    "PackageAttributes",
    "PackageResponse",
    "PackagesResponse",
    "Relationship",
    "RelationshipLinks",
    "ResourceLinkage",
    "ResourceLinks",
    "User",
    "UserAttributes",
    "UserGroup",
    "UserGroupAttributes",
    "UserGroupResponse",
    "UserGroupUsersLinkagesResponse",
    "UserGroupsResponse",
    "UserPhoneNumber",
    "UserResponse",
    "UserRoleOuMapping",
    "UsersResponse",
]


class PagedDocumentLinks(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/pageddocumentlinks"""

    first: str | None = None
    next: str | None = None
    self: str


class PagingInformation(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/paginginformation"""

    paging: PagingInformationPaging


class PagingInformationPaging(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/paginginformation/paging-data.dictionary"""

    limit: int
    total: int | None = None
    nextCursor: str | None = None


class ResourceLinks(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/resourcelinks"""

    self: str


"""https://developer.apple.com/documentation/applebusinessapi/documentlinks"""
DocumentLinks = ResourceLinks


class Relationship(BaseModel):
    """E.g. https://developer.apple.com/documentation/applebusinessapi/orgdevice/relationships-data.dictionary/assignedserver-data.dictionary"""

    related: ResourceLinks | None = None


class RelationshipLinks(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/relationshiplinks"""

    include: str | None = None
    related: str | None = None
    self: str | None = None


class OrgDevicesResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdevicesresponse"""

    data: list[OrgDevice]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class OrgDevice(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdevice"""

    attributes: OrgDeviceAttributes
    id: str
    links: ResourceLinks
    relationships: OrgDeviceRelationships
    type: Literal["orgDevices"]


class OrgDeviceAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdevice/attributes-data.dictionary"""

    addedToOrgDateTime: datetime
    releasedFromOrgDateTime: datetime | None = None
    color: str
    deviceCapacity: str
    deviceModel: str
    eid: str | None = None
    imei: list[str] | None = None
    meid: list[str] | None = None
    wifiMacAddress: str
    bluetoothMacAddress: str
    ethernetMacAddress: list[str]
    orderDateTime: datetime
    orderNumber: str
    partNumber: str
    productFamily: str
    productType: str
    purchaseSourceType: str
    purchaseSourceId: str
    serialNumber: str
    status: str
    updatedDateTime: datetime
    releaserEntityType: str | None = None
    releaserId: str | None = None


class OrgDeviceRelationships(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdevice/relationships-data.dictionary"""

    assignedServer: Relationship | None = None
    appleCareCoverage: Relationship | None = None


class OrgDeviceResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceresponse"""

    data: OrgDevice
    links: ResourceLinks


class MdmDevicesResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevicesresponse"""

    data: list[MdmDevice]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class MdmDevice(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevice"""

    attributes: MdmDeviceAttributes
    id: str
    links: ResourceLinks | None = None
    relationships: MdmDeviceRelationships
    type: Literal["mdmDevices"]


class MdmDeviceAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevice/attributes-data.dictionary"""

    deviceName: str
    enrolledUserId: str | None = None
    productFamily: str
    serialNumber: str


class MdmDeviceRelationships(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevice/relationships-data.dictionary"""

    details: MdmDeviceRelationshipsDetails


class MdmDeviceRelationshipsDetails(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevice/relationships-data.dictionary/details-data.dictionary"""

    links: RelationshipLinks


class MdmDeviceDetailResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevicedetailresponse"""

    data: MdmDeviceDetail
    links: ResourceLinks


class MdmDeviceDetail(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevicedetail"""

    attributes: MdmDeviceDetailAttributes
    id: str
    links: ResourceLinks | None = None
    type: Literal["mdmDeviceDetails"]


class MdmDeviceDetailAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdevicedetail/attributes-data.dictionary"""

    bluetoothMacAddress: str
    deviceEraseStatus: str
    deviceLockStatus: str
    deviceModel: str
    deviceName: str
    ethernetMacAddress: str
    imei: list[str]
    isFileVaultEnabled: bool
    isFirewallEnabled: bool
    lastCheckInDateTime: datetime
    lostModeStatus: str
    meid: list[str] | None = None
    osVersion: str
    platform: str
    serialNumber: str
    storageFreeCapacity: int
    storageTotalCapacity: int
    wifiMacAddress: str


class MdmServersResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserversresponse"""

    data: list[MdmServer]
    included: list[OrgDevice] | None = None
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class OrgDeviceAssignedServerLinkageResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceassignedserverlinkageresponse"""

    data: OrgDeviceAssignedServerLinkage
    links: DocumentLinks


class OrgDeviceAssignedServerLinkage(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceassignedserverlinkageresponse/data-data.dictionary"""

    id: str
    type: Literal["mdmServers"]


class MdmServerResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserverresponse"""

    data: MdmServer
    included: list[OrgDevice] | None = None
    links: DocumentLinks


class MdmServer(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserver"""

    attributes: MdmServerAttributes
    id: str
    relationships: MdmServerRelationships
    type: Literal["mdmServers"]


class MdmServerAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserver/attributes-data.dictionary"""

    createdDateTime: datetime
    serverName: str
    serverType: str
    updatedDateTime: datetime


class MdmServerRelationships(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserver/relationships-data.dictionary"""

    devices: MdmServerRelationshipsDevices


class MdmServerRelationshipsDevices(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserver/relationships-data.dictionary/devices-data.dictionary"""

    data: list[MdmServerRelationshipsDevicesData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class MdmServerRelationshipsDevicesData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserver/relationships-data.dictionary/devices-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["orgDevices"]


class OrgDeviceActivityResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceactivityresponse"""

    data: OrgDeviceActivity
    links: DocumentLinks


class OrgDeviceActivity(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceactivity"""

    attributes: OrgDeviceActivityAttributes
    id: str
    links: ResourceLinks
    type: Literal["orgDeviceActivities"]


class OrgDeviceActivityAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/orgdeviceactivity/attributes-data.dictionary"""

    createdDateTime: datetime | None = None
    status: str | None = None
    subStatus: str | None = None
    completedDateTime: datetime | None = None
    downloadUrl: str | None = None


class BlueprintsResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintsresponse"""

    data: list[Blueprint]
    # included: list[App | Package | Configuration | OrgDevice | User | UserGroup] | None = None
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class Blueprint(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint"""

    attributes: BlueprintAttributes
    id: str
    links: ResourceLinks
    relationships: BlueprintRelationships
    type: Literal["blueprints"]


class BlueprintAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/attributes-data.dictionary"""

    name: str
    description: str
    status: str
    appLicenseDeficient: bool
    createdDateTime: datetime
    updatedDateTime: datetime


class BlueprintRelationships(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary"""

    apps: BlueprintRelationshipsApps
    configurations: BlueprintRelationshipsConfigurations
    orgDevices: BlueprintRelationshipsOrgDevices | None = None
    packages: BlueprintRelationshipsPackages
    users: BlueprintRelationshipsUsers
    userGroups: BlueprintRelationshipsUserGroups


class BlueprintRelationshipsApps(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/apps-data.dictionary"""

    data: list[BlueprintRelationshipsAppsData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsAppsData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/apps-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["apps"]


class BlueprintRelationshipsConfigurations(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/configurations-data.dictionary"""

    data: list[BlueprintRelationshipsConfigurationsData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsConfigurationsData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/configurations-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["configurations"]


class BlueprintRelationshipsOrgDevices(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/devices-data.dictionary"""

    data: list[BlueprintRelationshipsOrgDevicesData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsOrgDevicesData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/devices-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["orgDevices"]


class BlueprintRelationshipsPackages(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/packages-data.dictionary"""

    data: list[BlueprintRelationshipsPackagesData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsPackagesData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/packages-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["packages"]


class BlueprintRelationshipsUsers(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/users-data.dictionary"""

    data: list[BlueprintRelationshipsUsersData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsUsersData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/users-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["users"]


class BlueprintRelationshipsUserGroups(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/usergroups-data.dictionary"""

    data: list[BlueprintRelationshipsUserGroupsData] | None = None
    links: RelationshipLinks
    meta: PagingInformation | None = None


class BlueprintRelationshipsUserGroupsData(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprint/relationships-data.dictionary/usergroups-data.dictionary/data-data.dictionary"""

    id: str
    type: Literal["userGroups"]


class BlueprintResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintresponse"""

    data: Blueprint
    # included: list[App | Package | Configuration | OrgDevice | User | UserGroup] | None = None
    links: DocumentLinks


class ConfigurationsResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/configurationsresponse"""

    data: list[Configuration]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class Configuration(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/configuration"""

    attributes: ConfigurationCustomSetting
    id: str
    links: ResourceLinks
    relationships: ConfigurationCustomSetting | None = None
    type: Literal["configurations"]


class ConfigurationCommon(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/configurationcommon"""

    configuredForPlatforms: list[str]
    createdDateTime: datetime
    name: str
    type: str
    updatedDateTime: datetime


class ConfigurationCustomSetting(ConfigurationCommon):
    """https://developer.apple.com/documentation/applebusinessapi/configurationcustomsetting"""

    customSettingsValues: CustomSettingsValues | None = None


class CustomSettingsValues(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/customsettingsvalues"""

    configurationProfile: str  # byte array, possibly Base64-encoded
    filename: str


class ConfigurationResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/configurationresponse"""

    data: Configuration
    links: DocumentLinks


class ResourceLinkage(BaseModel):
    """Generic JSON:API resource identifier object: `{id, type}`."""

    id: str
    type: str


class MdmDeviceResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmdeviceresponse"""

    data: MdmDevice
    links: DocumentLinks


class MdmServerDevicesLinkagesResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/mdmserverdeviceslinkagesresponse"""

    data: list[ResourceLinkage]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class AppleCareCoverage(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/applecarecoverage"""

    id: str
    type: Literal["appleCareCoverage"]
    attributes: AppleCareCoverageAttributes | None = None
    links: ResourceLinks | None = None


class AppleCareCoverageAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/applecarecoverage/attributes-data.dictionary"""

    status: str | None = None
    paymentType: str | None = None
    description: str | None = None
    startDateTime: datetime | None = None
    endDateTime: datetime | None = None
    isRenewable: bool | None = None
    isCanceled: bool | None = None
    contractCancelDateTime: datetime | None = None
    agreementNumber: str | None = None


class AppleCareCoverageResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/applecarecoverageresponse"""

    data: list[AppleCareCoverage]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class UserPhoneNumber(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/userphonenumber"""

    phoneNumber: str | None = None
    type: str | None = None


class UserRoleOuMapping(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/userroleoumapping"""

    roleName: str | None = None
    ouId: str | None = None


class UserAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/user/attributes-data.dictionary"""

    firstName: str | None = None
    middleName: str | None = None
    lastName: str | None = None
    status: str | None = None
    managedAppleAccount: str | None = None
    isExternalUser: bool | None = None
    roleOuList: list[UserRoleOuMapping] | None = None
    email: str | None = None
    employeeNumber: str | None = None
    costCenter: str | None = None
    division: str | None = None
    department: str | None = None
    jobTitle: str | None = None
    phoneNumbers: list[UserPhoneNumber] | None = None
    startDateTime: datetime | None = None
    createdDateTime: datetime | None = None
    updatedDateTime: datetime | None = None


class User(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/user"""

    id: str
    type: Literal["users"]
    attributes: UserAttributes | None = None
    links: ResourceLinks | None = None


class UserResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/userresponse"""

    data: User
    links: DocumentLinks


class UsersResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usersresponse"""

    data: list[User]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class UserGroupAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usergroup/attributes-data.dictionary"""

    ouId: str | None = None
    name: str | None = None
    type: str | None = None
    totalMemberCount: int | None = None
    status: str | None = None
    createdDateTime: datetime | None = None
    updatedDateTime: datetime | None = None


class UserGroup(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usergroup"""

    id: str
    type: Literal["userGroups"]
    attributes: UserGroupAttributes | None = None
    links: ResourceLinks | None = None


class UserGroupResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usergroupresponse"""

    data: UserGroup
    links: DocumentLinks


class UserGroupsResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usergroupsresponse"""

    data: list[UserGroup]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class UserGroupUsersLinkagesResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/usergroupuserslinkagesresponse"""

    data: list[ResourceLinkage]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class AppAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/app/attributes-data.dictionary"""

    name: str | None = None
    bundleId: str | None = None
    websiteUrl: str | None = None
    version: str | None = None
    supportedOS: list[str] | None = None
    isCustomApp: bool | None = None
    appStoreUrl: str | None = None


class App(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/app"""

    id: str
    type: Literal["apps"]
    attributes: AppAttributes | None = None
    links: ResourceLinks | None = None


class AppResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/appresponse"""

    data: App
    links: DocumentLinks


class AppsResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/appsresponse"""

    data: list[App]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class PackageAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/package/attributes-data.dictionary"""

    name: str | None = None
    url: str | None = None
    hash: str | None = None
    bundleIds: list[str] | None = None
    description: str | None = None
    version: str | None = None
    createdDateTime: datetime | None = None
    updatedDateTime: datetime | None = None


class Package(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/package"""

    id: str
    type: Literal["packages"]
    attributes: PackageAttributes | None = None
    links: ResourceLinks | None = None


class PackageResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/packageresponse"""

    data: Package
    links: DocumentLinks


class PackagesResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/packagesresponse"""

    data: list[Package]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class _LinkagesRequest(BaseModel):
    data: list[ResourceLinkage]


class _LinkagesResponse(BaseModel):
    data: list[ResourceLinkage]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None


class BlueprintAppsLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintappslinkagesrequest"""


class BlueprintAppsLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintappslinkagesresponse"""


class BlueprintConfigurationsLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintconfigurationslinkagesrequest"""


class BlueprintConfigurationsLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintconfigurationslinkagesresponse"""


class BlueprintPackagesLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintpackageslinkagesrequest"""


class BlueprintPackagesLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintpackageslinkagesresponse"""


class BlueprintOrgDevicesLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintorgdeviceslinkagesrequest"""


class BlueprintOrgDevicesLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintorgdeviceslinkagesresponse"""


class BlueprintUsersLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintuserslinkagesrequest"""


class BlueprintUsersLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintuserslinkagesresponse"""


class BlueprintUserGroupsLinkagesRequest(_LinkagesRequest):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintusergroupslinkagesrequest"""


class BlueprintUserGroupsLinkagesResponse(_LinkagesResponse):
    """https://developer.apple.com/documentation/applebusinessapi/blueprintusergroupslinkagesresponse"""


class AuditEventCommonAttributes(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/auditeventcommonattributes"""

    eventDateTime: datetime | None = None
    type: str
    category: str | None = None
    actorType: str | None = None
    actorId: str | None = None
    actorName: str | None = None
    subjectType: str | None = None
    subjectId: str | None = None
    subjectName: str | None = None
    outcome: str | None = None
    groupId: str | None = None
    eventDataPropertyKey: str | None = None


class AuditEvent(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/auditevent"""

    id: str
    type: str
    attributes: dict | None = None
    links: ResourceLinks | None = None


class AuditEventsResponse(BaseModel):
    """https://developer.apple.com/documentation/applebusinessapi/auditeventsresponse"""

    data: list[AuditEvent]
    links: PagedDocumentLinks
    meta: PagingInformation | None = None
