import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="HR Resource Query Chatbot",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .employee-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    .skill-tag {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .availability-available {
        color: #4caf50;
        font-weight: bold;
    }
    .availability-busy {
        color: #f44336;
        font-weight: bold;
    }
    .main-header {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 2rem;
    }
    .query-examples {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to the backend."""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API server. Please make sure the FastAPI server is running on http://localhost:8000")
        st.info("💡 **To start the server:** Open terminal and run: `python -m uvicorn app.main:app --reload --port 8000`")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def display_employee_card(employee: Dict, show_full: bool = True):
    """Display an employee card with formatted information."""
    availability_class = "availability-available" if employee["availability"] == "available" else "availability-busy"
    
    if show_full:
        st.markdown(f"""
        <div class="employee-card">
            <h4>👤 {employee["name"]}</h4>
            <p><strong>Experience:</strong> {employee["experience_years"]} years</p>
            <p><strong>Department:</strong> {employee.get("department", "Unknown")}</p>
            <p><strong>Location:</strong> {employee.get("location", "Unknown")}</p>
            <p><strong>Availability:</strong> <span class="{availability_class}">{employee["availability"].title()}</span></p>
            <p><strong>Email:</strong> {employee.get("email", "Not provided")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Skills
        st.write("**Skills:**")
        skills_html = ""
        for skill in employee["skills"]:
            skills_html += f'<span class="skill-tag">{skill}</span> '
        st.markdown(skills_html, unsafe_allow_html=True)
        
        # Projects
        st.write("**Recent Projects:**")
        for project in employee["projects"]:
            st.write(f"• {project}")
        
        st.markdown("---")
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{employee['name']}** - {employee.get('department', 'Unknown')}")
            st.write(f"Skills: {', '.join(employee['skills'][:3])}{'...' if len(employee['skills']) > 3 else ''}")
        with col2:
            st.write(f"{employee['experience_years']} years exp.")
        with col3:
            status_emoji = "✅" if employee["availability"] == "available" else "🔴"
            st.write(f"{status_emoji} {employee['availability'].title()}")

def show_example_queries():
    """Display example queries that users can click."""
    st.markdown('<div class="query-examples">', unsafe_allow_html=True)
    st.write("**💡 Try these example queries:**")
    
    example_queries = [
        "Find Python developers with 3+ years experience",
        "Who has worked on healthcare projects?",
        "Suggest people for a React Native project", 
        "Find developers who know both AWS and Docker",
        "I need someone experienced with machine learning for a healthcare project",
        "Who can help with mobile app development?",
        "Find available backend engineers",
        "Who has experience with DevOps and cloud technologies?",
        "Find QA engineers with automation experience",
        "Who can work on data science projects?"
    ]
    
    # Create columns for better layout
    cols = st.columns(2)
    for i, query in enumerate(example_queries):
        col = cols[i % 2]
        with col:
            if st.button(f"📝 {query}", key=f"example_{i}", help="Click to use this query"):
                st.session_state["query_input"] = query
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">👥 HR Resource Query Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1em;">AI-powered assistant to help you find the right employees for your projects</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Status & Controls")
        
        # Health check
        if st.button("🔍 Check API Status", help="Test connection to the backend API"):
            with st.spinner("Checking API status..."):
                health = make_api_request("/health")
                if health:
                    st.success(f"✅ API is healthy!")
                    st.info(f"📊 **Employees loaded:** {health['employees_loaded']}")
                else:
                    st.error("❌ API is not responding")
        
        st.markdown("---")
        
        # Basic search
        st.header("🔎 Advanced Filter Search")
        with st.form("basic_search"):
            skills_input = st.text_input(
                "Skills (comma-separated)", 
                placeholder="Python, React, AWS",
                help="Enter skills separated by commas"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                min_exp = st.number_input("Min Experience", min_value=0, value=0, help="Minimum years of experience")
            with col2:
                availability = st.selectbox("Availability", ["", "available", "busy"])
            
            department = st.text_input("Department", placeholder="Engineering", help="Filter by department")
            
            search_clicked = st.form_submit_button("🔍 Filter Search", type="primary")
            
            if search_clicked:
                with st.spinner("Searching employees..."):
                    params = {}
                    if skills_input: params["skills"] = skills_input
                    if min_exp > 0: params["min_experience"] = min_exp
                    if availability: params["availability"] = availability
                    if department: params["department"] = department
                    
                    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                    result = make_api_request(f"/employees/search?{query_string}")
                    
                    if result:
                        st.session_state["search_results"] = result["employees"]
                        st.success(f"Found {result['count']} employees")
        
        # View all employees
        st.markdown("---")
        if st.button("👥 View All Employees"):
            with st.spinner("Loading all employees..."):
                result = make_api_request("/employees")
                if result:
                    st.session_state["all_employees"] = result
                    st.success(f"Loaded {len(result)} employees")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🤖 AI Chat", "🔍 Search Results", "📊 All Employees"])
    
    with tab1:
        st.header("💬 Natural Language Query")
        
        # Show example queries
        show_example_queries()
        
        # Chat input
        query_input = st.text_input(
            "Ask me anything about our employees:",
            placeholder="e.g., Find Python developers with ML experience who are available",
            value=st.session_state.get("query_input", ""),
            key="main_query",
            help="Ask questions in natural language about finding employees"
        )
        
        col1, col2, col3 = st.columns([2, 1, 3])
        with col1:
            search_button = st.button("🚀 Search with AI", type="primary", help="Use AI to find and recommend employees")
        with col2:
            if st.button("🗑️ Clear", help="Clear the input field"):
                st.session_state["query_input"] = ""
                st.experimental_rerun()
        
        # Process chat query
        if search_button and query_input:
            with st.spinner("🤖 AI is analyzing your request..."):
                result = make_api_request("/chat", "POST", {"query": query_input})
                
                if result:
                    st.session_state["chat_result"] = result
                    st.session_state["query_input"] = ""  # Clear input
                    st.experimental_rerun()
        
        # Display chat results
        if "chat_result" in st.session_state:
            result = st.session_state["chat_result"]
            
            st.markdown("---")
            st.header("🤖 AI Response")
            
            # Show confidence score
            if result.get("confidence_score"):
                confidence_percentage = result["confidence_score"] * 100
                confidence_color = "green" if confidence_percentage > 70 else "orange" if confidence_percentage > 40 else "red"
                st.markdown(f"**Confidence Score:** <span style='color: {confidence_color}'>{confidence_percentage:.1f}%</span>", unsafe_allow_html=True)
            
            # AI response
            st.markdown(f"**AI Analysis:**")
            st.write(result["response"])
            
            if result["relevant_employees"]:
                st.header("👥 Recommended Employees")
                
                # Summary stats
                total_employees = len(result["relevant_employees"])
                available_count = sum(1 for emp in result["relevant_employees"] if emp["availability"] == "available")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Found", total_employees)
                with col2:
                    st.metric("Available", available_count)
                with col3:
                    st.metric("Busy", total_employees - available_count)
                
                # Display employees
                for i, employee in enumerate(result["relevant_employees"], 1):
                    with st.expander(f"🏆 Candidate {i}: {employee['name']} ({employee['experience_years']} years)", expanded=(i <= 2)):
                        display_employee_card(employee)
    
    with tab2:
        st.header("🔍 Filter Search Results")
        
        if "search_results" in st.session_state and st.session_state["search_results"]:
            employees = st.session_state["search_results"]
            st.success(f"Found {len(employees)} employees matching your criteria")
            
            # Create summary table
            if employees:
                df_data = []
                for emp in employees:
                    df_data.append({
                        "Name": emp["name"],
                        "Department": emp.get("department", "Unknown"),
                        "Experience": f"{emp['experience_years']} years",
                        "Top Skills": ", ".join(emp["skills"][:3]),
                        "Availability": emp["availability"].title(),
                        "Location": emp.get("location", "Unknown")
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Detailed Profiles")
                
                for i, employee in enumerate(employees, 1):
                    with st.expander(f"{employee['name']} - {employee.get('department', 'Unknown')} Department"):
                        display_employee_card(employee)
        else:
            st.info("Use the sidebar filters to search for employees, or try the AI chat for natural language queries.")
    
    with tab3:
        st.header("📊 All Employees Database")
        
        if "all_employees" in st.session_state:
            employees = st.session_state["all_employees"]
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Employees", len(employees))
            with col2:
                available = sum(1 for emp in employees if emp["availability"] == "available")
                st.metric("Available", available)
            with col3:
                avg_exp = sum(emp["experience_years"] for emp in employees) / len(employees)
                st.metric("Avg Experience", f"{avg_exp:.1f} years")
            with col4:
                departments = len(set(emp.get("department", "Unknown") for emp in employees))
                st.metric("Departments", departments)
            
            # Department breakdown
            st.subheader("👥 Department Breakdown")
            dept_data = {}
            for emp in employees:
                dept = emp.get("department", "Unknown")
                if dept not in dept_data:
                    dept_data[dept] = {"count": 0, "available": 0}
                dept_data[dept]["count"] += 1
                if emp["availability"] == "available":
                    dept_data[dept]["available"] += 1
            
            dept_df = pd.DataFrame([
                {"Department": dept, "Total": data["count"], "Available": data["available"]}
                for dept, data in dept_data.items()
            ])
            st.dataframe(dept_df, use_container_width=True)
            
            # Full employee list
            st.subheader("📋 Complete Employee Directory")
            
            # Search within all employees
            search_term = st.text_input("🔍 Quick search employees:", placeholder="Search by name, skill, or project...")
            
            filtered_employees = employees
            if search_term:
                search_lower = search_term.lower()
                filtered_employees = [
                    emp for emp in employees
                    if (search_lower in emp["name"].lower() or
                        any(search_lower in skill.lower() for skill in emp["skills"]) or
                        any(search_lower in project.lower() for project in emp["projects"]) or
                        search_lower in emp.get("department", "").lower())
                ]
                st.info(f"Showing {len(filtered_employees)} employees matching '{search_term}'")
            
            for employee in filtered_employees:
                with st.expander(f"{employee['name']} - {employee.get('department', 'Unknown')} ({employee['experience_years']} years)"):
                    display_employee_card(employee)
        else:
            st.info("Click 'View All Employees' in the sidebar to load the complete employee database.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 Powered by AI • Built with Streamlit & FastAPI</p>
        <p>💡 <strong>Tip:</strong> For best results, be specific about skills, experience level, and project requirements</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()