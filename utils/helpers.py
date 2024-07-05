def validate_form(fields):
    for field in fields:
        if not field.get():
            return False
    return True
