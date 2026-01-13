# Campus Assist

## 📋 Project Description

**Campus Assist** is a desktop application designed to help students navigate campus life more efficiently. Built as a hackathon prototype, this application provides quick access to faculty information, real-time availability status, and campus service locations with an advanced search-based discovery system.

Students can easily:
- **Search for faculty** by name, department, subject, role, or room number
- Check which faculty members are currently available or in class
- Find where to go for specific administrative tasks (bonafide certificates, fee payments, ID cards, etc.)
- Get helpful tips based on why they're looking for faculty

## ✨ Features

### 1. **Smart Faculty Search**
- **Advanced Search Bar**: Search by name, department, subject, role, or room
  - Example: Type "DBMS" → finds Database faculty
  - Example: Type "HOD" → finds department heads
  - Example: Type "CS-201" → finds faculty in that room
- **Live Filtering**: Results update as you type (case-insensitive, partial matching)
- **Search Results Display**: Shows Name | Department | Role for easy identification
- **Enhanced Faculty Data**: Each faculty includes:
  - Name and Department
  - Subject taught (e.g., DBMS, AI, Thermodynamics)
  - Role/Post (e.g., HOD, Lab Incharge, Project Coordinator)
  - Room/Office number
  - Real-time availability status
- **Purpose Buttons**: Quick-access buttons for common needs:
  - Subject Doubt
  - Internship Approval
  - Project Guidance
  - Administrative Work
  - Each provides helpful tips when clicked

### 2. **Campus Services Directory**
- Browse a comprehensive list of 10 campus services
- View detailed information for each service:
  - Office name
  - Room location
  - Working hours
- Services include:
  - Bonafide Certificate
  - Fee Payment & Issues
  - ID Card
  - Library Card
  - Exam Forms
  - Transcript & Marksheet
  - Hostel Admission
  - Scholarship Information
  - Grievance & Complaints
  - Sports Facilities

### 3. **Professional User Interface**
- **Resizable Window**: 900x600 default, fully resizable (minimum 800x500)
- **Frame-Based Navigation**: Smooth transitions between screens
- **Back to Home Buttons**: Easy navigation from all screens
- **Mouse Wheel Scrolling**: Natural scrolling on all lists and panels
  - Works on Windows and Linux
  - Hover and scroll - no clicking needed
- **Responsive Layout**: Adapts to window resizing
- **Color-Coded Status**: Green for available, red for unavailable
- **Scrollable Content**: All long content areas support scrolling

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter (built-in with Python)
- **Data Storage**: JSON files (local storage)
- **Libraries Used**:
  - `tkinter` - GUI development
  - `json` - Data handling
  - `datetime` - Time-based availability checking

## 📁 Project Structure

```
Beyonders-Project/
│
├── data/
│   ├── faculty.json          # Faculty information with subjects and roles
│   ├── timetable.json         # Teaching schedules
│   └── offices.json           # Campus services data
│
├── logic/
│   └── availability.py        # Availability checking logic
│
├── ui/
│   └── app.py                 # Main application UI with search feature
│
└── README.md                  # Project documentation
```

## 🚀 How to Run the Application

### Prerequisites
- Python 3.6 or higher installed on your system
- Tkinter (usually comes pre-installed with Python)

### Steps to Run

1. **Navigate to the project directory**:
   ```bash
   cd Beyonders-Project
   ```

2. **Run the application**:
   ```bash
   python ui/app.py
   ```
   
   Or on some systems:
   ```bash
   python3 ui/app.py
   ```

3. **Using the Application**:
   - The main menu will appear with three options
   - Click **"Find Faculty"** to search for faculty and check availability
   - Click **"Campus Services"** to browse campus offices
   - Click **"Exit"** to close the application

### Using the Search Feature

1. **Search Faculty**:
   - Type in the search bar (e.g., "Computer", "DBMS", "HOD", "204")
   - Results filter automatically as you type
   - Click on any result to view full details

2. **Purpose Buttons**:
   - Click a purpose button to get helpful tips
   - Check faculty availability below

3. **Mouse Scrolling**:
   - Hover over any list or panel
   - Scroll with your mouse wheel naturally

## 📊 Sample Data

The application comes pre-loaded with sample data:
- **8 Faculty Members** across different departments (CS, Electronics, Mathematics, Physics, Chemistry, Mechanical, Civil)
- **Enhanced Faculty Data**: Each includes subject taught and role/post
- **Teaching Schedules** for each faculty member
- **10 Campus Services** with office locations and working hours

You can modify the JSON files in the `data/` folder to customize the information for your campus.

## 🎯 Key Improvements

### Implemented Features
✅ **Search-Based Discovery**: Find faculty by multiple criteria
✅ **Live Filtering**: Real-time search results
✅ **Enhanced Data**: Subject and role fields for all faculty
✅ **Purpose Buttons**: Contextual help for students
✅ **Resizable Window**: Professional, flexible UI
✅ **Mouse Wheel Scrolling**: Natural scrolling on all scrollable areas
✅ **Frame-Based Navigation**: Smooth screen transitions
✅ **Responsive Layout**: Adapts to window size

### Future Enhancements

1. **Mobile Application**
   - Develop Android/iOS versions using frameworks like Kivy or React Native
   - Add push notifications for faculty availability changes

2. **Advanced Features**
   - Add faculty contact information (email, phone)
   - Include campus maps with visual navigation
   - Add student feedback/rating system
   - Appointment booking system

3. **Data Management**
   - Admin panel to update faculty and service information
   - Database integration (SQLite/MySQL)
   - Import/export functionality for bulk updates

4. **Additional Modules**
   - Event calendar for campus activities
   - Bus/transport schedules
   - Canteen menu and timings
   - Emergency contacts directory

## 👥 Target Users

- **Students**: Primary users looking for faculty and campus services
- **New Students**: Especially helpful during orientation
- **Parents/Visitors**: Can use during campus visits

## 🎓 Why This Design?

### Realistic User Scenario
Students often don't remember exact faculty names but remember:
- "The HOD of CSE department"
- "The professor who teaches DBMS"
- "The faculty in room 204"
- "The internship coordinator"

### User Experience Benefits
1. **Faster Discovery**: Type what you remember instead of scrolling
2. **Multiple Entry Points**: Search by any field
3. **Contextual Help**: Purpose buttons provide guidance
4. **Professional Feel**: Smooth scrolling and responsive design

## 🤝 Contributing

This is a hackathon project built for educational purposes. Feel free to fork and enhance it for your own campus!

## 📝 License

This project is open-source and available for educational use.

---

**Built with ❤️ for the Beyonders Hackathon**

*Making campus navigation easier, one search at a time!*
