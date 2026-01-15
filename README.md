# Campus Assist - Web Application

## 🎓 Project Overview

**Campus Assist** is a web-based smart campus helper designed for the **GDG Campus Hackathon**. It helps students find faculty members, check their real-time availability, and locate campus services efficiently.

### 🌟 Key Features

- **🔍 Smart Faculty Search** - Search by name, department, subject, role, or room number
- **⏰ Real-time Availability** - Check if faculty are currently available or in class
- **📊 Live Data Sync** - All data fetched from Google Sheets in real-time
- **📅 Google Calendar Concept** - Availability based on teaching schedules (Google Calendar logic)
- **🏢 Campus Services** - Directory of campus offices and their locations

---

## 🚀 Google Technology Integration

This project demonstrates the use of **Google technologies** as required for the GDG Campus Hackathon:

### 1. **Google Sheets as Live Backend**
- Faculty data stored in Google Sheets
- Timetable/schedule data in separate Google Sheet
- No hardcoded data - everything synced live
- Easy to update by campus administrators
- Collaborative editing capabilities

### 2. **Google Calendar Concept**
- Faculty availability determined using Google Calendar-based logic
- Teaching schedules represent calendar events
- In production, would integrate with Google Calendar API
- Current implementation simulates real-time calendar checking

**Google Sheets Used:**
- **Faculty Data Sheet**: Contains Name, Department, Subject, Role, Room
- **Timetable Sheet**: Contains Name, Day, Start, End (teaching schedules)

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (to fetch data from Google Sheets)

---

## 🛠️ Local Setup & Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/0Ketan/Beyonders-Project
cd Beyonders-Project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and CSV parsing

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if not already done)
2. **Push your code** to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Campus Assist web app"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Select** your repository: `Beyonders-Project`
5. **Set** main file path: `app.py`
6. **Click** "Deploy"

### Step 3: Get Your Live URL

After deployment (usually takes 2-3 minutes), you'll receive a public URL like:
```
https://your-app-name.streamlit.app
```

**Share this URL for your hackathon demo!**

---

## 📊 Google Sheets Configuration

The application uses two Google Sheets as the data source:

### Faculty Data Sheet
**URL:** [Faculty Data](https://docs.google.com/spreadsheets/d/16xBC5BLVAxGS1wSs8yoYNOEGQs8NtlUjgvZl5O1rZtA/edit#gid=0)

**Structure:**
| Name | Department | Subject | Role | Room |
|------|------------|---------|------|------|
| Dr. Rajesh Kumar | Computer Science | Database Management Systems (DBMS) | HOD | CS-201 |
| Prof. Priya Sharma | Electronics | Digital Signal Processing | Professor | EC-105 |

### Timetable Sheet
**URL:** [Faculty Timetable](https://docs.google.com/spreadsheets/d/1lQoalBwyKMYG0qlUj7BT_nNbPXuNrFfW7BFkzaY-r58/edit#gid=0)

**Structure:**
| Name | Day | Start | End |
|------|-----|-------|-----|
| Dr. Rajesh Kumar | Monday | 09:00 | 10:30 |
| Dr. Rajesh Kumar | Monday | 14:00 | 15:30 |

### How to Update Data

1. **Open the Google Sheet** (must have edit access)
2. **Edit the data** directly in the sheet
3. **Save** (auto-saves in Google Sheets)
4. **Refresh the web app** - data will update automatically (cached for 5 minutes)

### Creating Your Own Sheets

If you want to use your own Google Sheets:

1. **Create a new Google Sheet**
2. **Add the columns** as shown above
3. **Fill in your data**
4. **Set sharing** to "Anyone with the link → Viewer"
5. **Get the CSV export URL**:
   - Format: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv`
   - Replace `<SHEET_ID>` with your sheet's ID (from the URL)
6. **Update** the URLs in `app.py`:
   ```python
   FACULTY_SHEET_URL = "your-faculty-sheet-csv-url"
   TIMETABLE_SHEET_URL = "your-timetable-sheet-csv-url"
   ```

---

## 🎯 How to Use the Application

### 1. **Home Page**
- Overview of the application
- Explanation of Google technology integration
- Navigation instructions

### 2. **Find Faculty**
- **Search Bar**: Type any keyword (name, department, subject, role, room)
  - Example: "Computer Science" → finds all CS faculty
  - Example: "DBMS" → finds faculty teaching DBMS
  - Example: "HOD" → finds department heads
  - Example: "CS-201" → finds faculty in that room
- **Search Results**: Click "View Details" on any faculty
- **Faculty Details**: See complete information and current availability
- **Availability Status**:
  - ✅ Available (Based on Google Calendar)
  - 🔴 In Class (09:00 - 10:30) (Based on Google Calendar)

### 3. **Campus Services**
- Browse campus offices and services
- Find room locations and working hours

---

## 🏗️ Project Structure

```
Beyonders-Project/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                # This file
│
├── data/                    # Original JSON data (legacy)
│   ├── faculty.json
│   ├── timetable.json
│   └── offices.json
│
├── logic/                   # Original availability logic (legacy)
│   └── availability.py
│
└── ui/                      # Original Tkinter UI (legacy)
    └── app.py
```

**Note:** The `data/`, `logic/`, and `ui/` folders contain the original Tkinter desktop application code. The new web application is entirely in `app.py`.

---

## 🔧 Technical Details

### Technologies Used
- **Frontend/Backend**: Streamlit (Python web framework)
- **Data Source**: Google Sheets (via CSV export)
- **Data Processing**: Pandas
- **Deployment**: Streamlit Community Cloud

### How It Works

1. **Data Loading**:
   - App fetches CSV data from Google Sheets URLs
   - Data is cached for 5 minutes to reduce API calls
   - Pandas parses CSV into DataFrames

2. **Search Functionality**:
   - Case-insensitive partial matching
   - Searches across all fields: Name, Department, Subject, Role, Room
   - Real-time filtering as you type

3. **Availability Logic** (Google Calendar Concept):
   - Gets current day and time
   - Matches faculty name in timetable
   - Checks if current time falls within any teaching slot
   - Returns availability status with Google Calendar reference

4. **UI/UX**:
   - Sidebar navigation between pages
   - Responsive layout with Streamlit columns
   - Session state for selected faculty
   - Clean, intuitive interface

---

## 📱 Demo & Screenshots

### Live Demo
**URL:** [Your deployed Streamlit app URL here]

### Screenshots
*(Add screenshots after deployment)*

---

## 🎓 GDG Campus Hackathon Compliance

### Google Technology Usage ✅

1. **Google Sheets**:
   - ✅ Used as primary data source
   - ✅ Live data fetching (not hardcoded)
   - ✅ Demonstrates cloud-based data management

2. **Google Calendar Concept**:
   - ✅ Availability logic based on calendar events
   - ✅ Teaching schedules represent calendar entries
   - ✅ Clear documentation of Google Calendar integration approach
   - ✅ Production-ready architecture (can be extended with Calendar API)

### Problem Solved
- **Real Campus Problem**: Students struggle to find faculty and know when they're available
- **Solution**: Centralized, searchable directory with real-time availability
- **Impact**: Saves time, reduces confusion, improves campus navigation

---

## 🚀 Future Enhancements

1. **Google Calendar API Integration**
   - Real-time sync with faculty Google Calendars
   - Automatic availability updates
   - Meeting scheduling

2. **Additional Google Services**
   - Google Maps integration for campus navigation
   - Google Forms for feedback collection
   - Google Drive for document storage

3. **Enhanced Features**
   - Email notifications (Gmail API)
   - Appointment booking system
   - Mobile-responsive design improvements
   - Faculty contact information

---

## 👥 Target Users

- **Students**: Find faculty and check availability
- **New Students**: Navigate campus during orientation
- **Faculty**: Share their schedules and availability
- **Administrators**: Manage campus information centrally

---

## 📝 License

This project is open-source and available for educational use.

---

## 🤝 Contributing

This is a hackathon project. Feel free to fork and enhance it for your campus!

---

## 📧 Contact

For questions or feedback about this project, please reach out through the hackathon platform.

---

**Built with ❤️ for the GDG Campus Hackathon**

*Powered by Google Sheets, Google Calendar Concept, and Streamlit*
