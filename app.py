





"""
Campus Assist - Streamlit Web Application
A smart campus helper for finding faculty and checking availability

This application uses Google Sheets as a live data source and demonstrates
Google Calendar API integration for the GDG Campus Hackathon.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import requests
import os
import google.generativeai as genai

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
        # Using Indian Standard Time (UTC+5:30)
        ist = timezone(timedelta(hours=5, minutes=30))
        now = datetime.now(ist)
        
        # Start of today (00:00:00)
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        
        # End of today (23:59:59)
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
    
    Process:
    1. Fetch all events for today from Google Calendar API
    2. Parse event titles to extract faculty names
    3. Check if current time overlaps with any event for this faculty
    4. Return availability status
    
    Args:
        faculty_name (str): Name of the faculty member
        
    Returns:
        dict: {
            'available': bool,
            'status': str (description with time if in class),
            'error': bool (True if API call failed)
        }
    """
    # Fetch events from Google Calendar
    events = fetch_calendar_events()
    
    # If API call failed, return error status
    if events is None:
        return {
            'available': False,
            'status': '❌ Unable to fetch calendar data',
            'error': True
        }
    
    # Get current time (IST - UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    
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
    """Display the home page with project description."""
    
    st.title("🎓 Campus Assist")
    st.subheader("Smart Campus Helper")
    
    st.markdown("---")
    
    # Project Description
    st.markdown("""
    ### Welcome to Campus Assist!
    
    Campus Assist helps students navigate campus life more efficiently by providing:
    
    - 🔍 **Smart Faculty Search** - Find faculty by name, department, subject, role, or room
    - ⏰ **Real-time Availability** - Check if faculty are currently available or in class
    - 🏢 **Campus Services** - Locate offices for administrative tasks
    - 🔬 **Labs Directory** - Browse campus labs by department and location
    
    ### 🌟 Google Technology Integration
    
    This application demonstrates the power of Google technologies:
    
    #### 📊 Google Sheets as Live Backend
    - All faculty data is stored in **Google Sheets**
    - Data syncs in real-time - no hardcoded information
    - Easy to update and maintain by campus administrators
    - Collaborative editing capabilities
    
    #### 📅 Google Calendar Integration
    - Faculty availability is fetched from **Google Calendar API**
    - Live teaching events from shared public calendar
    - Real-time availability checking
    - Event titles automatically parsed to identify faculty
    
    ### 🚀 How It Works
    
    1. **Data Source**: Faculty information is maintained in Google Sheets
    2. **Live Sync**: The app fetches fresh data every time you search
    3. **Smart Search**: Type any keyword to find faculty instantly
    4. **Availability Check**: Real-time queries to Google Calendar API to check teaching events
    
    ### 📱 Get Started
    
    Use the sidebar to navigate:
    - **Find Faculty** - Search for faculty and check availability
    - **Campus Services** - Browse campus office locations
    - **Labs Directory** - Find campus labs and their details
    
    ---
    
    **Built for GDG Campus Hackathon** | Powered by Google Sheets & Streamlit
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: FIND FACULTY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_find_faculty_page():
    """Display the Find Faculty page with search and availability checking."""
    
    st.title("🔍 Find Faculty")
    
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
    
    st.markdown("---")
    
    # Search Bar
    st.markdown("### Search Faculty")
    search_query = st.text_input(
        "Search by name, department, subject, role, or room",
        placeholder="e.g., Computer Science, DBMS, HOD, CS-201",
        help="Type any keyword to search across all fields"
    )
    
    # Perform search
    if search_query:
        results_df = search_faculty(search_query, faculty_df)
    else:
        results_df = faculty_df
    
    st.markdown(f"**Found {len(results_df)} faculty member(s)**")
    
    # Display results
    if results_df.empty:
        st.warning("No faculty found matching your search.")
    else:
        # Display results as clickable list
        st.markdown("### Search Results")
        
        # Create columns for better layout
        for idx, row in results_df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display faculty info
                    st.markdown(f"**{row['Name']}**")
                    st.caption(f"{row['Department']} | {row['Role']}")
                
                with col2:
                    # Button to view details
                    if st.button("View Details", key=f"btn_{idx}"):
                        st.session_state['selected_faculty'] = row['Name']
                
                st.markdown("---")
        
        # Display selected faculty details
        if 'selected_faculty' in st.session_state and st.session_state['selected_faculty']:
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
        
        # Show current time
        now = datetime.now()
        st.caption(f"Current: {now.strftime('%A, %H:%M')}")
    
    # Clear selection button
    if st.button("← Back to Search Results"):
        st.session_state['selected_faculty'] = None
        st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: CAMPUS SERVICES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_campus_services_page():
    """Display the Campus Services page with live data from Google Sheets."""
    
    st.title("🏢 Campus Services")
    
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
    st.markdown("Find the right office for your needs")
    st.markdown("---")

    # Search Bar
    st.markdown("### Search Services")
    search_query = st.text_input(
        "Search by service name, office, room, or description",
        placeholder="e.g., Bonafide, Fee, Admission, Accounts",
        help="Type any keyword to search for campus services"
    )
    
    # Perform search
    if search_query:
        results_df = search_services(search_query, services_df)
    else:
        results_df = services_df
    
    st.markdown(f"**Found {len(results_df)} service(s)**")
    
    # Display results
    if results_df.empty:
        st.warning("No services found matching your search.")
    else:
        st.markdown("---")

        
        # Service Selector (dropdown)
        service_names = results_df['Service'].unique().tolist()
        selected_service_name = st.selectbox(
            "Select a Service",
            options=service_names,
            help="Choose a service to view detailed information"
        )
    
        if selected_service_name:
            # Get details for selected service
            service_info = results_df[results_df['Service'] == selected_service_name].iloc[0]
            
            # Display details in a nice card-like layout
            with st.container():
                st.markdown("---")
                st.markdown(f"### {service_info['Service']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**📍 Office:** {service_info['Office']}")
                    st.markdown(f"**🚪 Room:** {service_info['Room']}")
                
                with col2:
                    st.markdown(f"**🕒 Working Hours:** {service_info['Working Hours']}")
                
                st.markdown("---")
                st.markdown("#### Description")
                st.write(service_info['Description'])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LABS DIRECTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_labs_directory_page():
    """Display the Labs Directory page with live data from Google Sheets."""
    
    st.title("🔬 Labs Directory")
    
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
    st.markdown("Find labs by name or department")
    st.markdown("---")

    # Search Bar
    st.markdown("### Search Labs")
    search_query = st.text_input(
        "Search by lab name, department, building, room, or description",
        placeholder="e.g., Computer Lab, CSE, Block A, Lab-101",
        help="Type any keyword to search for labs"
    )
    
    # Perform search
    if search_query:
        results_df = search_labs(search_query, labs_df)
    else:
        results_df = labs_df
    
    st.markdown(f"**Found {len(results_df)} lab(s)**")
    
    # Display results
    if results_df.empty:
        st.warning("No labs found matching your search.")
    else:
        st.markdown("---")
        
        # Lab Selector (dropdown)
        lab_names = results_df['Lab Name'].unique().tolist()
        selected_lab_name = st.selectbox(
            "Select a Lab",
            options=lab_names,
            help="Choose a lab to view detailed information"
        )
        
        if selected_lab_name:
            # Get details for selected lab
            lab_info = results_df[results_df['Lab Name'] == selected_lab_name].iloc[0]
            
            # Display details in a nice card-like layout
            with st.container():
                st.markdown("---")
                st.markdown(f"### {lab_info['Lab Name']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**🏛️ Department:** {lab_info['Department']}")
                    st.markdown(f"**🏢 Building:** {lab_info['Building']}")
                    st.markdown(f"**🚪 Room:** {lab_info['Room']}")
                
                with col2:
                    st.markdown(f"**🕒 Working Hours:** {lab_info['Working Hours']}")
                
                st.markdown("---")
                st.markdown("#### Description")
                st.write(lab_info['Description'])



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AI ASSISTANT PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_ai_assistant_page():
    """Display the AI Assistant page using Google Gemini."""
    
    st.title("🤖 Ask Campus Assist (AI)")
    st.markdown("Powered by **Google Gemini**")
    
    # Check for API Key
    if not GEMINI_API_KEY:
        st.warning("⚠️ Google Gemini API Key not found. Please set `GEMINI_API_KEY` in your environment variables or Streamlit secrets.")
        st.info("To test this feature, you need a valid Google Gemini API key.")
        return

    # Initialize Gemini
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error configuring Google Gemini: {e}")
        return

    st.markdown("""
    I am your AI Campus Assistant! Ask me about:
    - 👨‍🏫 **Faculty** details and roles
    - 🏢 **Campus Services** and offices
    - 🔬 **Labs** and facilities
    - 🎓 **General** college procedures
    """)
    
    st.markdown("---")

    # User Input
    user_question = st.text_input("How can I help you today?", placeholder="e.g., Where is the admission office? Who is the HOD of CSE?")
    
    if st.button("Ask AI", type="primary"):
        if not user_question:
            st.warning("Please enter a question.")
            return
            
        with st.spinner("Thinking..."):
            try:
                # Context for the AI
                system_prompt = """
                You are a helpful campus assistant for a university. 
                Provide clear, concise, and polite answers to student questions related to college services, academics, and campus facilities.
                If a question is completely unrelated to college/campus life, politely decline to answer.
                Keep answers short and helpful.
                """
                
                # Create prompt with context
                full_prompt = f"{system_prompt}\n\nStudent Question: {user_question}"
                
                # Generate response
                response = model.generate_content(full_prompt)
                
                # Display response
                st.markdown("### 🤖 Response:")
                st.success(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.markdown("*Note: Please ensure your API key is valid and has access to Gemini API.*")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN APPLICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Main application entry point."""
    
    # Initialize session state
    if 'selected_faculty' not in st.session_state:
        st.session_state['selected_faculty'] = None
    
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
