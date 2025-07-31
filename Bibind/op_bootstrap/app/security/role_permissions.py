ROLE_PERMISSIONS = {
    "user": ["offres:read", "projets:read"],
    "expert": ["offres:create", "infrastructures:create"],
    "admin": ["*"],
    "agent": ["orchestration:trigger", "validation:auto-approve"],
    "backoffice": ["validation:read", "validation:approve"],
}
