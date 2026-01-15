# Campus Assist

## 1. Project Overview

Campus Assist is a centralized, web-based platform designed to assist university students in navigating campus resources efficiently. Built for the ATLAS – GDG on Campus Hackathon, this open innovation project simplifies the daily interactions between students and the complex university ecosystem, ensuring that essential information regarding faculty, services, and facilities is accessible in real-time.

## 2. Problem Statement

Navigating a large university campus allows for significant friction and inefficiency. Common challenges faced by students include:

*   **Difficulty Finding Faculty:** Students often struggle to locate faculty members or determine if they are currently in their offices, leading to wasted time walking across campus.
*   **Uncertain Availability:** Static timetables are often outdated or hard to interpret quickly, resulting in students waiting for faculty who are in class or unavailable.
*   **Campus Confusion:** New students frequently face confusion when trying to locate administrative services, labs, or specific departments.
*   **Inefficiency:** The lack of a centralized information system leads to unnecessary delays in academic and administrative processes.

## 3. Solution Overview

Campus Assist solves these problems by providing a unified, search-based interface for campus information. It moves away from static, decentralized lists and offers a data-driven approach where information is queried in real-time. By integrating directly with live data sources, the application ensures that students have access to the most current information available regarding faculty locations, schedules, and campus services.

## 4. Key Features

*   **Find Faculty with Real-Time Availability:** Search for faculty members by name, department, or subject. View their current status (Available / In Class) based on live schedule data.
*   **Campus Services Directory:** A searchable directory of administrative offices and student services, including location details and descriptions.
*   **Labs Directory:** Easy access to information about various university laboratories, organized by department and building.
*   **Multi-Field Search:** Powerful search filters allow users to query across names, roles, room numbers, and descriptions.
*   **Live Data Updates:** The system is connected to live cloud-based data sheets, ensuring that any administrative updates are immediately reflected in the application.

## 5. Google Technologies Used

This project leverages the Google ecosystem to create a scalable, low-maintenance, and highly accessible solution:

*   **Google Sheets:** Utilized as the primary backend database for storing faculty directories, service listings, and lab information. This allows non-technical campus staff to easily update records without needing to redeploy the application.
*   **Google Calendar:** Integrated to determine real-time faculty availability. The application queries a shared Google Calendar to identify teaching schedules and events, dynamically updating the status shown to students.
*   **Streamlit Cloud:** Used for hosting and deploying the application, providing a fast and reliable web interface accessible from any device.

## 6. Architecture Overview

The architecture of Campus Assist is designed for simplicity and maintainability:

1.  **Frontend:** Built with Streamlit (Python), providing a responsive and user-friendly web interface.
2.  **Data Layer:** Google Sheets acts as a structured relational database, hosting the core datasets for faculty, services, and labs.
3.  **Logic Layer:** The Python application fetches data using the Pandas library and interacts with the Google Calendar API to process time-based logic for availability.
4.  **Deployment:** The application runs in a containerized environment on Streamlit Cloud, ensuring continuous availability.

## 7. Live Demo

You can access the live version of Campus Assist here:

**https://0ketan-beyonders-project-app-bezivc.streamlit.app/**

We encourage judges to try searching for faculty names or campus services to experience the real-time filtering capabilities.

## 8. How to Run Locally

To run this project on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/0Ketan/Beyonders-Project
    cd Beyonders-Project
    ```

2.  **Install Dependencies:**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

4.  **Access the App:**
    Open your browser and navigate to `http://localhost:8501`.

## 9. Real-World Impact

Campus Assist offers immediate and tangible benefits to the university community:

*   **Saves Student Time:** Reduces the time spent physically checking for faculty availability or finding offices.
*   **Reduces Confusion:** Provides a single source of truth for campus locations, particularly helping freshers settle in faster.
*   **Scalable Solution:** The architecture can be easily adapted to other campuses or institutions with minimal configuration changes.

Estimates suggest that a centralized system like this could save a student body hundreds of collective hours per semester in reduced transit and wait times.

## 10. Future Improvements

We have a clear roadmap to evolve Campus Assist from a prototype into a comprehensive institutional tool:

*   **Interactive Campus Map Integration:** Integrate an interactive campus map to guide students directly to faculty rooms, labs, and service offices, improving navigation and reducing on-campus confusion.
*   **Holiday & Academic Calendar Awareness:** Enhance availability logic by integrating academic calendars so the system automatically reflects holidays, events, and non-working days.
*   **Production-Ready Institutional Data Integration:** Collaborate with campus administration to connect the app with official data sources, enabling real-time updates and real-world deployment beyond a prototype.
*   **AI-Powered Student Assistant:** Introduce an AI assistant to help students with common academic and administrative queries, improving accessibility and user experience.
*   **Enhanced UI & UX:** Further improve the user interface and interaction design to make the application more intuitive and mobile-friendly.

## 11. Team & Acknowledgements

**Team Beyonders**

*   Ketan (Lead Developer)
*   Student Contributors

**Acknowledgements**

We would like to thank the organizers of the ATLAS – GDG on Campus Hackathon and the Google Developer Groups community for providing the platform and tools to build this solution.
