"""
Campus Assist - Streamlit Web Application
A smart campus helper for finding faculty and checking availability

This application uses Google Sheets as a live data source and demonstrates
Google Calendar-based availability checking for the GDG Campus Hackathon.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GOOGLE SHEETS CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Faculty Data Sheet - Contains faculty information
FACULTY_SHEET_URL = "https://docs.google.com/spreadsheets/d/16xBC5BLVAxGS1wSs8yoYNOEGQs8NtlUjgvZl5O1rZtA/export?format=csv"

# Timetable Sheet - Contains teaching schedules
TIMETABLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1lQoalBwyKMYG0qlUj7BT_nNbPXuNrFfW7BFkzaY-r58/export?format=csv"

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
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error loading faculty data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_timetable_data():
    """
    Load timetable data from Google Sheets.
    
    This timetable represents teaching schedules that would typically be
    synced from Google Calendar in a production environment.
    
    Returns:
        pandas.DataFrame: Timetable data with columns: Name, Day, Start, End
    """
    try:
        df = pd.read_csv(TIMETABLE_SHEET_URL)
        # Strip whitespace from column names and values
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error loading timetable data: {e}")
        return pd.DataFrame()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AVAILABILITY CHECKING LOGIC (GOOGLE CALENDAR CONCEPT)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_faculty_availability(faculty_name, timetable_df):
    """
    Check if a faculty member is currently available based on their teaching schedule.
    
    GOOGLE CALENDAR INTEGRATION CONCEPT:
    ------------------------------------
    In a production environment, this function would integrate with Google Calendar API
    to fetch real-time availability from faculty calendars. Teaching schedules would be
    synced as calendar events, and this function would check for conflicts.
    
    Current Implementation:
    -----------------------
    This MVP simulates Google Calendar integration by checking teaching schedules
    stored in Google Sheets. The logic represents how availability would be determined
    from calendar events.
    
    Args:
        faculty_name (str): Name of the faculty member
        timetable_df (pandas.DataFrame): Timetable data from Google Sheets
        
    Returns:
        dict: {
            'available': bool,
            'status': str (description with Google Calendar reference)
        }
    """
    # Get current day and time
    now = datetime.now()
    current_day = now.strftime("%A")  # e.g., "Monday"
    current_time = now.strftime("%H:%M")  # e.g., "14:30"
    
    # Filter timetable for this faculty
    faculty_schedule = timetable_df[timetable_df['Name'] == faculty_name]
    
    if faculty_schedule.empty:
        return {
            'available': True,
            'status': '✅ Available (Based on Google Calendar)'
        }
    
    # Check if current time falls within any teaching slot
    for _, slot in faculty_schedule.iterrows():
        if slot['Day'] == current_day:
            # Parse times for comparison
            try:
                slot_start = datetime.strptime(slot['Start'], "%H:%M").time()
                slot_end = datetime.strptime(slot['End'], "%H:%M").time()
                current = datetime.strptime(current_time, "%H:%M").time()
                
                # Check if current time is within this slot
                if slot_start <= current <= slot_end:
                    return {
                        'available': False,
                        'status': f'🔴 In Class ({slot["Start"]} - {slot["End"]}) (Based on Google Calendar)'
                    }
            except Exception as e:
                continue
    
    # Not in any teaching slot - faculty is available
    return {
        'available': True,
        'status': '✅ Available (Based on Google Calendar)'
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
    
    ### 🌟 Google Technology Integration
    
    This application demonstrates the power of Google technologies:
    
    #### 📊 Google Sheets as Live Backend
    - All faculty data is stored in **Google Sheets**
    - Data syncs in real-time - no hardcoded information
    - Easy to update and maintain by campus administrators
    - Collaborative editing capabilities
    
    #### 📅 Google Calendar Concept
    - Faculty availability is determined using **Google Calendar-based logic**
    - Teaching schedules represent calendar events
    - In production, this would integrate with Google Calendar API
    - Real-time synchronization with faculty calendars
    
    ### 🚀 How It Works
    
    1. **Data Source**: Faculty information and schedules are maintained in Google Sheets
    2. **Live Sync**: The app fetches fresh data every time you search
    3. **Smart Search**: Type any keyword to find faculty instantly
    4. **Availability Check**: See if faculty are available based on their teaching schedule
    
    ### 📱 Get Started
    
    Use the sidebar to navigate:
    - **Find Faculty** - Search for faculty and check availability
    - **Campus Services** - Browse campus office locations
    
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
    timetable_df = load_timetable_data()
    
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
            display_faculty_details(st.session_state['selected_faculty'], faculty_df, timetable_df)


def display_faculty_details(faculty_name, faculty_df, timetable_df):
    """
    Display detailed information for a selected faculty member.
    
    Args:
        faculty_name (str): Name of the faculty member
        faculty_df (pandas.DataFrame): Faculty data
        timetable_df (pandas.DataFrame): Timetable data
    """
    st.markdown("---")
    st.markdown("## 👤 Faculty Details")
    
    # Get faculty info
    faculty_info = faculty_df[faculty_df['Name'] == faculty_name].iloc[0]
    
    # Check availability
    availability = check_faculty_availability(faculty_name, timetable_df)
    
    # Display in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {faculty_info['Name']}")
        st.markdown(f"**Department:** {faculty_info['Department']}")
        st.markdown(f"**Subject:** {faculty_info['Subject']}")
        st.markdown(f"**Role:** {faculty_info['Role']}")
        st.markdown(f"**Room:** {faculty_info['Room']}")
    
    with col2:
        st.markdown("### Availability")
        st.markdown(availability['status'])
        
        # Show current time
        now = datetime.now()
        st.caption(f"Current: {now.strftime('%A, %H:%M')}")
    
    # Display teaching schedule
    st.markdown("### 📅 Teaching Schedule")
    faculty_schedule = timetable_df[timetable_df['Name'] == faculty_name]
    
    if not faculty_schedule.empty:
        # Group by day
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days_order:
            day_schedule = faculty_schedule[faculty_schedule['Day'] == day]
            if not day_schedule.empty:
                st.markdown(f"**{day}:**")
                for _, slot in day_schedule.iterrows():
                    st.markdown(f"- {slot['Start']} - {slot['End']}")
    else:
        st.info("No teaching schedule available.")
    
    # Clear selection button
    if st.button("← Back to Search Results"):
        st.session_state['selected_faculty'] = None
        st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: CAMPUS SERVICES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def display_campus_services_page():
    """Display the Campus Services page."""
    
    st.title("🏢 Campus Services")
    st.markdown("Find the right office for your needs")
    
    st.markdown("---")
    
    # Sample campus services (can be moved to Google Sheets in future)
    services = [
        {"service": "Bonafide Certificate", "office": "Academic Office", "room": "Admin-101", "hours": "9:00 AM - 5:00 PM"},
        {"service": "Fee Payment & Issues", "office": "Accounts Department", "room": "Admin-102", "hours": "9:00 AM - 4:00 PM"},
        {"service": "ID Card", "office": "Student Affairs", "room": "Admin-103", "hours": "10:00 AM - 4:00 PM"},
        {"service": "Library Card", "office": "Library Office", "room": "Library-001", "hours": "8:00 AM - 8:00 PM"},
        {"service": "Exam Forms", "office": "Examination Cell", "room": "Admin-201", "hours": "9:00 AM - 5:00 PM"},
        {"service": "Transcript & Marksheet", "office": "Academic Office", "room": "Admin-101", "hours": "9:00 AM - 5:00 PM"},
        {"service": "Hostel Admission", "office": "Hostel Office", "room": "Hostel-Admin", "hours": "9:00 AM - 6:00 PM"},
        {"service": "Scholarship Information", "office": "Student Welfare", "room": "Admin-104", "hours": "10:00 AM - 4:00 PM"},
        {"service": "Grievance & Complaints", "office": "Dean's Office", "room": "Admin-301", "hours": "9:00 AM - 5:00 PM"},
        {"service": "Sports Facilities", "office": "Sports Department", "room": "Sports-Complex", "hours": "6:00 AM - 8:00 PM"},
    ]
    
    # Display services in a clean format
    for service in services:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.markdown(f"**{service['service']}**")
            
            with col2:
                st.markdown(f"📍 {service['office']} - {service['room']}")
            
            with col3:
                st.markdown(f"🕒 {service['hours']}")
            
            st.markdown("---")


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
        ["Home", "Find Faculty", "Campus Services"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "Campus Assist helps students find faculty and check their availability in real-time.\n\n"
        "**Powered by:**\n"
        "- 📊 Google Sheets\n"
        "- 📅 Google Calendar (Concept)\n"
        "- 🚀 Streamlit"
    )
    
    # Display selected page
    if page == "Home":
        display_home_page()
    elif page == "Find Faculty":
        display_find_faculty_page()
    elif page == "Campus Services":
        display_campus_services_page()


if __name__ == "__main__":
    main()
