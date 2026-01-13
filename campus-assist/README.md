# Campus Assist

## 📋 Project Description

**Campus Assist** is a desktop application designed to help students navigate campus life more efficiently. Built as a hackathon prototype, this application provides quick access to faculty information, real-time availability status, and campus service locations.

Students can easily find out:
- Which faculty members are currently available or in class
- Where to go for specific administrative tasks (bonafide certificates, fee payments, ID cards, etc.)
- Faculty office locations and department information

## ✨ Features

### 1. **Find Faculty**
- Search and select faculty members from a dropdown menu
- View faculty details including:
  - Name and Department
  - Room/Office number
  - Real-time availability status
- Availability is determined based on current day and time against teaching schedules
- Clear visual indicators showing if faculty is available or currently in class

### 2. **Campus Services**
- Browse a comprehensive list of campus services
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

### 3. **User-Friendly Interface**
- Clean and intuitive Tkinter-based GUI
- Easy navigation between screens
- Color-coded availability status
- Responsive design elements

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
campus-assist/
│
├── data/
│   ├── faculty.json          # Faculty information
│   ├── timetable.json         # Teaching schedules
│   └── offices.json           # Campus services data
│
├── logic/
│   └── availability.py        # Availability checking logic
│
├── ui/
│   └── app.py                 # Main application UI
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
   cd campus-assist
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
   - Click **"Find Faculty"** to check faculty availability
   - Click **"Campus Services"** to browse campus offices
   - Click **"Exit"** to close the application

## 📊 Sample Data

The application comes pre-loaded with sample data:
- **8 Faculty Members** across different departments (CS, Electronics, Mathematics, Physics, Chemistry, Mechanical, Civil)
- **Teaching Schedules** for each faculty member
- **10 Campus Services** with office locations and working hours

You can modify the JSON files in the `data/` folder to customize the information for your campus.

## 🎯 Future Improvements

This is a hackathon prototype with potential for expansion:

1. **Mobile Application**
   - Develop Android/iOS versions using frameworks like Kivy or React Native
   - Add push notifications for faculty availability changes

2. **Enhanced Features**
   - Add faculty contact information (email, phone)
   - Include campus maps with visual navigation
   - Implement search functionality
   - Add student feedback/rating system

3. **Data Management**
   - Admin panel to update faculty and service information
   - Database integration (SQLite/MySQL)
   - Import/export functionality for bulk updates

4. **Advanced Availability**
   - Integration with faculty calendar systems
   - Real-time updates via cloud sync
   - Appointment booking system

5. **Additional Modules**
   - Event calendar for campus activities
   - Bus/transport schedules
   - Canteen menu and timings
   - Emergency contacts directory

## 👥 Target Users

- **Students**: Primary users looking for faculty and campus services
- **New Students**: Especially helpful during orientation
- **Parents/Visitors**: Can use during campus visits

## 🤝 Contributing

This is a hackathon project built for educational purposes. Feel free to fork and enhance it for your own campus!

## 📝 License

This project is open-source and available for educational use.

---

**Built with ❤️ for the Hackathon**

*Making campus navigation easier, one click at a time!*
