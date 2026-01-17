import requests
import json
from typing import Optional, Dict, Any, List
import streamlit as st
import os

# API base URL - use environment variable or default to production
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://cxai-backend-prod-6e43ca701a40.herokuapp.com/v1"
)

class APIClient:
    """Client for calling FastAPI backend"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """Get headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    # ============ AUTH ============
    
    def signup(self, email: str, password: str, company_name: str, 
               timezone: str, industry: str, employee_count: int) -> Dict[str, Any]:
        """Sign up new customer"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/signup",
                headers=self.get_headers(),
                json={
                    "email": email,
                    "password": password,
                    "company_name": company_name,
                    "timezone": timezone,
                    "industry": industry,
                    "employee_count": employee_count
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Signup failed"))
        except Exception as e:
            raise Exception(f"Signup error: {str(e)}")
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login customer"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                headers=self.get_headers(),
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Login failed"))
        except Exception as e:
            raise Exception(f"Login error: {str(e)}")
    
    # ============ AGENTS ============
    
    def create_agent(self, token: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new agent"""
        try:
            response = requests.post(
                f"{self.base_url}/agents",
                headers=self.get_headers(token),
                json=agent_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Agent creation failed"))
        except Exception as e:
            raise Exception(f"Create agent error: {str(e)}")
    
    def get_agents(self, token: str) -> List[Dict[str, Any]]:
        """Get all agents"""
        try:
            response = requests.get(
                f"{self.base_url}/agents",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json().get("agents", [])
            else:
                raise Exception(response.json().get("detail", "Failed to get agents"))
        except Exception as e:
            raise Exception(f"Get agents error: {str(e)}")
    
    def update_agent(self, token: str, agent_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update agent"""
        try:
            response = requests.patch(
                f"{self.base_url}/agents/{agent_id}",
                headers=self.get_headers(token),
                json=updates
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Agent update failed"))
        except Exception as e:
            raise Exception(f"Update agent error: {str(e)}")
    
    def activate_agent(self, token: str, agent_id: str) -> Dict[str, Any]:
        """Activate agent"""
        try:
            response = requests.post(
                f"{self.base_url}/agents/{agent_id}/activate",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Agent activation failed"))
        except Exception as e:
            raise Exception(f"Activate agent error: {str(e)}")
    
    # ============ EMPLOYEES ============
    
    def add_employee(self, token: str, agent_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add single employee"""
        try:
            response = requests.post(
                f"{self.base_url}/employees?agent_id={agent_id}",
                headers=self.get_headers(token),
                json=employee_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Employee creation failed"))
        except Exception as e:
            raise Exception(f"Add employee error: {str(e)}")
    
    def get_employees(self, token: str, agent_id: str, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get employees for agent"""
        try:
            response = requests.get(
                f"{self.base_url}/employees?agent_id={agent_id}&page={page}&limit={limit}",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Failed to get employees"))
        except Exception as e:
            raise Exception(f"Get employees error: {str(e)}")
    
    # ============ CHECK-INS ============
    
    def create_checkin(self, token: str, agent_id: str, employee_id: str, flow_name: str) -> Dict[str, Any]:
        """Trigger check-in"""
        try:
            response = requests.post(
                f"{self.base_url}/check-ins",
                headers=self.get_headers(token),
                json={
                    "agent_id": agent_id,
                    "employee_id": employee_id,
                    "flow_name": flow_name
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Check-in creation failed"))
        except Exception as e:
            raise Exception(f"Create check-in error: {str(e)}")
    
    def get_checkin(self, token: str, checkin_id: str) -> Dict[str, Any]:
        """Get check-in details"""
        try:
            response = requests.get(
                f"{self.base_url}/check-ins/{checkin_id}",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Failed to get check-in"))
        except Exception as e:
            raise Exception(f"Get check-in error: {str(e)}")
    
    def send_message(self, token: str, checkin_id: str, user_message: str, source: str = "web") -> Dict[str, Any]:
        """Send message in check-in"""
        try:
            response = requests.post(
                f"{self.base_url}/check-ins/{checkin_id}/message",
                headers=self.get_headers(token),
                json={
                    "user_message": user_message,
                    "source": source
                }
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json().get("detail", "Message send failed"))
        except Exception as e:
            raise Exception(f"Send message error: {str(e)}")
    
    # ============ ANALYTICS ============
    
    def get_dashboard_summary(self, token: str) -> Dict[str, Any]:
        """Get dashboard summary"""
        try:
            response = requests.get(
                f"{self.base_url}/dashboard/summary",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to get summary")
        except Exception as e:
            raise Exception(f"Get summary error: {str(e)}")
    
    def get_sentiment_breakdown(self, token: str) -> Dict[str, Any]:
        """Get sentiment breakdown"""
        try:
            response = requests.get(
                f"{self.base_url}/dashboard/sentiment",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to get sentiment")
        except Exception as e:
            raise Exception(f"Get sentiment error: {str(e)}")
    
    def get_roi_metrics(self, token: str) -> Dict[str, Any]:
        """Get ROI metrics"""
        try:
            response = requests.get(
                f"{self.base_url}/dashboard/roi",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Failed to get ROI")
        except Exception as e:
            raise Exception(f"Get ROI error: {str(e)}")

    # ============ DOCUMENTS ============

    def get_documents(self, token: str) -> List[Dict[str, Any]]:
        """Get available documents (PDFs)"""
        try:
            response = requests.get(
                f"{self.base_url}/documents",
                headers=self.get_headers(token)
            )
            if response.status_code == 200:
                return response.json().get("documents", [])
            else:
                raise Exception(response.json().get("detail", "Failed to get documents"))
        except Exception as e:
            raise Exception(f"Get documents error: {str(e)}")

# Create global API client instance
api_client = APIClient()
