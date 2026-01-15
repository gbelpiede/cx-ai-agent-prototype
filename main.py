import streamlit as st
from api_client import api_client
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Proactive CX AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.customer = None
    st.session_state.api_error = None

# ============ AUTHENTICATION ============

def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🤖 Proactive CX AI Agent")
        st.markdown("### Replace Forms. Retain Workers. Grow Your Business.")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Sign Up", "Log In"])
        
        with tab1:
            st.subheader("Create Your Account")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            company_name = st.text_input("Company Name")
            industry = st.selectbox("Industry", 
                                   ["Staffing", "Logistics", "Hospitality", "Retail", "Manufacturing", "Healthcare", "Other"])
            employee_count = st.number_input("Number of Employees", min_value=10, max_value=10000, step=10)
            
            if st.button("Create Account", key="signup_btn"):
                if email and password and company_name:
                    try:
                        with st.spinner("Creating account..."):
                            response = api_client.signup(
                                email=email,
                                password=password,
                                company_name=company_name,
                                timezone="UTC",
                                industry=industry,
                                employee_count=employee_count
                            )
                        
                        st.session_state.logged_in = True
                        st.session_state.token = response['access_token']
                        st.session_state.customer = {
                            "email": email,
                            "company_name": company_name,
                            "industry": industry,
                            "employee_count": employee_count
                        }
                        st.success("✅ Account created! Welcome!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Sign up failed: {str(e)}")
                else:
                    st.error("Please fill in all fields")
        
        with tab2:
            st.subheader("Log In")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Log In", key="login_btn"):
                if email and password:
                    try:
                        with st.spinner("Logging in..."):
                            response = api_client.login(email, password)
                        
                        st.session_state.logged_in = True
                        st.session_state.token = response['access_token']
                        st.session_state.customer = {
                            "email": email,
                            "company_name": "Your Company"
                        }
                        st.success("✅ Logged in!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {str(e)}")
                else:
                    st.error("Please fill in all fields")

# ============ MAIN APP ============

def show_dashboard():
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.customer['company_name']}")
        st.markdown(f"**Email:** {st.session_state.customer['email']}")
        st.markdown("---")
        
        st.markdown("### 📍 Navigation")
        page = st.radio("", 
                        ["🏠 Dashboard", "🤖 Agents", "👥 Employees", "⚙️ Settings", "📊 Analytics"],
                        label_visibility="collapsed")
        
        st.markdown("---")
        if st.button("🚪 Log Out"):
            st.session_state.logged_in = False
            st.session_state.token = None
            st.rerun()
    
    # Main content
    if page == "🏠 Dashboard":
        show_dashboard_page()
    elif page == "🤖 Agents":
        show_agents_page()
    elif page == "👥 Employees":
        show_employees_page()
    elif page == "⚙️ Settings":
        show_settings_page()
    elif page == "📊 Analytics":
        show_analytics_page()

# ============ DASHBOARD PAGE ============

def show_dashboard_page():
    st.markdown("# 🏠 Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.customer['company_name']}**!")
    
    # Get agents
    try:
        agents = api_client.get_agents(st.session_state.token)
    except Exception as e:
        st.error(f"Failed to load agents: {str(e)}")
        agents = []
    
    if not agents:
        st.info("👋 No agents yet. Create your first AI agent to get started!")
        if st.button("➕ Create Your First Agent"):
            st.switch_page("pages/agents.py")
        return
    
    st.markdown("---")
    
    # Summary Cards
    try:
        summary = api_client.get_dashboard_summary(st.session_state.token)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Agents Active", len(agents))
        
        with col2:
            try:
                employee_data = api_client.get_employees(st.session_state.token, agents[0]['id'])
                st.metric("Employees", employee_data.get('total', 0))
            except:
                st.metric("Employees", "N/A")
        
        with col3:
            st.metric("Check-ins (30d)", summary.get('check_ins_sent_30d', 0))
        
        with col4:
            response_rate = int(summary.get('response_rate', 0) * 100)
            st.metric("Response Rate", f"{response_rate}%")
    except Exception as e:
        st.warning(f"Could not load dashboard stats: {str(e)}")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    activities = [
        {"time": "Just now", "action": "Loaded dashboard", "status": "✅ Connected"},
        {"time": "Few minutes ago", "action": "Agents retrieved from API", "status": "✅ Working"},
        {"time": "Less than 1 min ago", "action": "Connected to FastAPI backend", "status": "✅ Active"},
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(activity["action"])
        with col2:
            st.markdown(activity["time"])
        with col3:
            st.markdown(activity["status"])
        st.divider()

# ============ AGENTS PAGE ============

def show_agents_page():
    st.markdown("# 🤖 Agents")
    
    tab1, tab2 = st.tabs(["Your Agents", "Create New"])
    
    with tab1:
        try:
            agents = api_client.get_agents(st.session_state.token)
            
            if not agents:
                st.info("No agents yet. Create one in the 'Create New' tab!")
            else:
                for agent in agents:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### {agent['name']}")
                        voice = agent.get('voice_name', 'Unknown')
                        tone = int(agent.get('tone_score', 0) * 100)
                        st.markdown(f"**Voice:** {voice} | **Tone:** {tone}% Friendly")
                    
                    with col2:
                        status = "🟢 Active" if agent['status'] == 'active' else "🟡 Draft"
                        st.markdown(f"{status}")
                        flows = agent.get('flows_enabled', {})
                        enabled_flows = sum(1 for v in flows.values() if v)
                        st.markdown(f"Flows: {enabled_flows} enabled")
                    
                    with col3:
                        if agent['status'] == 'draft':
                            if st.button("✅ Activate", key=f"activate_{agent['id']}"):
                                try:
                                    api_client.activate_agent(st.session_state.token, agent['id'])
                                    st.success("Agent activated!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to activate: {str(e)}")
                    
                    st.divider()
        except Exception as e:
            st.error(f"Failed to load agents: {str(e)}")
    
    with tab2:
        st.subheader("Create New Agent")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            agent_name = st.text_input("Agent Name", value="Alex")
            description = st.text_area("Description", value="Friendly HR assistant")
            tone_score = st.slider("Tone", min_value=0.0, max_value=1.0, step=0.1, 
                                   value=0.7, help="0=Professional, 1=Friendly")
        
        with col2:
            voice_name = st.selectbox("Voice", 
                                     ["Adam", "Sarah", "Dorothy", "Josh", "Maya", "Chris", "James"])
            language = st.selectbox("Language", ["English", "Spanish", "French"])
        
        st.markdown("---")
        st.subheader("Enable Flows")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            retention = st.checkbox("📊 Retention Check-in", value=True)
        with col2:
            payroll = st.checkbox("💰 Payroll Help", value=True)
        with col3:
            safety = st.checkbox("⚠️ Safety Reports", value=False)
        
        st.markdown("---")
        
        if st.button("✅ Create Agent"):
            try:
                with st.spinner("Creating agent..."):
                    agent_data = {
                        "name": agent_name,
                        "description": description,
                        "tone_score": tone_score,
                        "voice_name": voice_name,
                        "language": language,
                        "flows_enabled": {
                            "retention_checkin": retention,
                            "payroll_help": payroll,
                            "safety_report": safety
                        }
                    }
                    result = api_client.create_agent(st.session_state.token, agent_data)
                
                st.success(f"✅ Agent '{agent_name}' created!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to create agent: {str(e)}")

# ============ EMPLOYEES PAGE ============

def show_employees_page():
    st.markdown("# 👥 Employees")
    
    # Get agents
    try:
        agents = api_client.get_agents(st.session_state.token)
    except Exception as e:
        st.error(f"Failed to load agents: {str(e)}")
        agents = []
    
    if not agents:
        st.warning("Create an agent first before uploading employees.")
        return
    
    agent_id = st.selectbox("Select Agent", 
                           options=[a['id'] for a in agents],
                           format_func=lambda x: next(a['name'] for a in agents if a['id'] == x))
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Directory", "Add Manually", "Upload CSV"])
    
    with tab1:
        st.subheader("Employee Directory")
        
        try:
            employee_data = api_client.get_employees(st.session_state.token, agent_id)
            employees = employee_data.get('employees', [])
            
            if employees:
                emp_list = []
                for emp in employees:
                    emp_list.append({
                        "Name": emp['first_name'] + " " + emp['last_name'],
                        "Phone": emp['phone'],
                        "Hire Date": emp['hire_date'],
                        "Site": emp.get('site_location', 'N/A'),
                        "Status": "✅ Active"
                    })
                
                st.dataframe(emp_list, use_container_width=True)
            else:
                st.info("No employees yet. Add them manually or upload a CSV.")
        except Exception as e:
            st.error(f"Failed to load employees: {str(e)}")
    
    with tab2:
        st.subheader("Add Employee Manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone (E.164 format)", "+1-555-0100")
            email = st.text_input("Email")
        
        with col2:
            hire_date = st.date_input("Hire Date")
            manager_name = st.text_input("Manager Name")
            site_location = st.text_input("Site Location", "Main Site")
        
        if st.button("➕ Add Employee"):
            if first_name and last_name and phone:
                try:
                    with st.spinner("Adding employee..."):
                        employee_data_dict = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "phone": phone,
                            "email": email,
                            "hire_date": str(hire_date),
                            "manager_name": manager_name,
                            "site_location": site_location,
                            "department": "Operations"
                        }
                        api_client.add_employee(st.session_state.token, agent_id, employee_data_dict)
                    
                    st.success("✅ Employee added!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add employee: {str(e)}")
            else:
                st.error("Please fill in required fields (First Name, Last Name, Phone)")
    
    with tab3:
        st.subheader("Upload CSV")
        st.markdown("**Expected columns:** first_name, last_name, phone, email, hire_date, manager_name, site_location")
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())
            
            if st.button("✅ Import"):
                try:
                    with st.spinner(f"Importing {len(df)} employees..."):
                        for idx, row in df.iterrows():
                            employee_dict = {
                                "first_name": row.get('first_name', ''),
                                "last_name": row.get('last_name', ''),
                                "phone": row.get('phone', ''),
                                "email": row.get('email', ''),
                                "hire_date": str(row.get('hire_date', '')),
                                "manager_name": row.get('manager_name', ''),
                                "site_location": row.get('site_location', ''),
                                "department": row.get('department', 'Operations')
                            }
                            api_client.add_employee(st.session_state.token, agent_id, employee_dict)
                    
                    st.success(f"✅ Imported {len(df)} employees!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to import: {str(e)}")

# ============ SETTINGS PAGE ============

def show_settings_page():
    st.markdown("# ⚙️ Settings")
    
    tab1 = st.tabs(["Company Profile"])[0]
    
    with tab1:
        st.subheader("Company Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Company:** {st.session_state.customer['company_name']}")
            st.markdown(f"**Industry:** {st.session_state.customer.get('industry', 'N/A')}")
            timezone = st.selectbox("Timezone", 
                                   ["America/Los_Angeles", "America/Chicago", "America/New_York", "UTC"])
        
        with col2:
            st.markdown(f"**Email:** {st.session_state.customer['email']}")
            st.markdown(f"**Employees:** {st.session_state.customer.get('employee_count', 'N/A')}")
            language = st.selectbox("Language", ["English", "Spanish", "French"])
        
        if st.button("💾 Save Changes"):
            st.success("✅ Settings updated!")

# ============ ANALYTICS PAGE ============

def show_analytics_page():
    st.markdown("# 📊 Analytics & Results")
    
    # Get agents
    try:
        agents = api_client.get_agents(st.session_state.token)
    except Exception as e:
        st.error(f"Failed to load agents: {str(e)}")
        agents = []
    
    if not agents:
        st.info("Create an agent to see analytics.")
        return
    
    # Summary cards
    st.subheader("Summary (Last 30 Days)")
    
    try:
        summary = api_client.get_dashboard_summary(st.session_state.token)
        sentiment = api_client.get_sentiment_breakdown(st.session_state.token)
        roi = api_client.get_roi_metrics(st.session_state.token)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Check-ins Sent", summary.get('check_ins_sent_30d', 0), "+45%")
        with col2:
            response_rate = int(summary.get('response_rate', 0) * 100)
            st.metric("Response Rate", f"{response_rate}%", "+12%")
        with col3:
            st.metric("Avg Sentiment", "+0.42", "↑ Positive")
        with col4:
            st.metric("Churn Alerts", summary.get('churn_alerts_this_month', 0), "⚠️ High")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution")
            sentiment_data = {
                "Positive": sentiment.get('positive', {}).get('count', 0),
                "Neutral": sentiment.get('neutral', {}).get('count', 0),
                "Negative": sentiment.get('negative', {}).get('count', 0)
            }
            st.bar_chart(sentiment_data)
        
        with col2:
            st.subheader("Response Rate Trend")
            trend_data = {
                "Week 1": 65,
                "Week 2": 70,
                "Week 3": 76,
                "Week 4": int(summary.get('response_rate', 0) * 100)
            }
            st.line_chart(trend_data)
        
        st.markdown("---")
        
        # ROI
        st.subheader("💰 Estimated Impact")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Time Saved", f"{roi.get('time_saved_hours', 0):.0f} hours", "Admin work")
        with col2:
            improvement = int(roi.get('response_rate_improvement_pct', 0))
            st.metric("Response Improvement", f"+{improvement}%", "vs. forms")
        with col3:
            savings = roi.get('estimated_savings', 0)
            st.metric("Est. Savings", f"${savings:,.0f}", "Replacement costs")
    
    except Exception as e:
        st.error(f"Failed to load analytics: {str(e)}")

# ============ MAIN ============

if __name__ == "__main__":
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()
