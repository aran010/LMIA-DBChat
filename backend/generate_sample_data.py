import sqlite3
import os
import fitz  # PyMuPDF

# Paths inside the docker container
UPLOADS_DIR = "/opt/ragapp/uploads/policies"
DB_PATH = "/opt/ragapp/config/sample_hr.db"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# 1. Create SQLite DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    full_name TEXT,
    age INTEGER,
    department TEXT,
    job_role TEXT,
    attrition TEXT,
    monthly_income INTEGER,
    years_at_company INTEGER
)''')

sample_employees = [
    (1001, "Alice Smith", 34, "Sales", "Sales Executive", "No", 5993, 8),
    (1002, "Bob Jones", 41, "Research & Development", "Research Scientist", "No", 5130, 10),
    (1003, "Charlie Brown", 28, "Human Resources", "HR Generalist", "Yes", 2090, 2),
    (1004, "Diana Prince", 45, "Engineering", "Software Engineer", "No", 8500, 15),
    (1005, "Evan Wright", 22, "Sales", "Sales Representative", "Yes", 2800, 1)
]

c.executemany('INSERT OR REPLACE INTO employees VALUES (?,?,?,?,?,?,?,?)', sample_employees)
conn.commit()
conn.close()

print(f"Created SQLite database at {DB_PATH}")

# 2. Create Sample PDF
pdf_path = os.path.join(UPLOADS_DIR, "sample_policy.pdf")
doc = fitz.open()
page = doc.new_page()

text = """ACME CORPORATION - HR POLICIES AND PROCEDURES

1. REMOTE WORK POLICY
Employees in the Engineering and Research & Development departments are eligible for 
up to 3 days of remote work per week. Sales and Human Resources employees must be 
on-site 4 days a week.

2. ANNUAL LEAVE
All full-time employees are entitled to 20 days of paid annual leave per year. 
Unused leave does not roll over to the next year.

3. ATTRITION AND OFFBOARDING
If an employee decides to leave Acme Corporation, a standard 2-week notice period 
is required. All company assets including laptops and security badges must be 
returned to the HR department on the final day.
"""

page.insert_text((50, 50), text, fontsize=12)
doc.save(pdf_path)
print(f"Created sample PDF at {pdf_path}")
