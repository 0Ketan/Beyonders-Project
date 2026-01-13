"""
Quick test script to verify Google Sheets data loading
"""

import pandas as pd

# Google Sheets URLs
FACULTY_SHEET_URL = "https://docs.google.com/spreadsheets/d/16xBC5BLVAxGS1wSs8yoYNOEGQs8NtlUjgvZl5O1rZtA/export?format=csv"
TIMETABLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1lQoalBwyKMYG0qlUj7BT_nNbPXuNrFfW7BFkzaY-r58/export?format=csv"

print("Testing Google Sheets Data Loading...")
print("=" * 50)

# Test Faculty Data
print("\n1. Loading Faculty Data...")
try:
    faculty_df = pd.read_csv(FACULTY_SHEET_URL)
    faculty_df.columns = faculty_df.columns.str.strip()
    faculty_df = faculty_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    print(f"✅ Successfully loaded {len(faculty_df)} faculty members")
    print("\nColumns:", list(faculty_df.columns))
    print("\nFirst 3 rows:")
    print(faculty_df.head(3))
except Exception as e:
    print(f"❌ Error loading faculty data: {e}")

# Test Timetable Data
print("\n" + "=" * 50)
print("\n2. Loading Timetable Data...")
try:
    timetable_df = pd.read_csv(TIMETABLE_SHEET_URL)
    timetable_df.columns = timetable_df.columns.str.strip()
    timetable_df = timetable_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    print(f"✅ Successfully loaded {len(timetable_df)} timetable entries")
    print("\nColumns:", list(timetable_df.columns))
    print("\nFirst 5 rows:")
    print(timetable_df.head(5))
except Exception as e:
    print(f"❌ Error loading timetable data: {e}")

# Test Search Functionality
print("\n" + "=" * 50)
print("\n3. Testing Search Functionality...")
try:
    query = "computer"
    mask = (
        faculty_df['Name'].str.lower().str.contains(query, na=False) |
        faculty_df['Department'].str.lower().str.contains(query, na=False) |
        faculty_df['Subject'].str.lower().str.contains(query, na=False) |
        faculty_df['Role'].str.lower().str.contains(query, na=False) |
        faculty_df['Room'].str.lower().str.contains(query, na=False)
    )
    results = faculty_df[mask]
    print(f"✅ Search for '{query}' found {len(results)} results")
    print("\nResults:")
    print(results[['Name', 'Department', 'Role']])
except Exception as e:
    print(f"❌ Error testing search: {e}")

# Test Availability Logic
print("\n" + "=" * 50)
print("\n4. Testing Availability Logic...")
try:
    from datetime import datetime
    
    faculty_name = faculty_df.iloc[0]['Name']
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    
    print(f"Current Day: {current_day}")
    print(f"Current Time: {current_time}")
    print(f"Checking availability for: {faculty_name}")
    
    faculty_schedule = timetable_df[timetable_df['Name'] == faculty_name]
    print(f"Found {len(faculty_schedule)} schedule entries")
    
    if not faculty_schedule.empty:
        print("\nSchedule:")
        print(faculty_schedule[['Day', 'Start', 'End']])
    
    print("\n✅ Availability logic test completed")
except Exception as e:
    print(f"❌ Error testing availability: {e}")

print("\n" + "=" * 50)
print("\n✅ All tests completed!")
print("\nThe Streamlit app should be working correctly.")
print("Access it at: http://localhost:8501")
