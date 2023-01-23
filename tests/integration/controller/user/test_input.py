def generate_invalid_create_user_inputs():
    return [
        {"surname": "test", "email": "test@test.com", "balance": 1234},
        {"name": "test", "email": "test@test.com", "balance": 1234},
        {"name": "test", "surname": "test", "balance": 1234},
        {"name": None, "surname": "test", "email": "test@test.com", "balance": 1234},
        {"name": "test", "surname": None, "email": "test@test.com", "balance": 1234},
        {"name": "test", "surname": "test", "email": None, "balance": 1234},
        {
            "name": "test",
            "surname": "test",
            "email": "test@test.com",
            "balance": "test",
        },
    ]
