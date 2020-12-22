{
  "service": {
    "name": "backend-service",
    "port": 80,
    "tags": {{ keyOrDefault "backend/akeys" "[]" }},
    "connect": { "sidecar_service": {} }
  }
}
