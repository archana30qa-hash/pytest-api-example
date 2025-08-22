pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}
#Added Order schema for validation
order = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "id": {
            "type": "string"
        },
        "pet_id": {
            "type": "integer"
        },
        "message": {
            "type": "string"
        }
    }
}
