
import os
import shutil
from pathlib import Path
from openpyxl import load_workbook

# Existing local Excel workbook
file = Path("/Users/Nick/CI:CD/employees.xlsx")

# Parameters entered in Jenkins
name = os.environ.get("EMPLOYEE_NAME", os.environ.get("NAME", "")).strip()
department = os.environ.get("DEPARTMENT", os.environ.get("DEPT", "")).strip()

if not name or not department:
    raise ValueError("Employee name or department parameter is missing")

if not name:
    raise ValueError("Employee name cannot be empty")

# Open the existing Excel file
workbook = load_workbook(file)
sheet = workbook["Employees"]

old_count = sheet.max_row - 1

# Find the next employee ID
ids = [
    row[0]
    for row in sheet.iter_rows(
        min_row=2,
        max_col=1,
        values_only=True
    )
    if type(row[0]) is int
]

new_id = max(ids, default=0) + 1

# Add one employee
sheet.append([new_id, name, department])

# Create a backup before updating
backup = file.with_name(
    f"employees_backup_build_{os.environ['BUILD_NUMBER']}.xlsx"
)

shutil.copy2(file, backup)

# Save the updated workbook
workbook.save(file)
workbook.close()

print("Employee ID:", new_id)
print("Employee Name:", name)
print("Department:", department)
print("Previous records:", old_count)
print("Updated records:", old_count + 1)
print("Excel updated successfully!")
