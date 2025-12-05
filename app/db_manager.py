"""
FILE: app/database_manager.py
DESCRIPTION: 
    The core engine for SQL interactions.
    - STATIC Tables (Roles, Courses): Read-only helpers.
    - DYNAMIC Tables (Students, Surveys, etc.): Full CRUD support.
"""
import sqlite3
import os
from datetime import date
try:
    from .models import User, Student, Course, Assessment, Submission, WellbeingResponse
except ImportError:
    from models import User, Student, Course, Assessment, Submission, WellbeingResponse

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # 自动定位到 data/university.db
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(base_dir, 'data', 'university.db')
        else:
            self.db_path = db_path

    def get_connection(self):
        """Standard connection helper with Row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row # Allows row['column_name']
        conn.execute("PRAGMA foreign_keys = ON") # Vital for data integrity
        return conn

    # =====================================================
    # 1. AUTHENTICATION (登录模块)
    # =====================================================
    
    def verify_login(self, username, password):
        """
        Check credentials. Returns a User object if valid, else None.
        """
        conn = self.get_connection()
        # Join with Roles to get the role name immediately
        sql = """
            SELECT u.id, u.username, u.role_id, r.name as role_name 
            FROM Users u
            JOIN Roles r ON u.role_id = r.id
            WHERE u.username = ? AND u.password = ?
        """
        row = conn.execute(sql, (username, password)).fetchone()
        conn.close()
        
        if row:
            return User(row['id'], row['username'], row['role_id'], row['role_name'])
        return None

    # =====================================================
    # 2. STATIC DATA HELPERS (用于前端下拉菜单)
    # =====================================================

    def get_all_courses(self):
        """
        READ-ONLY: Get list of all courses.
        Frontend uses this for the 'Select Course' dropdown.
        """
        conn = self.get_connection()
        rows = conn.execute("SELECT * FROM Courses").fetchall()
        conn.close()
        return [Course(row['id'], row['name']) for row in rows]

    # =====================================================
    # 3. STUDENT MANAGEMENT (CRUD: 增删改查)
    # =====================================================

    def get_all_students(self, include_inactive: bool = False):
        """READ: 列出学生（默认仅 Active）。"""
        conn = self.get_connection()
        if include_inactive:
            rows = conn.execute("SELECT * FROM Students").fetchall()
        else:
            rows = conn.execute("SELECT * FROM Students WHERE status = 'Active'").fetchall()
        conn.close()
        return [Student(row['id'], row['graduation_date'], row['status']) for row in rows]

    def get_student(self, student_id):
        """READ: 根据 ID 获取单个学生。"""
        conn = self.get_connection()
        row = conn.execute("SELECT * FROM Students WHERE id = ?", (student_id,)).fetchone()
        conn.close()
        if not row:
            return None
        return Student(row['id'], row['graduation_date'], row['status'])

    def get_courses_by_student(self, student_id):
        """READ: 获取某学生所选课程列表。返回 [Course]。"""
        conn = self.get_connection()
        sql = """
            SELECT c.id, c.name
            FROM Courses c
            JOIN Enrollment e ON c.id = e.course_id
            WHERE e.student_id = ?
            ORDER BY c.id
        """
        rows = conn.execute(sql, (student_id,)).fetchall()
        conn.close()
        return [Course(row['id'], row['name']) for row in rows]
    
    def get_students_by_course(self, course_id):
        """
        READ: 获取某课程下的学生（Active）。
        """
        conn = self.get_connection()
        sql = """
            SELECT s.id, s.graduation_date, s.status 
            FROM Students s
            JOIN Enrollment e ON s.id = e.student_id
            WHERE e.course_id = ? AND s.status = 'Active'
        """
        rows = conn.execute(sql, (course_id,)).fetchall()
        conn.close()
        return [Student(row['id'], row['graduation_date'], row['status']) for row in rows]

    def add_student(self, student_id, course_id, graduation_date):
        """
        CREATE: 新建学生并选课。
        1) 插入 Students（如果已存在则忽略）
        2) 插入 Enrollment（建立关联）
        """
        conn = self.get_connection()
        try:
            sql_student = "INSERT OR IGNORE INTO Students (id, graduation_date, status) VALUES (?, ?, 'Active')"
            conn.execute(sql_student, (student_id, graduation_date))
            sql_enroll = "INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)"
            conn.execute(sql_enroll, (student_id, course_id))
            conn.commit()
            return True, "Success: Student enrolled."
        except sqlite3.IntegrityError as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    def enroll_student(self, student_id, course_id):
        """CREATE: 仅添加选课关联。"""
        conn = self.get_connection()
        try:
            conn.execute("INSERT INTO Enrollment (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
            conn.commit()
            return True, "Enrolled."
        except sqlite3.IntegrityError as e:
            return False, f"Error: {e}"
        finally:
            conn.close()

    def remove_enrollment(self, student_id, course_id):
        """DELETE: 取消某学生对某课程的选课。"""
        conn = self.get_connection()
        conn.execute("DELETE FROM Enrollment WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        conn.commit()
        conn.close()
        return True, "Enrollment removed."

    def update_student_status(self, student_id, new_status):
        """UPDATE: 修改学生状态。"""
        conn = self.get_connection()
        conn.execute("UPDATE Students SET status = ? WHERE id = ?", (new_status, student_id))
        conn.commit()
        conn.close()
        return True, "Status updated."

    def update_student_graduation(self, student_id, graduation_date):
        """UPDATE: 修改学生毕业日期。"""
        conn = self.get_connection()
        conn.execute("UPDATE Students SET graduation_date = ? WHERE id = ?", (graduation_date, student_id))
        conn.commit()
        conn.close()
        return True, "Graduation date updated."

    def delete_student(self, student_id):
        """
        DELETE: 级联删除学生相关记录（手动级联），以避免外键约束报错。
        依次删除：
          - Submissions（成绩）
          - Attendance（出勤）
          - Wellbeing_Surveys（健康问卷回答）
          - Enrollment（选课关联）
          - Students（学生本体）
        """
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM Submissions WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM Attendance WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM Wellbeing_Surveys WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM Enrollment WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM Students WHERE id = ?", (student_id,))
            conn.commit()
            return True, "Student and related records deleted."
        except sqlite3.IntegrityError as e:
            return False, f"Cannot delete due to FK constraints: {e}"
        finally:
            conn.close()
        
        

    # =====================================================
    # 4. ACADEMIC OPERATIONS (Dynamic Data)
    # =====================================================

    def add_assessment(self, title, course_id, deadline, max_score=100):
        """CREATE: Course Director adds a new assignment."""
        conn = self.get_connection()
        sql = "INSERT INTO Assessments (title, course_id, deadline, max_score) VALUES (?, ?, ?, ?)"
        conn.execute(sql, (title, course_id, deadline, max_score))
        conn.commit()
        conn.close()

    def get_assessment(self, assessment_id):
        """READ: 根据ID获取作业。返回 Assessment 或 None。"""
        conn = self.get_connection()
        row = conn.execute("SELECT * FROM Assessments WHERE id = ?", (assessment_id,)).fetchone()
        conn.close()
        if not row:
            return None
        return Assessment(row['id'], row['title'], row['course_id'], row['deadline'], row['max_score'])

    def get_assessments_by_course(self, course_id, start_deadline=None, end_deadline=None):
        """READ: 按课程与可选截止日期范围查询作业列表。返回 List[Assessment]."""
        conn = self.get_connection()
        sql = "SELECT * FROM Assessments WHERE course_id = ?"
        params = [course_id]
        if start_deadline:
            sql += " AND deadline >= ?"
            params.append(start_deadline)
        if end_deadline:
            sql += " AND deadline <= ?"
            params.append(end_deadline)
        sql += " ORDER BY deadline ASC, id ASC"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [Assessment(row['id'], row['title'], row['course_id'], row['deadline'], row['max_score']) for row in rows]

    def record_submission(self, assessment_id, student_id, date, score):
        """CREATE/UPDATE: Record a grade."""
        conn = self.get_connection()
        sql = """
            INSERT OR REPLACE INTO Submissions (assessment_id, student_id, submission_date, score)
            VALUES (?, ?, ?, ?)
        """
        conn.execute(sql, (assessment_id, student_id, date, score))
        conn.commit()
        conn.close()

    def upsert_submission(self, assessment_id, student_id, submission_date, score):
        """封装提交/更新成绩。"""
        self.record_submission(assessment_id, student_id, submission_date, score)
        return True

    def get_submissions_by_assessment(self, assessment_id):
        """READ: 获取某作业的全部提交。返回 List[dict]."""
        conn = self.get_connection()
        sql = """
            SELECT s.student_id, s.submission_date, s.score
            FROM Submissions s
            WHERE s.assessment_id = ?
            ORDER BY s.student_id
        """
        rows = conn.execute(sql, (assessment_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_submissions_by_course(self, course_id, start_date=None, end_date=None):
        """READ: 通过 Submissions JOIN Assessments 精确拿到课程下的提交。返回 List[dict]."""
        conn = self.get_connection()
        sql = """
            SELECT s.student_id, s.assessment_id, a.course_id, s.submission_date, s.score
            FROM Submissions s
            JOIN Assessments a ON s.assessment_id = a.id
            WHERE a.course_id = ?
        """
        params = [course_id]
        if start_date:
            sql += " AND s.submission_date >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND s.submission_date <= ?"
            params.append(end_date)
        sql += " ORDER BY s.submission_date ASC"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def log_attendance(self, student_id, course_id, date, status):
        """CREATE: Log weekly attendance."""
        try:
            conn = self.get_connection()
            sql = "INSERT INTO Attendance (student_id, course_id, lecture_date, status) VALUES (?, ?, ?, ?)"
            conn.execute(sql, (student_id, course_id, date, status))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False # Duplicate entry for same day

    def upsert_attendance(self, student_id, course_id, lecture_date, status):
        """INSERT 或 UPDATE 出勤记录。"""
        conn = self.get_connection()
        cur = conn.cursor()
        # 先尝试更新
        cur.execute(
            "UPDATE Attendance SET status = ? WHERE student_id = ? AND course_id = ? AND lecture_date = ?",
            (status, student_id, course_id, lecture_date),
        )
        if cur.rowcount == 0:
            # 不存在则插入
            cur.execute(
                "INSERT INTO Attendance (student_id, course_id, lecture_date, status) VALUES (?, ?, ?, ?)",
                (student_id, course_id, lecture_date, status),
            )
        conn.commit()
        conn.close()
        return True

    def get_attendance_by_course_and_date(self, course_id, lecture_date):
        """READ: 获取某课程在某日期的出勤记录。返回 {student_id: status}."""
        conn = self.get_connection()
        rows = conn.execute(
            "SELECT student_id, status FROM Attendance WHERE course_id = ? AND lecture_date = ?",
            (course_id, lecture_date),
        ).fetchall()
        conn.close()
        return {row['student_id']: row['status'] for row in rows}

    def get_attendance_range(self, course_id, start_date, end_date):
        """READ: 获取课程在时间范围内的出勤。返回 List[dict]."""
        conn = self.get_connection()
        rows = conn.execute(
            """
            SELECT student_id, course_id, lecture_date, status
            FROM Attendance 
            WHERE course_id = ? AND lecture_date BETWEEN ? AND ?
            ORDER BY lecture_date ASC
            """,
            (course_id, start_date, end_date),
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # =====================================================
    # 5. WELLBEING OPERATIONS (Complex Logic)
    # =====================================================

    def log_survey_response(self, student_id, stress_level, sleep_hours, passed_date: str = None):
        """
        CREATE: Handles the 'Double Insert' logic for surveys.
        - 支持管理员手动指定提交日期 passed_date (YYYY-MM-DD)，不传则使用今天日期。
        """
        survey_date = (passed_date or date.today().isoformat())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 1. 查找/创建 指定日期 的 Survey 定义
            cursor.execute("SELECT id FROM Surveys WHERE passed_date = ?", (survey_date,))
            survey_row = cursor.fetchone()
            
            if survey_row:
                survey_id = survey_row['id']
            else:
                cursor.execute("INSERT INTO Surveys (passed_date) VALUES (?)", (survey_date,))
                survey_id = cursor.lastrowid
            
            # 2. 插入该学生在该日期的回答
            sql = """
                INSERT INTO Wellbeing_Surveys (survey_id, student_id, stress_level, sleep_hours)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (survey_id, student_id, stress_level, sleep_hours))
            conn.commit()
            return True, "Survey logged."
        except sqlite3.IntegrityError:
            # 唯一约束 UNIQUE(student_id, survey_id) 触发
            return False, f"You have already submitted a survey for {survey_date}."
        finally:
            conn.close()

    # =====================================================
    # 6. ANALYTICS DATA PROVIDERS (For Team B)
    # =====================================================

    def get_raw_survey_data(self):
        """
        READ: Fetch data for Wellbeing Analytics.
        Returns List[Dict] because this is for Pandas processing.
        """
        conn = self.get_connection()
        sql = """
            SELECT ws.student_id, ws.stress_level, ws.sleep_hours, s.passed_date as date
            FROM Wellbeing_Surveys ws
            JOIN Surveys s ON ws.survey_id = s.id
            ORDER BY s.passed_date DESC
        """
        data = [dict(row) for row in conn.execute(sql).fetchall()]
        conn.close()
        return data

    def get_analytics_data(self):
        """
        READ: Fetch Attendance and Grades for Correlation Analytics.
        Returns two lists of dicts.
        """
        conn = self.get_connection()
        
        att_data = [dict(r) for r in conn.execute("SELECT student_id, status FROM Attendance").fetchall()]
        grade_data = [dict(r) for r in conn.execute("SELECT student_id, score FROM Submissions").fetchall()]
        
        conn.close()
        return att_data, grade_data
