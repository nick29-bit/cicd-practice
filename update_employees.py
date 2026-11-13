
from openpyxl import load_workbook

# Step 1: Read existing Excel file
workbook = load_workbook("employees.xlsx")
sheet = workbook["Employees"]

# Step 2: Check original record count
original_count = sheet.max_row - 1

if original_count != 100:
    raise ValueError("Expected 100 original records")

print(f"Original records: {original_count}")

# Step 3: Add 10 new records
for i in range(101, 111):
    sheet.append([
        i,
        f"Employee_{i}",
        "IT"
    ])

# Step 4: Save updated Excel file
workbook.save("employees_updated.xlsx")

# Step 5: Validate record count
updated_count = sheet.max_row - 1

assert updated_count == 110, "Record count mismatch"

print(f"Updated records: {updated_count}")
print("Excel updated successfully!")
