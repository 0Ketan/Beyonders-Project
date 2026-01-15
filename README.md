# Campus Assist
### ATLAS – GDG on Campus Hackathon

## 1. Project Overview

Campus Assist is a live, deployed web application designed to solve the everyday challenges of navigating a large university campus. Built as a practical Minimum Viable Product (MVP) for the ATLAS – GDG on Campus Hackathon, this project helps students efficiently find faculty based on real-time availability, locate campus services, and get instant answers to campus-related queries via an AI assistant. It integrates directly with Google's ecosystem to provide a scalable, low-maintenance solution for real-world campus use.

## 2. Problem Statement

Navigating specialized university resources is often inefficient. Common friction points include:

*   **Difficulty Finding Faculty:** Students waste valuable time walking to offices only to find faculty members are unavailable or in class.
*   **Decentralized Information:** Critical information about labs, services, and policies is often scattered or outdated.
*   **Lack of Immediate Assistance:** New students frequently struggle to find answers to simple administrative questions without queuing at help desks.
*   **Operational Inefficiency:** Manual directory updates are slow and often result in stale data.

## 3. Solution Overview

Campus Assist streamlines campus operations by providing a unified, search-first interface. Instead of static lists, it uses a real-time data-driven approach. Faculty availability is checked live against teaching schedules, directories are synced instantly from administrative spreadsheets, and a Generative AI assistant provides 24/7 guidance, ensuring students always have the most accurate information.

## 4. Key Features

*   **Find Faculty with LIVE Availability:** Search for faculty and instantly see if they are "Available" or "In Class," powered by real-time Google Calendar checks.
*   **Ask Campus Assist (AI):** A smart, conversational assistant powered by Google Gemini that answers questions about faculty roles, campus services, and general procedures.
*   **Campus Services Directory:** A searchable database of administrative offices and student support services.
*   **Labs Directory:** Comprehensive listings of university laboratories, organized by building and department.
*   **Live Data Sync:** All directory data is fetched live from Google Sheets, allowing for instant updates without code changes.

## 5. Google Technologies Used

This project heavily leverages the Google ecosystem to create a robust, scalable architecture:

*   **Google Gemini (Generative AI):** Powers the "Ask Campus Assist" smart helper, utilizing the Gemini Pro model to understand and answer natural language student queries.
*   **Google Calendar:** Serves as the real-time engine for faculty availability. The app queries a public calendar to identify teaching slots and dynamically update status.
*   **Google Sheets:** Acts as the live backend database for faculty, services, and lab records, enabling non-technical staff to manage data easily.
*   **Streamlit Cloud:** Provides the hosting and deployment platform, ensuring the application is accessible live on the web.

## 6. Architecture Overview

The system architecture prioritizes simplicity, maintainability, and real-time performance:

1.  **Frontend:** Streamlit (Python) provides a responsive, mobile-friendly user interface.
2.  **AI Layer:** Google Gemini API processes natural language queries for the student assistant.
3.  **Data Layer:** Google Sheets functions as a structured relational database for all directory information.
4.  **Logic Layer:** The application integrates with the Google Calendar API to compute real-time availability status based on current time and event schedules.
5.  **Deployment:** The solution is fully deployed on Streamlit Cloud for instant accessibility.

## 7. Live Demo

**Access the live application here:**

[**https://0ketan-beyonders-project-app-bezivc.streamlit.app/**](https://0ketan-beyonders-project-app-bezivc.streamlit.app/)

We encourage judges to try searching for a faculty member or asking the AI assistant a question about the campus.

## 8. Environment Variables & Security

To maintain security, no sensitive keys are hardcoded in the application. The system requires the following environment variable:

*   `GEMINI_API_KEY`: Required to authenticate with the Google Gemini API.

This key is stored securely in the Streamlit Cloud "Secrets" management system for the production deployment.

## 9. How to Run Locally

To run this project on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/0Ketan/Beyonders-Project
    cd Beyonders-Project
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variable:**
    On Windows (PowerShell):
    ```powershell
    $env:GEMINI_API_KEY="your-google-gemini-api-key"
    ```
    On Mac/Linux:
    ```bash
    export GEMINI_API_KEY="your-google-gemini-api-key"
    ```

4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

## 10. Future Improvements

We have a strategic roadmap to evolve Campus Assist into a comprehensive institutional platform:

*   **Interactive Campus Map Integration:** Integrate a visual map to guide students directly to specific rooms and buildings.
*   **Holiday & Academic Calendar Awareness:** Enhance availability logic to automatically account for university holidays and exam schedules.
*   **Production-Ready Data Integration:** Collaborating with university administration to connect directly with official institutional databases for automated sync.
*   **Advanced AI Guidance:** Expand the AI assistant's capabilities to handle personalized academic queries and schedule planning.
*   **UI/UX Enhancements:** Refine the interface for an even more seamless mobile experience.

---

**Team Beyonders**
Built for the ATLAS – GDG on Campus Hackathon
