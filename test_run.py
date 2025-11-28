"""
FILE: test_run.py
DESCRIPTION: A simple script to manually test if the backend logic is working correctly.
"""
from app.db_manager import DatabaseManager

def main():
    print("🚀 Starting System Test...\n")
    
    # 1. Initialize Database Manager
    db = DatabaseManager()
    
    # ==========================================
    # Test 1: Login Functionality
    # ==========================================
    print("--- 1. Testing Login ---")
    # Test correct credentials (pre-set in schema.sql)
    # Note: The password in schema.sql is 'test123'
    user = db.verify_login("will_b", "test123")
    
    if user:
        print(f" Login Successful! User: {user.username}, Role: {user.role_name}")
        print(f"   (Object Type Check: {type(user)})") # Proves it returns an Object
    else:
        print("Login Failed (Unexpected)")

    # ==========================================
    # Test 2: Get Static Data (Courses)
    # ==========================================
    print("\n--- 2. Testing Get Course List ---")
    courses = db.get_all_courses()
    for c in courses:
        print(f"   Course: {c.name} (ID: {c.id})")
    
    if len(courses) > 0:
        print("Successfully retrieved course list")

    # ==========================================
    # Test 3: Student CRUD (Add Student)
    # ==========================================
    print("\n--- 3. Testing Add Student ---")
    new_id = 99999
    # Attempt to add a new student
    success, msg = db.add_student(new_id, course_id=1, graduation_date='2026-07-01')
    if success:
        print(f"Student added successfully: {msg}")
    else:
        print(f"Add result: {msg} (Normal if ID is duplicate)")

    # Verify if the student exists in the list
    all_students = db.get_all_students()
    found = False
    for s in all_students:
        if s.id == new_id:
            found = True
            break
    
    if found:
        print("Found the newly added student in the database")

    # ==========================================
    # Test 4: Log Survey (Survey Logic)
    # ==========================================
    print("\n--- 4. Testing Log Survey ---")
    # Log stress level for the new student
    # Logic will automatically check if a Survey exists for today, create one if not
    success, msg = db.log_survey_response(student_id=new_id, stress_level=4, sleep_hours=6.5)
    print(f"   Log Result: {success} - {msg}")

    # ==========================================
    # Test 5: Analytics Data Fetch (For Team B)
    # ==========================================
    print("\n--- 5. Testing Analytics Data Fetch (For Team B) ---")
    
    # Test raw survey data
    raw_survey = db.get_raw_survey_data()
    print(f"   [Wellbeing] Retrieved {len(raw_survey)} survey records")
    if len(raw_survey) > 0:
        print(f"   Sample Data: {raw_survey[0]}")

    # Test attendance vs grade data
    att_data, grade_data = db.get_analytics_data()
    print(f"   [Course Director] Retrieved {len(att_data)} attendance records")
    print(f"   [Course Director] Retrieved {len(grade_data)} submission records")
    
    print("\n🎉 Test Complete! If no errors appeared, backend logic is working.")

if __name__ == "__main__":
    main()