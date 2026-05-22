# applebusiness

Async Python client for the [Apple Business API](https://developer.apple.com/documentation/applebusinessapi).

## Install

```sh
pip install applebusiness
```

Requires Python 3.14+.

## Authentication

You need an API key generated in Apple Business Manager.
The client uses the OAuth 2.0 client-credentials flow
with a JWT client assertion signed by your private key.
See [Implementing OAuth for the Apple School Manager and Apple Business API](https://developer.apple.com/documentation/apple-school-and-business-manager-api/implementing-oauth-for-the-apple-school-manager-and-apple-business-api).

You'll need:

- `key_id` — the key identifier from Apple Business Manager
- `client_id` — your API account's client ID
- `private_key_pem` — the PEM-encoded EC private key

## Usage

```python
import asyncio
from applebusiness import Client

async def main():
    async with Client(key_id, client_id, private_key_pem) as client:
        devices = await client.get_org_devices()
        for device in devices.data:
            print(device.id, device.attributes.serialNumber)

asyncio.run(main())
```

## Token caching

By default, OAuth tokens are cached in memory on the `Client` instance.
To share tokens across processes (e.g. via Redis),
subclass `Client` and override `_get_cached_token` / `_set_cached_token`:

```python
class RedisClient(Client):
    async def _get_cached_token(self):
        raw = await redis.get("ab-token")
        return json.loads(raw) if raw else None

    async def _set_cached_token(self, token):
        await redis.set("ab-token", json.dumps(token), ex=token["expires_in"])
```

## Coverage

The client implements every Apple Business API endpoint documented as of this release:

- **Devices** — `get_org_devices`, `get_org_device`,
  `get_org_device_apple_care_coverage`, `get_mdm_devices`, `get_mdm_device_details`
- **Device Management Services** — `get_mdm_servers`, `get_mdm_server_device_ids`,
  `get_org_device_assigned_server_id`, `get_org_device_assigned_server`,
  `assign_devices_to_server`, `unassign_devices_from_server`, `get_org_device_activity`
- **Users** — `get_users`, `get_user`
- **User Groups** — `get_user_groups`, `get_user_group`, `get_user_group_user_ids`
- **Apps & Packages** — `get_apps`, `get_app`, `get_packages`, `get_package`
- **Blueprints** — `get_blueprints`, `create_blueprint`, `get_blueprint`,
  `update_blueprint`, `delete_blueprint`, and `get_blueprint_<rel>_ids`
  `add_<rel>_to_blueprint` / `remove_<rel>_from_blueprint` for `apps`,
  `configurations`, `packages`, `org_devices`, `users`, `user_groups`
- **Configurations** — `get_configurations`, `create_configuration`,
  `get_configuration`, `update_configuration`, `delete_configuration`
- **Audit** — `get_audit_events`

All responses are returned as typed Pydantic models
(importable from the top-level `applebusiness` package).

## Activity polling

`assign_devices_to_server` and `unassign_devices_from_server` poll
the resulting `orgDeviceActivity` until it leaves `IN_PROGRESS`.
The polling timeout defaults to 300 seconds and raises `TimeoutError` when exceeded.
To skip polling, pass `wait=False`; to wait indefinitely, pass `timeout=None`.

## Errors

Non-2xx responses raise `applebusiness.ClientError`,
which exposes the HTTP status and parsed `ErrorResponse` body.

## License

MIT
