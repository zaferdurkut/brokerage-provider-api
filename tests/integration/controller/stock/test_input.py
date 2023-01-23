def generate_invalid_create_stock_inputs():
    return [
        {"symbol": "AAPL", "first_price": 123.33, "currency": "USD", "amount": 100},
        {"name": "Apple", "first_price": 123.33, "currency": "USD", "amount": 100},
        {"name": "Apple", "symbol": "AAPL", "currency": "USD", "amount": 100},
        {"name": "Apple", "symbol": "AAPL", "first_price": 123.33, "amount": 100},
        {"name": "Apple", "symbol": "AAPL", "first_price": 123.33, "currency": "USD"},
        {
            "name": "Apple",
            "symbol": "AAPL",
            "first_price": "test",
            "currency": "USD",
            "amount": 100,
        },
        {
            "name": "Apple",
            "symbol": "AAPL",
            "first_price": 123.33,
            "currency": "USD",
            "amount": "test",
        },
    ]
