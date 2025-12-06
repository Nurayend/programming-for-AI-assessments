"""
FILE: test_registration.py
DESCRIPTION: Test script for the registration functionality.
"""
from app.db_manager import DatabaseManager

def test_registration():
    print("=" * 60)
    print("注册功能测试 (Registration Functionality Test)")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Test 1: Valid registration for Wellbeing Officer
    print("\n--- 测试 1: 有效的健康管理员注册 ---")
    success, msg = db.register_user("test_wellbeing_1", "password123", 1)
    print(f"结果: {'成功' if success else '失败'}")
    print(f"消息: {msg}")
    
    # Test 2: Valid registration for Course Director
    print("\n--- 测试 2: 有效的课程主任注册 ---")
    success, msg = db.register_user("test_director_1", "password456", 2)
    print(f"结果: {'成功' if success else '失败'}")
    print(f"消息: {msg}")
    
    # Test 3: Duplicate username
    print("\n--- 测试 3: 重复的用户名 ---")
    success, msg = db.register_user("test_wellbeing_1", "password789", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 4: Username too short
    print("\n--- 测试 4: 用户名过短 ---")
    success, msg = db.register_user("ab", "password123", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 5: Username too long
    print("\n--- 测试 5: 用户名过长 ---")
    long_username = "a" * 51
    success, msg = db.register_user(long_username, "password123", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 6: Password too short
    print("\n--- 测试 6: 密码过短 ---")
    success, msg = db.register_user("test_user_short_pwd", "12345", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 7: Invalid role ID
    print("\n--- 测试 7: 无效的角色 ID ---")
    success, msg = db.register_user("test_user_invalid_role", "password123", 3)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 8: Login with newly registered account
    print("\n--- 测试 8: 使用新注册的账户登陆 ---")
    user = db.verify_login("test_wellbeing_1", "password123")
    if user:
        print(f"登陆成功")
        print(f"用户名: {user.username}")
        print(f"角色: {user.role_name}")
        print(f"角色 ID: {user.role_id}")
    else:
        print(f"登陆失败")
    
    # Test 9: Login with wrong password
    print("\n--- 测试 9: 使用错误的密码登陆 ---")
    user = db.verify_login("test_wellbeing_1", "wrongpassword")
    if user is None:
        print(f"正确拒绝错误的密码")
    else:
        print(f"不应该成功登陆")
    
    # Test 10: Empty username
    print("\n--- 测试 10: 空用户名 ---")
    success, msg = db.register_user("", "password123", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    # Test 11: Empty password
    print("\n--- 测试 11: 空密码 ---")
    success, msg = db.register_user("test_user_empty_pwd", "", 1)
    print(f"结果: {'正确拒绝' if not success else '不应该成功'}")
    print(f"消息: {msg}")
    
    print("\n" + "=" * 60)
    print("测试完成 (Test Complete)")
    print("=" * 60)

if __name__ == "__main__":
    test_registration()

