





"""
Campus Assist - Streamlit Web Application
A smart campus helper for finding faculty and checking availability

This application uses Google Sheets as a live data source and demonstrates
Google Calendar API integration for the GDG Campus Hackathon.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import os
import google.genai as genai

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GOOGLE SHEETS CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Faculty Data Sheet - Contains faculty information
FACULTY_SHEET_URL = "https://docs.google.com/spreadsheets/d/16xBC5BLVAxGS1wSs8yoYNOEGQs8NtlUjgvZl5O1rZtA/export?format=csv"

# Campus Services Sheet - Contains office and service info
SERVICES_SHEET_URL = "https://docs.google.com/spreadsheets/d/1jfIt_fjytU1OVSIwyMQbW2l9Q1l98bjuQJcXrMNGmqk/export?format=csv"

# Labs Directory Sheet - Contains lab information
LABS_SHEET_URL = "https://docs.google.com/spreadsheets/d/1dPFvmTslYsO6t8H-055zg6kvq5bV8xIpxjGuDUsxkX4/export?format=csv"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GOOGLE CALENDAR API CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Google Calendar ID - Shared public calendar with faculty teaching events
GOOGLE_CALENDAR_ID = "cee6954b0d57fcc80568fbb73b028f41eb9025730e0d27e48c2cbe2476a6be66@group.calendar.google.com"

# Google Calendar API Key - Read-only access to public calendar
GOOGLE_CALENDAR_API_KEY = "AIzaSyCtI8MeiXXVbrKiUwndC6dqpe4y7VmF5Gs"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GOOGLE GEMINI AI CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Configure Gemini API Key
# Priority 1: OS Environment Variable (Local Development)
# Priority 2: Streamlit Secrets (Cloud Deployment)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        # Check Streamlit secrets if not found in env vars
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except (FileNotFoundError, KeyError):
        # Key remains None if not found in either
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TIMEZONE CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_current_ist_time():
    """
    Get current time in Indian Standard Time (IST).
    
    CRITICAL: Streamlit Cloud runs in UTC timezone.
    This function ensures consistent IST time across all environments:
    - Local development (any timezone)
    - Streamlit Cloud deployment (UTC)
    
    Returns:
        datetime: Current time in Asia/Kolkata timezone (IST)
    """
    # Streamlit Cloud runs in UTC; explicitly converting to IST
    return datetime.now(ZoneInfo("Asia/Kolkata"))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Campus Assist",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA LOADING FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_faculty_data():
    """
    Load faculty data from Google Sheets.
    
    This function fetches live data from Google Sheets, demonstrating
    the use of Google technology as a backend data source.
    
    Returns:
        pandas.DataFrame: Faculty data with columns: Name, Department, Subject, Role, Room
    """
    try:
        df = pd.read_csv(FACULTY_SHEET_URL)
        # Strip whitespace from column names and values
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error loading faculty data: {e}")
        return pd.DataFrame()





@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_services_data():
    """
    Load campus services data from Google Sheets.
    
    Returns:
        pandas.DataFrame: Services data with columns: Service, Office, Room, Working Hours, Description
    """
    try:
        df = pd.read_csv(SERVICES_SHEET_URL)
        # Strip whitespace from column names and values
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error loading services data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_labs_data():
    """
    Load labs data from Google Sheets.
    
    This function fetches live lab directory information from Google Sheets,
    demonstrating the use of Google technology as a backend data source.
    
    Returns:
        pandas.DataFrame: Labs data with columns: Lab Name, Department, Building, Room, Working Hours, Description
    """
    try:
        df = pd.read_csv(LABS_SHEET_URL)
        # Strip whitespace from column names and values
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error loading labs data: {e}")
        return pd.DataFrame()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GOOGLE CALENDAR API INTEGRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fetch_calendar_events():
    """
    Fetch today's events from Google Calendar API.
    
    This function queries the Google Calendar API to get all events scheduled
    for the current day. Events contain faculty teaching schedules.
    
    Returns:
        list: List of calendar events, or None if API call fails
        Each event has: summary (title), start (datetime), end (datetime)
    """
    try:
        # Get today's date range in ISO format (required by Google Calendar API)
        # Streamlit Cloud runs in UTC; explicitly converting to IST
        now = get_current_ist_time()
        
        # Start of today (00:00:00 IST)
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        
        # End of today (23:59:59 IST)
        time_max = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
        
        # Build Google Calendar API request URL
        base_url = "https://www.googleapis.com/calendar/v3/calendars"
        calendar_url = f"{base_url}/{GOOGLE_CALENDAR_ID}/events"
        
        # API parameters
        params = {
            'key': GOOGLE_CALENDAR_API_KEY,
            'timeMin': time_min,
            'timeMax': time_max,
            'singleEvents': 'true',  # Expand recurring events
            'orderBy': 'startTime'
        }
        
        # Make API request
        response = requests.get(calendar_url, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            st.error(f"Google Calendar API error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Google Calendar API request timed out")
        return None
    except Exception as e:
        st.error(f"Error fetching calendar data: {e}")
        return None


def parse_faculty_name_from_event(event_title):
    """
    Extract faculty name from calendar event title.
    
    Event titles are expected to follow the format:
    "Faculty Name – Class Description"
    Example: "Brojo Kishore Mishra – Data Structures Class"
    
    Args:
        event_title (str): Calendar event title/summary
        
    Returns:
        str: Extracted faculty name, or None if pattern doesn't match
    """
    if not event_title:
        return None
    
    # Split by em dash (–) or regular dash (-)
    # Event format: "Faculty Name – Class Description"
    for separator in ['–', '—', '-']:
        if separator in event_title:
            parts = event_title.split(separator, 1)
            if parts:
                return parts[0].strip()
    
    # If no separator found, assume entire title is faculty name
    return event_title.strip()


def check_faculty_availability(faculty_name):
    """
    Check if a faculty member is currently available based on Google Calendar.
    
    REAL GOOGLE CALENDAR INTEGRATION:
    ----------------------------------
    This function fetches live events from the shared Google Calendar and determines
    faculty availability by checking if they have any teaching events happening now.
    
    CAMPUS WORKING HOURS:
    ---------------------
    College is open from 7:00 AM to 5:00 PM.
    Faculty are automatically unavailable outside these hours.
    
    WEEKLY HOLIDAY:
    ---------------
    Sunday is a weekly holiday.
    All faculty are unavailable on Sundays.
    
    Priority Order:
    1. Sunday holiday check (highest priority)
    2. Campus working hours check (7 AM - 5 PM)
    3. Google Calendar class schedule check
    4. Default available status
    
    Process:
    1. Check if today is Sunday (weekly holiday)
    2. If Sunday, return unavailable status immediately
    3. Check if current time is within campus working hours (7 AM - 5 PM)
    4. If outside working hours, return unavailable status immediately
    5. If within working hours, fetch events from Google Calendar API
    6. Parse event titles to extract faculty names
    7. Check if current time overlaps with any event for this faculty
    8. Return availability status
    
    Args:
        faculty_name (str): Name of the faculty member
        
    Returns:
        dict: {
            'available': bool,
            'status': str (description with time if in class),
            'error': bool (True if API call failed)
        }
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 1: Check Sunday Holiday (HIGHEST PRIORITY)
    # ═══════════════════════════════════════════════════════════════════════════
    # Weekly holiday: Sunday
    # Faculty unavailable on Sundays
    
    # Get current time in IST (Asia/Kolkata timezone)
    # Streamlit Cloud runs in UTC; explicitly converting to IST
    now = get_current_ist_time()
    current_weekday = now.weekday()  # Monday=0, Sunday=6
    
    # Check if today is Sunday (weekday = 6)
    if current_weekday == 6:
        return {
            'available': False,
            'status': '🔒 Unavailable (Holiday)',
            'error': False
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 2: Check Campus Working Hours
    # ═══════════════════════════════════════════════════════════════════════════
    # Campus working hours: 7 AM – 5 PM
    # Outside working hours, faculty are unavailable
    
    current_hour = now.hour
    current_minute = now.minute
    
    # Define campus working hours
    COLLEGE_OPEN_HOUR = 7   # 7:00 AM
    COLLEGE_CLOSE_HOUR = 17  # 5:00 PM (17:00 in 24-hour format)
    
    # Check if current time is outside working hours
    # Before 7:00 AM or at/after 5:00 PM
    if current_hour < COLLEGE_OPEN_HOUR or current_hour >= COLLEGE_CLOSE_HOUR:
        return {
            'available': False,
            'status': '🔒 Unavailable (College Closed - Hours: 7 AM to 5 PM)',
            'error': False
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 3: Check Google Calendar (only during working hours and non-holidays)
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Fetch events from Google Calendar
    events = fetch_calendar_events()
    
    # If API call failed, return error status
    if events is None:
        return {
            'available': False,
            'status': '❌ Unable to fetch calendar data',
            'error': True
        }
    
    # Check each event to see if faculty is currently in class
    for event in events:
        # Get event title
        event_title = event.get('summary', '')
        
        # Extract faculty name from event title
        event_faculty_name = parse_faculty_name_from_event(event_title)
        
        # Check if this event belongs to the faculty we're looking for
        # Case-insensitive partial match to handle variations in naming
        if event_faculty_name and faculty_name.lower() in event_faculty_name.lower():
            # Get event start and end times
            event_start = event.get('start', {}).get('dateTime')
            event_end = event.get('end', {}).get('dateTime')
            
            if event_start and event_end:
                try:
                    # Parse event times (ISO format with timezone)
                    start_time = datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                    
                    # Check if current time is within event time
                    if start_time <= now <= end_time:
                        # Format times for display (24-hour format)
                        start_str = start_time.strftime("%H:%M")
                        end_str = end_time.strftime("%H:%M")
                        
                        return {
                            'available': False,
                            'status': f'🔴 In Class ({start_str} - {end_str}) (Based on Google Calendar)',
                            'error': False
                        }
                except Exception as e:
                    # Skip this event if time parsing fails
                    continue
    
    # No matching events found - faculty is available
    return {
        'available': True,
        'status': '✅ Available (Based on Google Calendar)',
        'error': False
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SEARCH FUNCTIONALITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def search_faculty(query, faculty_df):
    """
    Search for faculty members across all fields.
    
    Performs case-insensitive partial matching across:
    - Name
    - Department
    - Subject
    - Role
    - Room
    
    Args:
        query (str): Search query
        faculty_df (pandas.DataFrame): Faculty data
        
    Returns:
        pandas.DataFrame: Filtered faculty results
    """
    if not query or query.strip() == "":
        return faculty_df
    
    query = query.lower().strip()
    
    # Search across all columns
    mask = (
        faculty_df['Name'].str.lower().str.contains(query, na=False) |
        faculty_df['Department'].str.lower().str.contains(query, na=False) |
        faculty_df['Subject'].str.lower().str.contains(query, na=False) |
        faculty_df['Role'].str.lower().str.contains(query, na=False) |
        faculty_df['Room'].str.lower().str.contains(query, na=False)
    )
    
    return faculty_df[mask]


def search_labs(query, labs_df):
    """
    Search for labs by name, department, building, room, or description.
    
    Performs case-insensitive partial matching across:
    - Lab Name
    - Department
    - Building
    - Room
    - Description
    
    Args:
        query (str): Search query
        labs_df (pandas.DataFrame): Labs data
        
    Returns:
        pandas.DataFrame: Filtered labs results
    """
    if not query or query.strip() == "":
        return labs_df
    
    query = query.lower().strip()
    
    # Search across all relevant columns
    # Convert to string first to handle potential NaN values safely
    mask = (
        labs_df['Lab Name'].astype(str).str.lower().str.contains(query, na=False) |
        labs_df['Department'].astype(str).str.lower().str.contains(query, na=False) |
        labs_df['Building'].astype(str).str.lower().str.contains(query, na=False) |
        labs_df['Room'].astype(str).str.lower().str.contains(query, na=False) |
        labs_df['Description'].astype(str).str.lower().str.contains(query, na=False)
    )
    
    return labs_df[mask]


def search_services(query, services_df):
    """
    Search for campus services by name, office, room, or description.
    
    Performs case-insensitive partial matching across:
    - Service
    - Office
    - Room
    - Description
    
    Args:
        query (str): Search query
        services_df (pandas.DataFrame): Services data
        
    Returns:
        pandas.DataFrame: Filtered services results
    """
    if not query or query.strip() == "":
        return services_df
    
    query = query.lower().strip()
    
    # Search across all relevant columns
    # Convert to string first to handle potential NaN values safely
    mask = (
        services_df['Service'].astype(str).str.lower().str.contains(query, na=False) |
        services_df['Office'].astype(str).str.lower().str.contains(query, na=False) |
        services_df['Room'].astype(str).str.lower().str.contains(query, na=False) |
        services_df['Description'].astype(str).str.lower().str.contains(query, na=False)
    )
    
    return services_df[mask]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_home_page():
    """Display the home page with feature cards."""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # WELCOME SECTION (Centered)
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("<h1 style='text-align: center;'>🎓 Campus Assist</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #666;'>Your Smart Campus Navigation Helper</p>", unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FEATURE CARDS (2x2 Grid)
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("### 🌟 Explore Features")
    st.markdown("")  # Spacing
    
    # Row 1: Find Faculty + Campus Services
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container():
            st.markdown("#### 🔍 Find Faculty")
            st.markdown("Search for faculty members by name, department, subject, or room. Check real-time availability using Google Calendar integration.")
            st.markdown("")  # Spacing
            # Note: Navigation happens via sidebar, so we just display info
    
    with col2:
        with st.container():
            st.markdown("#### 🏢 Campus Services")
            st.markdown("Locate administrative offices and campus services. Find the right office for bonafide certificates, fee payments, admissions, and more.")
            st.markdown("")  # Spacing
    
    st.markdown("")  # Spacing between rows
    
    # Row 2: Labs Directory + AI Assistant
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        with st.container():
            st.markdown("#### 🔬 Labs Directory")
            st.markdown("Browse campus labs by department and location. View lab details, working hours, and available facilities.")
            st.markdown("")  # Spacing
    
    with col4:
        with st.container():
            st.markdown("#### 🤖 AI Assistant")
            st.markdown("Ask questions about campus facilities, faculty, services, and procedures. Get instant AI-powered answers using Google Gemini.")
            st.markdown("")  # Spacing
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TECH STACK INFO (Collapsed by default)
    # ═══════════════════════════════════════════════════════════════════════════
    
    with st.expander("🌟 Powered by Google Technologies"):
        st.markdown("""
        **📊 Google Sheets** - Live data backend for faculty, services, and labs  
        **📅 Google Calendar API** - Real-time faculty availability tracking  
        **🤖 Google Gemini AI** - Intelligent campus assistant  
        
        All data syncs in real-time with no hardcoded information!
        """)
    
    st.markdown("")  # Spacing
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #888;'>Built for GDG Campus Hackathon | Powered by Google & Streamlit</p>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: FIND FACULTY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_find_faculty_page():
    """Display the Find Faculty page with search and card-based results."""
    
    st.title("🔍 Find Faculty")
    st.markdown("")
    
    # Load data from Google Sheets
    faculty_df = load_faculty_data()
    
    # Debug requirement: Display number of loaded faculty members
    if not faculty_df.empty:
        st.info(f"🐛 DEBUG: Loaded {len(faculty_df)} faculty members from Google Sheets")
    
    if faculty_df.empty:
        st.error("Unable to load faculty data. Please check your internet connection.")
        return
    
    # Display data source indicator
    st.success("📊 Data synced live from Google Sheets")
    st.markdown("")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SEARCH BAR (Full Width)
    # ═══════════════════════════════════════════════════════════════════════════
    
    search_query = st.text_input(
        "🔍 Search Faculty",
        placeholder="e.g., Computer Science, DBMS, HOD, CS-201",
        help="Search by name, department, subject, role, or room"
    )
    
    # Perform search
    if search_query:
        results_df = search_faculty(search_query, faculty_df)
    else:
        results_df = faculty_df
    
    st.markdown(f"**Found {len(results_df)} faculty member(s)**")
    st.markdown("")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FACULTY CARDS (2 per row)
    # ═══════════════════════════════════════════════════════════════════════════
    
    if results_df.empty:
        st.warning("No faculty found matching your search.")
    else:
        # Display results as cards in 2-column grid
        results_list = results_df.to_dict('records')
        
        # Process in pairs for 2-column layout
        for i in range(0, len(results_list), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            # First card
            with col1:
                faculty = results_list[i]
                with st.container():
                    # Faculty Name (Bold, Larger)
                    st.markdown(f"### {faculty['Name']}")
                    
                    # Department and Role
                    st.markdown(f"**{faculty['Department']}** | {faculty['Role']}")
                    
                    # Room
                    st.markdown(f"📍 Room: {faculty['Room']}")
                    
                    # Subject
                    st.caption(f"Subject: {faculty['Subject']}")
                    
                    st.markdown("")
                    
                    # View Details Button
                    if st.button("View Details", key=f"faculty_btn_{i}", use_container_width=True):
                        st.session_state['selected_faculty'] = faculty['Name']
                        st.rerun()
                    
                    st.markdown("")
            
            # Second card (if exists)
            if i + 1 < len(results_list):
                with col2:
                    faculty = results_list[i + 1]
                    with st.container():
                        # Faculty Name (Bold, Larger)
                        st.markdown(f"### {faculty['Name']}")
                        
                        # Department and Role
                        st.markdown(f"**{faculty['Department']}** | {faculty['Role']}")
                        
                        # Room
                        st.markdown(f"📍 Room: {faculty['Room']}")
                        
                        # Subject
                        st.caption(f"Subject: {faculty['Subject']}")
                        
                        st.markdown("")
                        
                        # View Details Button
                        if st.button("View Details", key=f"faculty_btn_{i+1}", use_container_width=True):
                            st.session_state['selected_faculty'] = faculty['Name']
                            st.rerun()
                        
                        st.markdown("")
        
        # Display selected faculty details
        if 'selected_faculty' in st.session_state and st.session_state['selected_faculty']:
            st.markdown("---")
            display_faculty_details(st.session_state['selected_faculty'], faculty_df)


def display_faculty_details(faculty_name, faculty_df):
    """
    Display detailed information for a selected faculty member.
    
    Args:
        faculty_name (str): Name of the faculty member
        faculty_df (pandas.DataFrame): Faculty data
    """
    st.markdown("---")
    st.markdown("## 👤 Faculty Details")
    
    # Get faculty info
    faculty_info = faculty_df[faculty_df['Name'] == faculty_name].iloc[0]
    
    # Check availability using Google Calendar
    availability = check_faculty_availability(faculty_name)
    
    # Display in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {faculty_info['Name']}")
        st.markdown(f"**Department:** {faculty_info['Department']}")
        st.markdown(f"**Subject:** {faculty_info['Subject']}")
        st.markdown(f"**Role:** {faculty_info['Role']}")
        st.markdown(f"**Room:** {faculty_info['Room']}")
    
    with col2:
        st.markdown("### Availability (Live from Google Calendar)")
        
        # Display status with appropriate styling based on error state
        if availability.get('error', False):
            st.error(availability['status'])
        else:
            st.markdown(availability['status'])
        
        # Show current time in IST
        # Streamlit Cloud runs in UTC; explicitly converting to IST
        now = get_current_ist_time()
        st.caption(f"Current: {now.strftime('%A, %H:%M')} IST")
    
    # Clear selection button
    if st.button("← Back to Search Results"):
        st.session_state['selected_faculty'] = None
        st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: CAMPUS SERVICES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_campus_services_page():
    """Display the Campus Services page with card-based layout."""
    
    st.title("🏢 Campus Services")
    st.markdown("")
    
    # Load data
    services_df = load_services_data()
    
    # Debug requirement: Display number of loaded services
    if not services_df.empty:
        st.info(f"🐛 DEBUG: Loaded {len(services_df)} services from Google Sheets")
    
    if services_df.empty:
        st.error("Unable to load services data. Please check your connection.")
        return

    # Display data source indicator
    st.success("📊 Data synced live from Google Sheets")
    st.markdown("")

    # ═══════════════════════════════════════════════════════════════════════════
    # SEARCH BAR (Full Width)
    # ═══════════════════════════════════════════════════════════════════════════

    search_query = st.text_input(
        "🔍 Search Services",
        placeholder="e.g., Bonafide, Fee, Admission, Accounts",
        help="Search by service name, office, room, or description"
    )
    
    # Perform search
    if search_query:
        results_df = search_services(search_query, services_df)
    else:
        results_df = services_df
    
    st.markdown(f"**Found {len(results_df)} service(s)**")
    st.markdown("")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SERVICE CARDS (2 per row)
    # ═══════════════════════════════════════════════════════════════════════════
    
    if results_df.empty:
        st.warning("No services found matching your search.")
    else:
        # Display results as cards in 2-column grid
        results_list = results_df.to_dict('records')
        
        # Process in pairs for 2-column layout
        for i in range(0, len(results_list), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            # First card
            with col1:
                service = results_list[i]
                with st.container():
                    # Service Name (Bold, Larger)
                    st.markdown(f"### {service['Service']}")
                    
                    # Office
                    st.markdown(f"**📍 {service['Office']}**")
                    
                    # Room
                    st.markdown(f"🚪 Room: {service['Room']}")
                    
                    # Working Hours
                    st.caption(f"🕒 {service['Working Hours']}")
                    
                    st.markdown("")
                    
                    # Description in expander
                    with st.expander("View Details"):
                        st.write(service['Description'])
                    
                    st.markdown("")
            
            # Second card (if exists)
            if i + 1 < len(results_list):
                with col2:
                    service = results_list[i + 1]
                    with st.container():
                        # Service Name (Bold, Larger)
                        st.markdown(f"### {service['Service']}")
                        
                        # Office
                        st.markdown(f"**📍 {service['Office']}**")
                        
                        # Room
                        st.markdown(f"🚪 Room: {service['Room']}")
                        
                        # Working Hours
                        st.caption(f"🕒 {service['Working Hours']}")
                        


                        st.markdown("")
                        
                        # Description in expander
                        with st.expander("View Details"):
                            st.write(service['Description'])
                        
                        st.markdown("")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LABS DIRECTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_labs_directory_page():
    """Display the Labs Directory page with card-based layout."""
    
    st.title("🔬 Labs Directory")
    st.markdown("")
    
    # Load data from Google Sheets
    labs_df = load_labs_data()
    
    # Debug requirement: Display number of loaded labs
    if not labs_df.empty:
        st.info(f"🐛 DEBUG: Loaded {len(labs_df)} labs from Google Sheets")
    
    if labs_df.empty:
        st.error("Unable to load labs data. Please check your connection.")
        return

    # Display data source indicator
    st.success("📊 Data synced live from Google Sheets")
    st.markdown("")

    # ═══════════════════════════════════════════════════════════════════════════
    # SEARCH BAR (Full Width)
    # ═══════════════════════════════════════════════════════════════════════════

    search_query = st.text_input(
        "🔍 Search Labs",
        placeholder="e.g., Computer Lab, CSE, Block A, Lab-101",
        help="Search by lab name, department, building, room, or description"
    )
    
    # Perform search
    if search_query:
        results_df = search_labs(search_query, labs_df)
    else:
        results_df = labs_df
    
    st.markdown(f"**Found {len(results_df)} lab(s)**")
    st.markdown("")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LAB CARDS (2 per row)
    # ═══════════════════════════════════════════════════════════════════════════
    
    if results_df.empty:
        st.warning("No labs found matching your search.")
    else:
        # Display results as cards in 2-column grid
        results_list = results_df.to_dict('records')
        
        # Process in pairs for 2-column layout
        for i in range(0, len(results_list), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            # First card
            with col1:
                lab = results_list[i]
                with st.container():
                    # Lab Name (Bold, Larger)
                    st.markdown(f"### {lab['Lab Name']}")
                    
                    # Department
                    st.markdown(f"**🏛️ {lab['Department']}**")
                    
                    # Building and Room
                    st.markdown(f"📍 {lab['Building']}, Room: {lab['Room']}")
                    
                    # Working Hours
                    st.caption(f"🕒 {lab['Working Hours']}")
                    
                    st.markdown("")
                    
                    # Description in expander
                    with st.expander("View Details"):
                        st.write(lab['Description'])
                    
                    st.markdown("")
            
            # Second card (if exists)
            if i + 1 < len(results_list):
                with col2:
                    lab = results_list[i + 1]
                    with st.container():
                        # Lab Name (Bold, Larger)
                        st.markdown(f"### {lab['Lab Name']}")
                        
                        # Department
                        st.markdown(f"**🏛️ {lab['Department']}**")
                        
                        # Building and Room
                        st.markdown(f"📍 {lab['Building']}, Room: {lab['Room']}")
                        
                        # Working Hours
                        st.caption(f"🕒 {lab['Working Hours']}")
                        
                        st.markdown("")
                        
                        # Description in expander
                        with st.expander("View Details"):
                            st.write(lab['Description'])
                        
                        st.markdown("")



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AI ASSISTANT PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_ai_assistant_page():
    """Display the AI Assistant page using Google Gemini with production-safe error handling."""
    
    st.title("🤖 Ask Campus Assist (AI)")
    st.markdown("Powered by **Google Gemini**")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 1: Check for API Key
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if not GEMINI_API_KEY:
        st.warning("⚠️ Google Gemini API key is not configured")
        st.info(
            "To use this feature, please configure the API key:\n\n"
            "**For Local Development:**\n"
            "Set the `GEMINI_API_KEY` environment variable\n\n"
            "**For Streamlit Cloud:**\n"
            "Add `GEMINI_API_KEY` to your app secrets"
        )
        return

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 2: Initialize Gemini (with error handling)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    try:
        # Create Gemini client with the new google-genai package
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error("AI assistant is temporarily unavailable. Please try again later.")
        # Show technical details in expander for debugging
        with st.expander("Technical Details (for developers)"):
            st.code(f"Error configuring Gemini: {str(e)}")
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 3: Display Introduction
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("")
    st.markdown("""
    I am your AI Campus Assistant! Ask me about:
    - 👨‍🏫 **Faculty** details and roles
    - 🏢 **Campus Services** and offices
    - 🔬 **Labs** and facilities
    - 🎓 **General** college procedures
    """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 4: User Input with Form (enables Enter key submission)
    # ═══════════════════════════════════════════════════════════════════════════
    with st.form(key="ai_question_form", clear_on_submit=False):
        user_question = st.text_area(
            "💬 Ask your question:",
            placeholder="e.g., Where is the admission office? Who is the HOD of CSE?",
            help="Type your question and press Ctrl+Enter or click 'Ask AI'",
            height=100,
            key="ai_input"
        )
        
        st.markdown("")  # Spacing
        
        # Submit button
        submit_button = st.form_submit_button("🤖 Ask AI", type="primary", use_container_width=True)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 5: Process Input (with validation)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if submit_button:
        # Clear previous error
        st.session_state['ai_error'] = ""
        
        # Input validation: Check for empty or whitespace-only input
        if not user_question or user_question.strip() == "":
            st.warning("⚠️ Please enter a question before submitting")
        else:
            # Store the question in session state
            st.session_state['ai_last_question'] = user_question.strip()
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # STEP 6: Call Gemini API (with comprehensive error handling)
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with st.spinner("🤔 Thinking..."):
                try:
                    # Context for the AI
                    system_instruction = """
                    You are a helpful campus assistant for a university. 
                    Provide clear, concise, and polite answers to student questions related to college services, academics, and campus facilities.
                    If a question is completely unrelated to college/campus life, politely decline to answer.
                    Keep answers short and helpful.
                    """
                    
                    # Generate response using new API
                    response = client.models.generate_content(
                        model='gemini-flash-latest',
                        contents=f"{system_instruction}\n\nStudent Question: {user_question}"
                    )
                    
                    # Check if response is valid
                    if response and response.text:
                        # Store response in session state for persistence
                        st.session_state['ai_last_response'] = response.text
                    else:
                        # Handle empty response
                        st.session_state['ai_error'] = "empty_response"
                        st.session_state['ai_last_response'] = ""
                    
                except Exception as e:
                    # Comprehensive error handling - catch all API errors
                    error_type = type(e).__name__
                    
                    # Store error in session state
                    st.session_state['ai_error'] = "api_error"
                    st.session_state['ai_last_response'] = ""
                    
                    # Log error for debugging (optional - only visible in terminal)
                    print(f"[AI Assistant Error] {error_type}: {str(e)}")
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 7: Display Response (persisted across reruns)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Add spacing
    st.markdown("")
    
    # Display last response if available
    if st.session_state.get('ai_last_response'):
        st.markdown("### 🤖 Response:")
        
        # Display response in a nice container (dark mode compatible)
        with st.container():
            # Use info box for better visibility and dark mode compatibility
            st.info(st.session_state['ai_last_response'])
        
        # Show timestamp
        st.caption(f"💬 Question: {st.session_state.get('ai_last_question', '')}")
    
    # Display error if present
    elif st.session_state.get('ai_error'):
        st.markdown("### ⚠️ Error")
        
        if st.session_state['ai_error'] == "empty_response":
            st.error(
                "AI assistant returned an empty response. "
                "This might be due to content safety filters. "
                "Please try rephrasing your question."
            )
        elif st.session_state['ai_error'] == "api_error":
            st.error(
                "AI assistant is temporarily unavailable. Please try again later.\n\n"
                "If this issue persists, please check your internet connection or API key."
            )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 8: Example Questions (for better UX)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - Where is the admission office located?
        - Who is the HOD of Computer Science department?
        - What are the working hours for the library?
        - How do I get a bonafide certificate?
        - Where can I find the CSE lab?
        """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN APPLICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Main application entry point."""
    
    # Initialize session state for faculty selection
    if 'selected_faculty' not in st.session_state:
        st.session_state['selected_faculty'] = None
    
    # Initialize session state for AI assistant
    if 'ai_last_question' not in st.session_state:
        st.session_state['ai_last_question'] = ""
    if 'ai_last_response' not in st.session_state:
        st.session_state['ai_last_response'] = ""
    if 'ai_error' not in st.session_state:
        st.session_state['ai_error'] = ""
    
    # Sidebar Navigation
    st.sidebar.title("🎓 Campus Assist")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Find Faculty", "Campus Services", "Labs Directory", "Ask Campus Assist (AI)"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "Campus Assist helps students find faculty and check their availability in real-time.\n\n"
        "**Powered by:**\n"
        "- 📊 Google Sheets\n"
        "- 📅 Google Calendar API\n"
        "- 🤖 Google Gemini AI\n"
        "- 🚀 Streamlit"
    )
    
    # Display selected page
    if page == "Home":
        display_home_page()
    elif page == "Find Faculty":
        display_find_faculty_page()
    elif page == "Campus Services":
        display_campus_services_page()
    elif page == "Labs Directory":
        display_labs_directory_page()
    elif page == "Ask Campus Assist (AI)":
        display_ai_assistant_page()


if __name__ == "__main__":
    main()
