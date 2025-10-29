import os

FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING":True
}
HTML_SANITIZATION_SCHEMA_EXTENSIONS = {
    "attributes":{
        "*":["style","className"],
    },
    "tagNames":["style"]
}
GUEST_ROLE_NAME = "Public"

ENABLE_CORS = True
OVERRIDE_HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL'}
TALISMAN_ENABLED = False
HTTP_HEADERS={"X-Frame-Options":"ALLOWALL"}

CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "origins": ["http://localhost:5173"],
}

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "my_secret_key")

GUEST_TOKEN_JWT_EXP_SECONDS = 300

# docker exec -u 0 -it smoc2-superset-1 /bin/bash