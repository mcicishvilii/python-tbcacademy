import uuid

def generate_id():
    return str(uuid.uuid4())[:8]  # Short UUID (8 characters)
