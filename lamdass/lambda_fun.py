def lambda_handler(event, context):
    name=event.get("name", "Unknown")
    return f"Hello {name}"
