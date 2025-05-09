import pytest
from file_storage_api.app.utils import hash_password, check_hash_password

def test_hash_password():
    """Test password hashing functionality"""
    test_cases = [
        ("password123", "user1"),
        ("", "user2"),
        ("complex!@#$%^&*()", "user3"),
        ("password123", "user1")  
    ]
    
    for password, username in test_cases:
        hash1 = hash_password(password, username)
        hash2 = hash_password(password, username)
        assert hash1 == hash2, "Hash should be consistent for same input"
        
        if username != "user1":
            assert hash1 != hash_password(password, "user1"), "Hash should be different for different usernames"
            assert hash1 != hash_password("different_password", username), "Hash should be different for different passwords"

def test_check_hash_password():
    password = "test_password"
    username = "test_user"
    hashed = hash_password(password, username)
    assert check_hash_password(password, username, hashed), "Correct password should verify successfully"
    
    assert not check_hash_password("wrong_password", username, hashed), "Incorrect password should fail verification"
    
    assert not check_hash_password(password, "wrong_username", hashed), "Incorrect username should fail verification"
    
    empty_hash = hash_password("", "")
    assert check_hash_password("", "", empty_hash), "Empty password should verify successfully"
    
    special_password = "!@#$%^&*()_+"
    special_hash = hash_password(special_password, username)
    assert check_hash_password(special_password, username, special_hash), "Special characters should verify successfully" 