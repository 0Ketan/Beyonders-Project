"""
Campus Assist - Main Application
A desktop application to help students find faculty and campus services.
REFACTORED VERSION with frame-based navigation and responsive layout.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add parent directory to path to import logic module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.availability import (
    load_json_file,
    check_faculty_availability,
    get_faculty_by_name
)


class CampusAssistApp:
    """Main application class for Campus Assist with frame-based navigation"""
    
    def __init__(self, root):
        """
        Initialize the application with frame-based architecture.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Campus Assist")
        
        # Configure window to be resizable
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Load data files
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.faculty_data = load_json_file(os.path.join(self.data_path, 'faculty.json'))
        self.timetable_data = load_json_file(os.path.join(self.data_path, 'timetable.json'))
        self.offices_data = load_json_file(os.path.join(self.data_path, 'offices.json'))
        
        # Create main container for all frames
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold all frames
        self.frames = {}
        
        # Create all frames
        self.create_frames()
        
        # Show home frame initially
        self.show_frame("HomeFrame")
    
    def create_frames(self):
        """Create all application frames and stack them in the container"""
        # Create Home Frame
        self.frames["HomeFrame"] = self.create_home_frame()
        
        # Create Find Faculty Frame
        self.frames["FindFacultyFrame"] = self.create_find_faculty_frame()
        
        # Create Services Frame
        self.frames["ServicesFrame"] = self.create_services_frame()
        
        # Stack all frames in the same location
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """
        Show the specified frame by raising it to the front.
        
        Args:
            frame_name (str): Name of the frame to show
        """
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def bind_mousewheel(self, widget, canvas):
        """
        Bind mouse wheel scrolling to a canvas widget.
        
        This enables natural scrolling behavior when the mouse is over a scrollable area.
        Supports both Windows and Linux platforms.
        
        Args:
            widget: The widget to bind mouse enter/leave events to
            canvas: The canvas widget that should scroll
        """
        def on_mousewheel(event):
            """Handle mouse wheel scrolling for Windows"""
            # Windows: event.delta is +/- 120 per scroll notch
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_mousewheel_linux_up(event):
            """Handle mouse wheel scroll up for Linux"""
            canvas.yview_scroll(-1, "units")
        
        def on_mousewheel_linux_down(event):
            """Handle mouse wheel scroll down for Linux"""
            canvas.yview_scroll(1, "units")
        
        def bind_wheel(event):
            """Bind scrolling when mouse enters the widget"""
            # Windows
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            # Linux
            canvas.bind_all("<Button-4>", on_mousewheel_linux_up)
            canvas.bind_all("<Button-5>", on_mousewheel_linux_down)
        
        def unbind_wheel(event):
            """Unbind scrolling when mouse leaves the widget"""
            # Windows
            canvas.unbind_all("<MouseWheel>")
            # Linux
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        
        # Bind enter/leave events to the widget
        widget.bind("<Enter>", bind_wheel)
        widget.bind("<Leave>", unbind_wheel)
    
    def create_home_frame(self):
        """Create and return the home screen frame"""
        frame = tk.Frame(self.container, bg=self.bg_color)
        
        # Configure grid for centering
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(
            frame,
            text="Campus Assist",
            font=("Arial", 32, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.grid(row=0, column=0, pady=(50, 10), sticky="s")
        
        # Subtitle
        subtitle_label = tk.Label(
            frame,
            text="Your Campus Navigation Helper",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Button container
        button_frame = tk.Frame(frame, bg=self.bg_color)
        button_frame.grid(row=2, column=0, pady=20)
        
        # Find Faculty button
        faculty_btn = tk.Button(
            button_frame,
            text="Find Faculty",
            font=("Arial", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            width=25,
            height=2,
            command=lambda: self.show_frame("FindFacultyFrame"),
            cursor="hand2"
        )
        faculty_btn.pack(pady=12)
        
        # Campus Services button
        services_btn = tk.Button(
            button_frame,
            text="Campus Services",
            font=("Arial", 14, "bold"),
            bg=self.secondary_color,
            fg="white",
            width=25,
            height=2,
            command=lambda: self.show_frame("ServicesFrame"),
            cursor="hand2"
        )
        services_btn.pack(pady=12)
        
        # Exit button
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 14),
            bg="#f44336",
            fg="white",
            width=25,
            height=2,
            command=self.root.quit,
            cursor="hand2"
        )
        exit_btn.pack(pady=12)
        
        return frame
    
    def create_find_faculty_frame(self):
        """Create and return the Find Faculty screen frame with search functionality"""
        frame = tk.Frame(self.container, bg=self.bg_color)
        
        # Configure grid for responsive layout
        frame.grid_rowconfigure(0, weight=0)  # Title
        frame.grid_rowconfigure(1, weight=0)  # Search bar
        frame.grid_rowconfigure(2, weight=0)  # Purpose buttons
        frame.grid_rowconfigure(3, weight=1)  # Content area (expandable)
        frame.grid_rowconfigure(4, weight=0)  # Back button
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(
            frame,
            text="Find Faculty",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.grid(row=0, column=0, pady=(25, 15), sticky="n")
        
        # Search area
        search_frame = tk.Frame(frame, bg=self.bg_color)
        search_frame.grid(row=1, column=0, pady=10, padx=50, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search label
        search_label = tk.Label(
            search_frame,
            text="Search Faculty:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        search_label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # Search entry with placeholder
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)  # Live search
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            width=50
        )
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        # Placeholder text
        search_entry.insert(0, "Search by name, department, subject, role, or room...")
        search_entry.config(fg='#999999')
        
        # Placeholder behavior
        def on_entry_click(event):
            if search_entry.get() == "Search by name, department, subject, role, or room...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=self.text_color)
        
        def on_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Search by name, department, subject, role, or room...")
                search_entry.config(fg='#999999')
        
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Clear button
        clear_btn = tk.Button(
            search_frame,
            text="Clear",
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            command=self.clear_search,
            cursor="hand2",
            padx=10
        )
        clear_btn.grid(row=0, column=2)
        
        # Purpose section - "Why are you looking for this faculty?"
        purpose_frame = tk.Frame(frame, bg=self.bg_color)
        purpose_frame.grid(row=2, column=0, pady=10, padx=50, sticky="ew")
        
        purpose_label = tk.Label(
            purpose_frame,
            text="Why are you looking for faculty?",
            font=("Arial", 11, "italic"),
            bg=self.bg_color,
            fg=self.text_color
        )
        purpose_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Purpose buttons
        purposes = [
            ("Subject Doubt", "#2196F3"),
            ("Internship Approval", "#FF9800"),
            ("Project Guidance", "#9C27B0"),
            ("Administrative Work", "#607D8B")
        ]
        
        for purpose, color in purposes:
            btn = tk.Button(
                purpose_frame,
                text=purpose,
                font=("Arial", 9),
                bg=color,
                fg="white",
                command=lambda p=purpose: self.show_purpose_message(p),
                cursor="hand2",
                padx=8,
                pady=3
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Main content area - two columns
        content_container = tk.Frame(frame, bg=self.bg_color)
        content_container.grid(row=3, column=0, pady=15, padx=50, sticky="nsew")
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=2)
        
        # Left side - Search results list
        left_frame = tk.Frame(content_container, bg=self.bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        results_label = tk.Label(
            left_frame,
            text="Search Results:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        results_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        
        # Results listbox with scrollbar
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.grid(row=1, column=0, sticky="nsew")
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)
        
        results_scrollbar = tk.Scrollbar(listbox_frame)
        results_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.results_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            yscrollcommand=results_scrollbar.set,
            activestyle="none",
            selectmode=tk.SINGLE,
            height=12
        )
        self.results_listbox.grid(row=0, column=0, sticky="nsew")
        results_scrollbar.config(command=self.results_listbox.yview)
        
        # Enable mouse wheel scrolling for results listbox
        def on_listbox_mousewheel(event):
            """Handle mouse wheel scrolling for the listbox"""
            self.results_listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_listbox_mousewheel_linux_up(event):
            self.results_listbox.yview_scroll(-1, "units")
        
        def on_listbox_mousewheel_linux_down(event):
            self.results_listbox.yview_scroll(1, "units")
        
        def bind_listbox_wheel(event):
            self.results_listbox.bind_all("<MouseWheel>", on_listbox_mousewheel)
            self.results_listbox.bind_all("<Button-4>", on_listbox_mousewheel_linux_up)
            self.results_listbox.bind_all("<Button-5>", on_listbox_mousewheel_linux_down)
        
        def unbind_listbox_wheel(event):
            self.results_listbox.unbind_all("<MouseWheel>")
            self.results_listbox.unbind_all("<Button-4>")
            self.results_listbox.unbind_all("<Button-5>")
        
        self.results_listbox.bind("<Enter>", bind_listbox_wheel)
        self.results_listbox.bind("<Leave>", unbind_listbox_wheel)
        
        # Bind selection event
        self.results_listbox.bind('<<ListboxSelect>>', self.on_faculty_select)
        
        # Populate with all faculty initially
        self.populate_search_results(self.faculty_data)
        
        # Right side - Faculty details (scrollable)
        right_frame = tk.Frame(content_container, bg=self.bg_color)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas for scrolling
        detail_canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
        detail_scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=detail_canvas.yview)
        
        # Faculty detail frame inside canvas
        self.faculty_detail_frame = tk.Frame(detail_canvas, bg="white", relief=tk.RIDGE, borderwidth=2)
        
        # Configure canvas
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        detail_canvas.grid(row=0, column=0, sticky="nsew")
        detail_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create window in canvas
        detail_canvas_frame = detail_canvas.create_window((0, 0), window=self.faculty_detail_frame, anchor="nw")
        
        # Update scroll region when frame size changes
        def configure_detail_scroll(event):
            detail_canvas.configure(scrollregion=detail_canvas.bbox("all"))
            detail_canvas.itemconfig(detail_canvas_frame, width=event.width)
        
        self.faculty_detail_frame.bind("<Configure>", configure_detail_scroll)
        detail_canvas.bind("<Configure>", configure_detail_scroll)
        
        # Enable mouse wheel scrolling for faculty details canvas
        self.bind_mousewheel(detail_canvas, detail_canvas)
        
        # Initial message
        initial_label = tk.Label(
            self.faculty_detail_frame,
            text="Search or select a faculty member to view details",
            font=("Arial", 12, "italic"),
            bg="white",
            fg="#999999",
            wraplength=400
        )
        initial_label.pack(pady=80)
        
        # Back to Home button
        back_btn = tk.Button(
            frame,
            text="← Back to Home",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            command=lambda: self.show_frame("HomeFrame"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        back_btn.grid(row=4, column=0, pady=15)
        
        return frame
    
    def search_faculty(self, query):
        """
        Search faculty by name, department, subject, role, or room.
        Returns list of matching faculty (case-insensitive partial match).
        """
        if not query or query == "Search by name, department, subject, role, or room...":
            return self.faculty_data
        
        query = query.lower().strip()
        results = []
        
        for faculty in self.faculty_data:
            # Check all searchable fields
            if (query in faculty['name'].lower() or
                query in faculty['department'].lower() or
                query in faculty['room'].lower() or
                query in faculty.get('subject', '').lower() or
                query in faculty.get('role', '').lower()):
                results.append(faculty)
        
        return results
    
    def on_search_change(self, *args):
        """Called when search text changes - performs live filtering"""
        query = self.search_var.get()
        
        # Don't search on placeholder text
        if query == "Search by name, department, subject, role, or room...":
            return
        
        # Get matching faculty
        matching_faculty = self.search_faculty(query)
        
        # Update results listbox
        self.populate_search_results(matching_faculty)
    
    def populate_search_results(self, faculty_list):
        """Populate the results listbox with faculty"""
        self.results_listbox.delete(0, tk.END)
        
        # Store faculty data for later retrieval
        self.current_results = faculty_list
        
        if not faculty_list:
            self.results_listbox.insert(tk.END, "No results found")
            return
        
        for faculty in faculty_list:
            # Display format: Name | Department | Role
            display_text = f"{faculty['name']} | {faculty['department']} | {faculty.get('role', 'N/A')}"
            self.results_listbox.insert(tk.END, display_text)
    
    def clear_search(self):
        """Clear search and show all faculty"""
        self.search_var.set("")
        self.populate_search_results(self.faculty_data)
        
        # Clear faculty details
        for widget in self.faculty_detail_frame.winfo_children():
            widget.destroy()
        
        initial_label = tk.Label(
            self.faculty_detail_frame,
            text="Search or select a faculty member to view details",
            font=("Arial", 12, "italic"),
            bg="white",
            fg="#999999",
            wraplength=400
        )
        initial_label.pack(pady=80)
    
    def on_faculty_select(self, event):
        """Called when a faculty is selected from search results"""
        selection = self.results_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # Check if "No results found" message
        if not hasattr(self, 'current_results') or not self.current_results:
            return
        
        if index >= len(self.current_results):
            return
        
        faculty = self.current_results[index]
        self.display_faculty_details(faculty)
    
    def show_purpose_message(self, purpose):
        """Show helpful message based on why user is looking for faculty"""
        messages = {
            "Subject Doubt": "💡 Tip: Faculty are usually available during non-teaching hours. Check availability below before visiting.",
            "Internship Approval": "📋 Note: For internship approvals, it's best to schedule an appointment. Check if faculty is available now.",
            "Project Guidance": "🎓 Suggestion: Prepare your questions beforehand. Faculty office hours are ideal for project discussions.",
            "Administrative Work": "📄 Info: For administrative tasks, ensure you have all required documents. Check faculty availability below."
        }
        
        message = messages.get(purpose, "Check faculty availability below.")
        messagebox.showinfo(f"{purpose}", message)
    
    def display_faculty_details(self, faculty):
        """Display detailed faculty information with availability"""
        # Clear previous details
        for widget in self.faculty_detail_frame.winfo_children():
            widget.destroy()
        
        # Check availability
        availability = check_faculty_availability(faculty['id'], self.timetable_data)
        
        # Title
        title_label = tk.Label(
            self.faculty_detail_frame,
            text="Faculty Details",
            font=("Arial", 18, "bold"),
            bg="white",
            fg=self.primary_color
        )
        title_label.pack(pady=(20, 15))
        
        # Info container
        info_container = tk.Frame(self.faculty_detail_frame, bg="white")
        info_container.pack(pady=10, padx=25, fill=tk.BOTH, expand=True)
        
        # Name
        name_label = tk.Label(
            info_container,
            text=f"Name: {faculty['name']}",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        name_label.pack(pady=8, anchor="w", fill=tk.X)
        
        # Department
        dept_label = tk.Label(
            info_container,
            text=f"Department: {faculty['department']}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        dept_label.pack(pady=6, anchor="w", fill=tk.X)
        
        # Subject
        subject_label = tk.Label(
            info_container,
            text=f"Subject: {faculty.get('subject', 'N/A')}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        subject_label.pack(pady=6, anchor="w", fill=tk.X)
        
        # Role
        role_label = tk.Label(
            info_container,
            text=f"Role: {faculty.get('role', 'N/A')}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        role_label.pack(pady=6, anchor="w", fill=tk.X)
        
        # Room
        room_label = tk.Label(
            info_container,
            text=f"Room: {faculty['room']}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        room_label.pack(pady=6, anchor="w", fill=tk.X)
        
        # Separator
        separator = tk.Frame(info_container, height=2, bg="#e0e0e0")
        separator.pack(fill=tk.X, pady=15)
        
        # Availability status
        status_color = "#4CAF50" if availability['available'] else "#f44336"
        status_text = "✓ AVAILABLE" if availability['available'] else "✗ NOT AVAILABLE"
        
        status_label = tk.Label(
            info_container,
            text=f"Status: {status_text}",
            font=("Arial", 15, "bold"),
            bg="white",
            fg=status_color,
            anchor="w",
            wraplength=450
        )
        status_label.pack(pady=10, anchor="w", fill=tk.X)
        
        # Additional availability info
        detail_label = tk.Label(
            info_container,
            text=availability['status'],
            font=("Arial", 11, "italic"),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=450
        )
        detail_label.pack(pady=6, anchor="w", fill=tk.X)
        
        # Bottom padding
        bottom_spacer = tk.Frame(self.faculty_detail_frame, bg="white", height=30)
        bottom_spacer.pack()
    
    def display_faculty_info(self):
        """Display faculty information and availability in the result frame"""
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        faculty_name = self.selected_faculty.get()
        
        # Validate selection
        if faculty_name == "-- Select a Faculty --":
            messagebox.showwarning("No Selection", "Please select a faculty member first!")
            return
        
        # Get faculty details
        faculty = get_faculty_by_name(faculty_name, self.faculty_data)
        
        if not faculty:
            messagebox.showerror("Error", "Faculty not found!")
            return
        
        # Check availability
        availability = check_faculty_availability(faculty['id'], self.timetable_data)
        
        # Display information with better spacing and visibility
        info_label = tk.Label(
            self.result_frame,
            text="Faculty Information",
            font=("Arial", 18, "bold"),
            bg="white",
            fg=self.primary_color
        )
        info_label.pack(pady=(25, 20))
        
        # Create info container for better layout
        info_container = tk.Frame(self.result_frame, bg="white")
        info_container.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        # Name
        name_label = tk.Label(
            info_container,
            text=f"Name: {faculty['name']}",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=600
        )
        name_label.pack(pady=10, anchor="w", padx=20, fill=tk.X)
        
        # Department
        dept_label = tk.Label(
            info_container,
            text=f"Department: {faculty['department']}",
            font=("Arial", 13),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=600
        )
        dept_label.pack(pady=8, anchor="w", padx=20, fill=tk.X)
        
        # Room
        room_label = tk.Label(
            info_container,
            text=f"Room Number: {faculty['room']}",
            font=("Arial", 13),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=600
        )
        room_label.pack(pady=8, anchor="w", padx=20, fill=tk.X)
        
        # Separator
        separator = tk.Frame(info_container, height=2, bg="#e0e0e0")
        separator.pack(fill=tk.X, pady=15, padx=20)
        
        # Availability status
        status_color = "#4CAF50" if availability['available'] else "#f44336"
        status_text = "✓ AVAILABLE" if availability['available'] else "✗ NOT AVAILABLE"
        
        status_label = tk.Label(
            info_container,
            text=f"Status: {status_text}",
            font=("Arial", 15, "bold"),
            bg="white",
            fg=status_color,
            anchor="w",
            wraplength=600
        )
        status_label.pack(pady=12, anchor="w", padx=20, fill=tk.X)
        
        # Additional info
        detail_label = tk.Label(
            info_container,
            text=availability['status'],
            font=("Arial", 12, "italic"),
            bg="white",
            fg=self.text_color,
            anchor="w",
            wraplength=600
        )
        detail_label.pack(pady=8, anchor="w", padx=20, fill=tk.X)
        
        # Add some bottom padding
        bottom_spacer = tk.Frame(self.result_frame, bg="white", height=30)
        bottom_spacer.pack()
    
    def create_services_frame(self):
        """Create and return the Campus Services screen frame"""
        frame = tk.Frame(self.container, bg=self.bg_color)
        
        # Configure grid for responsive layout
        frame.grid_rowconfigure(0, weight=0)  # Title
        frame.grid_rowconfigure(1, weight=1)  # Content area (expandable)
        frame.grid_rowconfigure(2, weight=0)  # Back button
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(
            frame,
            text="Campus Services",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.secondary_color
        )
        title_label.grid(row=0, column=0, pady=(30, 20), sticky="n")
        
        # Main content container
        content_container = tk.Frame(frame, bg=self.bg_color)
        content_container.grid(row=1, column=0, pady=10, padx=50, sticky="nsew")
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)
        
        # Left side - Service list
        left_frame = tk.Frame(content_container, bg=self.bg_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        list_label = tk.Label(
            left_frame,
            text="Select a Service:",
            font=("Arial", 13, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        list_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.grid(row=1, column=0, sticky="nsew")
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.services_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            activestyle="none",
            selectmode=tk.SINGLE
        )
        self.services_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.services_listbox.yview)
        
        # Enable mouse wheel scrolling for services listbox
        def on_services_mousewheel(event):
            """Handle mouse wheel scrolling for the services listbox"""
            self.services_listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_services_mousewheel_linux_up(event):
            self.services_listbox.yview_scroll(-1, "units")
        
        def on_services_mousewheel_linux_down(event):
            self.services_listbox.yview_scroll(1, "units")
        
        def bind_services_wheel(event):
            self.services_listbox.bind_all("<MouseWheel>", on_services_mousewheel)
            self.services_listbox.bind_all("<Button-4>", on_services_mousewheel_linux_up)
            self.services_listbox.bind_all("<Button-5>", on_services_mousewheel_linux_down)
        
        def unbind_services_wheel(event):
            self.services_listbox.unbind_all("<MouseWheel>")
            self.services_listbox.unbind_all("<Button-4>")
            self.services_listbox.unbind_all("<Button-5>")
        
        self.services_listbox.bind("<Enter>", bind_services_wheel)
        self.services_listbox.bind("<Leave>", unbind_services_wheel)
        
        # Populate listbox
        for office in self.offices_data:
            self.services_listbox.insert(tk.END, office['service'])
        
        # Bind selection event
        self.services_listbox.bind('<<ListboxSelect>>', self.display_service_info)
        
        # Right side - Service details (scrollable)
        right_frame = tk.Frame(content_container, bg=self.bg_color)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas for scrolling
        detail_canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
        detail_scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=detail_canvas.yview)
        
        # Service detail frame inside canvas
        self.service_detail_frame = tk.Frame(detail_canvas, bg="white", relief=tk.RIDGE, borderwidth=2)
        
        # Configure canvas
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        detail_canvas.grid(row=0, column=0, sticky="nsew")
        detail_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create window in canvas
        detail_canvas_frame = detail_canvas.create_window((0, 0), window=self.service_detail_frame, anchor="nw")
        
        # Update scroll region when frame size changes
        def configure_detail_scroll(event):
            detail_canvas.configure(scrollregion=detail_canvas.bbox("all"))
            # Make the frame width match canvas width
            detail_canvas.itemconfig(detail_canvas_frame, width=event.width)
        
        self.service_detail_frame.bind("<Configure>", configure_detail_scroll)
        detail_canvas.bind("<Configure>", configure_detail_scroll)
        
        # Enable mouse wheel scrolling for service details canvas
        self.bind_mousewheel(detail_canvas, detail_canvas)
        
        # Initial message
        initial_label = tk.Label(
            self.service_detail_frame,
            text="Select a service to view details",
            font=("Arial", 13, "italic"),
            bg="white",
            fg="#999999",
            wraplength=350
        )
        initial_label.pack(pady=80)
        
        # Back to Home button
        back_btn = tk.Button(
            frame,
            text="← Back to Home",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            command=lambda: self.show_frame("HomeFrame"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        back_btn.grid(row=2, column=0, pady=20)
        
        return frame
    
    def display_service_info(self, event):
        """Display selected service information in the detail panel"""
        # Clear previous details
        for widget in self.service_detail_frame.winfo_children():
            widget.destroy()
        
        # Get selected service
        selection = self.services_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        service_data = self.offices_data[index]
        
        # Display service details with better spacing
        title_label = tk.Label(
            self.service_detail_frame,
            text=service_data['service'],
            font=("Arial", 16, "bold"),
            bg="white",
            fg=self.secondary_color,
            wraplength=350,
            justify=tk.LEFT
        )
        title_label.pack(pady=(30, 20), padx=20, anchor="w")
        
        # Create info container
        info_container = tk.Frame(self.service_detail_frame, bg="white")
        info_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Office name
        office_label = tk.Label(
            info_container,
            text=f"Office: {service_data['office']}",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.text_color,
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        office_label.pack(pady=10, anchor="w", fill=tk.X)
        
        # Room number
        room_label = tk.Label(
            info_container,
            text=f"Room: {service_data['room']}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        room_label.pack(pady=8, anchor="w", fill=tk.X)
        
        # Separator
        separator = tk.Frame(info_container, height=2, bg="#e0e0e0")
        separator.pack(fill=tk.X, pady=15)
        
        # Working hours
        hours_label = tk.Label(
            info_container,
            text=f"Working Hours:\n{service_data['working_hours']}",
            font=("Arial", 12),
            bg="white",
            fg=self.text_color,
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        hours_label.pack(pady=10, anchor="w", fill=tk.X)
        
        # Add bottom padding
        bottom_spacer = tk.Frame(self.service_detail_frame, bg="white", height=30)
        bottom_spacer.pack()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CampusAssistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
