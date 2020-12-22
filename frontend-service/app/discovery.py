import json
from typing import Any, List, Optional
from urllib.request import urlopen


SERVICE_NAME = "frontend-service"


def _get_destination_service_sidecar_proxy_url(destination_name: str) -> str:
    with urlopen("http://localhost:8500/v1/agent/services") as res:
        services = json.loads(res.read())
        sidecar_proxy_name = "{}-sidecar-proxy".format(SERVICE_NAME)
        sidecar_proxy_service = services.get(sidecar_proxy_name, None)

        if not sidecar_proxy_service:
            raise Exception("Service {} not found".format(sidecar_proxy_name))

        upstreams = sidecar_proxy_service["Proxy"]["Upstreams"]

        destination_upstream = next(
            upstream
            for upstream in upstreams
            if upstream["DestinationName"] == destination_name
        )

        return "http://localhost:{}".format(destination_upstream["LocalBindPort"])


def _get_mfa_deployment_name(akey: str) -> Optional[str]:
    with urlopen("http://localhost:8500/v1/catalog/services") as res:
        services = json.loads(res.read())
        mfa_deployment_name = None

        for service_name, tags in services.items():
            is_mfa_deployment = service_name.startswith(
                "backend-service"
            ) and not service_name.endswith("-sidecar-proxy")

            if is_mfa_deployment and akey in tags:
                mfa_deployment_name = service_name
                break

        return mfa_deployment_name


def get_mfa_deployment_url(akey: str) -> Optional[str]:
    mfa_deployment_name = _get_mfa_deployment_name(akey)

    if not mfa_deployment_name:
        return None

    return _get_destination_service_sidecar_proxy_url(mfa_deployment_name)
