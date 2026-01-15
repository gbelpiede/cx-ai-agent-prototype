# Proactive CX AI Agent - Streamlit Prototype

A fully interactive, clickable prototype demonstrating the complete customer experience of the Proactive CX AI Agent platform.

**NOW WIRED TO REAL FASTAPI BACKEND** ✅

---

## ✨ What's New

This prototype now **connects to the real FastAPI backend** (instead of using mock data):
- ✅ **Real authentication** (signup, login with JWT tokens)
- ✅ **Real agent creation** (saved to Supabase database)
- ✅ **Real employee management** (add employees, upload CSV)
- ✅ **Real analytics** (pulls from backend)
- ✅ **Real data persistence** (all changes saved in Supabase)

---

## 🎯 What This Prototype Shows

### 1. **Authentication** (Sign Up / Log In)
- Create new account with company details
- Enter email, password, company name, industry, employee count
- Real login flow

### 2. **Agent Builder** (Create & Customize AI Agent)
- **Create Agent**: Name (e.g., "Alex"), description
- **Customize Tone**: Slider from Professional (0%) to Friendly (100%)
- **Select Voice**: Choose from 7 ElevenLabs voices
- **Enable Flows**: Toggle Retention Check-in, Payroll Help, Safety Reports
- **Status**: Draft → Active

### 3. **Employee Management**
- **Upload CSV**: Bulk import with preview
- **Manual Add**: Add single employees with all details
- **Directory View**: List all employees with hire date, site, status

### 4. **Settings & Configuration**
- Company profile (timezone, language)
- Integration setup (Slack, Google Sheets, ADP, Workday)
- Escalation rules (sentiment thresholds, keywords, alert destinations)

### 5. **Dashboard** 
- Quick stats (agents, employees, check-ins, response rate)
- Recent activity feed
- Quick navigation to create first agent

### 6. **Analytics & Results**
- Summary cards (30-day metrics)
- Sentiment distribution chart
- Response rate trend
- At-risk employees list
- ROI estimate ($15K savings example)

---

## 🚀 How to Run

### Prerequisites
You must have the FastAPI backend running first. See `/backend/QUICKSTART.md` for setup.

### Step 1: Install Dependencies
```bash
cd /Users/giuseppebelpiede/Claude\ Code/CX\ AI\ Agent/prototype
pip install -r requirements.txt
```

### Step 2: Verify Backend is Running
```bash
# In another terminal, check backend is running at port 8000:
curl http://localhost:8000/health

# You should see:
# {"status":"healthy","version":"0.1.0","environment":"development"}
```

### Step 3: Run the Streamlit App
```bash
streamlit run main.py
```

### Step 4: Open in Browser
```
http://localhost:8501
```

You should see the **Proactive CX AI Agent** login page.

---

## 🔗 Backend Connection

The app connects to the FastAPI backend at: `http://localhost:8000`

If your backend is running on a different port, edit `api_client.py`:
```python
API_BASE_URL = "http://localhost:8000/v1"  # Change 8000 to your port
```

---

## 🎮 How to Use the Prototype

### First Time: Create Account
1. Click **Sign Up** tab
2. Enter:
   - Email: `demo@staffing.com`
   - Password: `demo123`
   - Company: `Staffing Co`
   - Industry: `Staffing`
   - Employees: `150`
3. Click **Create Account**

### Then: Create Your First Agent
1. Left sidebar → **🤖 Agents**
2. Click **Create New** tab
3. Customize:
   - Name: `Alex` (default)
   - Tone: Slide to ~70% Friendly
   - Voice: Select `Sarah`
   - Enable: ✓ Retention Check-in, ✓ Payroll Help
4. Click **✅ Create Agent**

### Then: Upload Employees
1. Left sidebar → **👥 Employees**
2. **Option A - Upload CSV:**
   - Prepare CSV with columns: `first_name, last_name, phone, email, hire_date, manager_name, site_location`
   - Click **Upload CSV** tab
   - Select file → Preview → **✅ Import**

3. **Option B - Manual Add:**
   - Click **Add Manually** tab
   - Fill form with employee details
   - Click **➕ Add Employee**

### Then: View Dashboard
1. Left sidebar → **🏠 Dashboard**
2. See:
   - Summary cards (agents, employees, check-ins)
   - Recent activity
   - Quick navigation buttons

### Then: View Analytics
1. Left sidebar → **📊 Analytics**
2. See:
   - 30-day summary
   - Sentiment distribution
   - Response rate trends
   - At-risk employees
   - ROI estimate

### Advanced: Configure Flows
1. Left sidebar → **⚙️ Settings**
2. **Escalation Rules** tab
3. Set:
   - Sentiment threshold (when to alert)
   - Escalation keywords
   - Alert destinations (Slack, Email, SMS)

---

## 📊 Sample Data Included

When you interact with the prototype:
- **Mock agents** created have realistic settings (voice, tone, flows)
- **Mock employees** display in directory with hire dates, locations
- **Mock analytics** show realistic metrics (78% response rate, 12 churn alerts)
- **Mock sentiment distribution** visualizes positive/neutral/negative breakdown
- **Mock at-risk employees** demonstrate escalation workflow

---

## 🔧 Customization

### Add More Voices
In `main.py`, find this line:
```python
voice_name = st.selectbox("Voice", 
                         ["Adam", "Sarah", "Dorothy", "Josh", "Maya", "Chris", "James"])
```

Add more voices from ElevenLabs.

### Modify Flow Options
In `show_agents_page()`, change:
```python
col1, col2, col3 = st.columns(3)

with col1:
    retention = st.checkbox("📊 Retention Check-in", value=True)
with col2:
    payroll = st.checkbox("💰 Payroll Help", value=True)
with col3:
    safety = st.checkbox("⚠️ Safety Reports", value=False)
```

### Change Sidebar Navigation
In `show_dashboard()`, modify:
```python
page = st.radio("", 
                ["🏠 Dashboard", "🤖 Agents", "👥 Employees", "⚙️ Settings", "📊 Analytics"],
                label_visibility="collapsed")
```

---

## 📝 What's Included vs. NOT Included

### ✅ Included (Real Backend)
- ✅ Real authentication (JWT tokens)
- ✅ Real database connections (Supabase)
- ✅ Real agent management (create, list, activate)
- ✅ Real employee management (add, upload CSV)
- ✅ Real data persistence (Supabase database)
- ✅ Real analytics API calls

### ❌ Not Yet Integrated
- ❌ **WhatsApp integration** (no actual SMS/WhatsApp messages sent)
- ❌ **LangFlow execution** (AI responses are mocked)
- ❌ **ElevenLabs voice** (no actual voice generation)
- ❌ **Actual check-in conversations** (message sending is mocked)
- ❌ **Sentiment analysis** (returns mock sentiment scores)
- ❌ **Slack alerts** (no actual Slack notifications)

**To add these**:
1. Build LangFlow flows (from `/research/langflow_setup_guide.md`)
2. Integrate WhatsApp Business API in backend
3. Add ElevenLabs voice synthesis endpoint
4. Implement Groq Whisper for voice transcription
5. Connect Slack webhooks for alerts

---

## 🎓 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Gallery**: https://streamlit.io/gallery
- **Python Pandas**: https://pandas.pydata.org
- **Session State**: https://docs.streamlit.io/library/api-reference/session-state

---

## 🐛 Troubleshooting

### Port already in use
```bash
streamlit run main.py --server.port 8502
```

### Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Session state lost after refresh
This is expected. Streamlit session state is in-memory. For persistence, use a real database.

---

## 📸 Screenshots (What You'll See)

1. **Login Screen**
   - Clean sign-up form
   - Company details input
   - Account creation button

2. **Dashboard**
   - Summary cards (agents, employees, check-ins)
   - Recent activity feed
   - Quick onboarding prompts

3. **Agent Builder**
   - Create agent form
   - Tone slider with examples
   - Voice selector
   - Flow toggles

4. **Employee Directory**
   - Table view of all employees
   - CSV import flow
   - Manual add form

5. **Settings**
   - Company profile editor
   - Integration connectors (Slack, Google Sheets, ADP)
   - Escalation rule configuration

6. **Analytics**
   - Summary metrics
   - Charts (sentiment, response rate trend)
   - At-risk employees list
   - ROI estimate

---

## 🎯 Common Tasks

### Run Both Services Together (Full Stack)

**Terminal 1 - Start Backend:**
```bash
cd "/Users/giuseppebelpiede/Claude Code/CX AI Agent/backend"
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
cd "/Users/giuseppebelpiede/Claude Code/CX AI Agent/prototype"
streamlit run main.py
```

**Terminal 3 (Optional) - Swagger API Docs:**
- Open: http://localhost:8000/docs
- Test endpoints manually here

---

## 🚀 Next Phases

### Phase 1: Expand API Coverage ✅ DONE
- ✅ Authentication, Agents, Employees, Check-ins, Analytics

### Phase 2: Add AI Integration
1. Build LangFlow flows (Retention, Payroll, Safety)
2. Create `/check-ins/{id}/process` endpoint that calls LangFlow
3. Implement sentiment analysis
4. Add escalation logic

### Phase 3: Add External Integrations
1. WhatsApp Business API webhook
2. ElevenLabs voice synthesis
3. Groq Whisper STT
4. Slack alert webhooks

### Phase 4: Production Ready
1. Deploy backend to AWS/GCP/Heroku
2. Set up CI/CD pipeline
3. Configure production database
4. Add monitoring & logging
5. Security audit

---

## 📧 Questions?

Review these docs for more details:
- **Product Overview**: `/product/PRODUCT_BLUEPRINT.md`
- **Technical Spec**: `/product/API_SPECIFICATION.md`
- **Database Design**: `/product/DATABASE_SCHEMA.md`
- **Roadmap**: `/product/FEATURE_ROADMAP.md`
- **LangFlow Setup**: `/research/langflow_setup_guide.md`
- **Audio Integration**: `/research/audio_voice_integration.md`

