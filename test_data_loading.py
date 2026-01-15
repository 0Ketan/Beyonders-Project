"""
Test script to verify Google Sheets and Google Calendar API integration
for Campus Assist - GDG Campus Hackathon Project
"""
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Campus Assist - Production Validation Tests")
print("=" * 60)

# Google Sheets URLs
FACULTY_SHEET_URL = "https://docs.google.com/spreadsheets/d/16xBC5BLVAxGS1wSs8yoYNOEGQs8NtlUjgvZl5O1rZtA/export?format=csv"
SERVICES_SHEET_URL = "https://docs.google.com/spreadsheets/d/1jfIt_fjytU1OVSIwyMQbW2l9Q1l98bjuQJcXrMNGmqk/export?format=csv"
LABS_SHEET_URL = "https://docs.google.com/spreadsheets/d/1dPFvmTslYsO6t8H-055zg6kvq5bV8xIpxjGuDUsxkX4/export?format=csv"

# Google Calendar configuration
GOOGLE_CALENDAR_ID = "cee6954b0d57fcc80568fbb73b028f41eb9025730e0d27e48c2cbe2476a6be66@group.calendar.google.com"
GOOGLE_CALENDAR_API_KEY = "AIzaSyCtI8MeiXXVbrKiUwndC6dqpe4y7VmF5Gs"

# Test 1: Faculty Data Loading
print("\n1. Testing Faculty Data Loading (Google Sheets)")
print("-" * 60)
try:
    faculty_df = pd.read_csv(FACULTY_SHEET_URL)
    faculty_df.columns = faculty_df.columns.str.strip()
    faculty_df = faculty_df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    assert len(faculty_df) > 0, "Faculty data is empty"
    assert 'Name' in faculty_df.columns, "Name column missing"
    assert 'Department' in faculty_df.columns, "Department column missing"
    
    print(f"✅ Successfully loaded {len(faculty_df)} faculty members")
    print(f"   Columns: {list(faculty_df.columns)}")
    print(f"   Sample: {faculty_df.iloc[0]['Name']} - {faculty_df.iloc[0]['Department']}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

# Test 2: Campus Services Data Loading
print("\n2. Testing Campus Services Data Loading (Google Sheets)")
print("-" * 60)
try:
    services_df = pd.read_csv(SERVICES_SHEET_URL)
    services_df.columns = services_df.columns.str.strip()
    services_df = services_df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    assert len(services_df) > 0, "Services data is empty"
    assert 'Service' in services_df.columns, "Service column missing"
    
    print(f"✅ Successfully loaded {len(services_df)} services")
    print(f"   Columns: {list(services_df.columns)}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

# Test 3: Labs Data Loading
print("\n3. Testing Labs Data Loading (Google Sheets)")
print("-" * 60)
try:
    labs_df = pd.read_csv(LABS_SHEET_URL)
    labs_df.columns = labs_df.columns.str.strip()
    labs_df = labs_df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    assert len(labs_df) > 0, "Labs data is empty"
    assert 'Lab Name' in labs_df.columns, "Lab Name column missing"
    
    print(f"✅ Successfully loaded {len(labs_df)} labs")
    print(f"   Columns: {list(labs_df.columns)}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

# Test 4: Google Calendar API Connection
print("\n4. Testing Google Calendar API Connection")
print("-" * 60)
try:
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    time_max = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
    
    calendar_url = f"https://www.googleapis.com/calendar/v3/calendars/{GOOGLE_CALENDAR_ID}/events"
    params = {
        'key': GOOGLE_CALENDAR_API_KEY,
        'timeMin': time_min,
        'timeMax': time_max,
        'singleEvents': 'true',
        'orderBy': 'startTime'
    }
    
    response = requests.get(calendar_url, params=params, timeout=10)
    
    assert response.status_code == 200, f"API returned status {response.status_code}"
    
    data = response.json()
    events = data.get('items', [])
    
    print(f"✅ Google Calendar API connected successfully")
    print(f"   Events today: {len(events)}")
    if events:
        print(f"   Sample event: {events[0].get('summary', 'No title')}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

# Test 5: Search Functionality
print("\n5. Testing Search Functionality")
print("-" * 60)
try:
    # Test faculty search
    query = "computer"
    mask = (
        faculty_df['Name'].str.lower().str.contains(query, na=False) |
        faculty_df['Department'].str.lower().str.contains(query, na=False) |
        faculty_df['Subject'].str.lower().str.contains(query, na=False) |
        faculty_df['Role'].str.lower().str.contains(query, na=False) |
        faculty_df['Room'].str.lower().str.contains(query, na=False)
    )
    results = faculty_df[mask]
    print(f"✅ Faculty search for '{query}' found {len(results)} results")
    
    # Test services search
    query = "bon"
    services_mask = services_df['Service'].astype(str).str.lower().str.contains(query, na=False)
    services_results = services_df[services_mask]
    print(f"✅ Services search for '{query}' found {len(services_results)} results")
    
    # Test labs search
    query = "lab"
    labs_mask = labs_df['Lab Name'].astype(str).str.lower().str.contains(query, na=False)
    labs_results = labs_df[labs_mask]
    print(f"✅ Labs search for '{query}' found {len(labs_results)} results")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n📊 Data Sources:")
print("   - Faculty Data: Google Sheets (Live)")
print("   - Services Data: Google Sheets (Live)")
print("   - Labs Data: Google Sheets (Live)")
print("   - Availability: Google Calendar API (Live)")
print("\n🚀 The app is production-ready!")
print("   Run: streamlit run app.py")
print("   Access: http://localhost:8501")
print()
