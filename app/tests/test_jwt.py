from app.core.security.jwt import verify_password, get_password_hash

def test_password():
    plain_password = "password123"
    hashed_password = get_password_hash(plain_password)

    print("\nPlain Password:", plain_password)
    print("\nHashed Password:", hashed_password)

    # Verify the password
    is_valid = verify_password(plain_password, hashed_password)
    print("\nIs the password valid?", is_valid)
    assert is_valid == True
    
