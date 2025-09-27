import json
import os
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self, employees_file: str = "app/data/employees.json"):
        self.employees_file = employees_file
        self.employees = self.load_employees()
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.employee_embeddings = self.create_employee_embeddings()
        
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def load_employees(self) -> List[dict]:
        """Load employee data from JSON file."""
        try:
            with open(self.employees_file, 'r') as f:
                data = json.load(f)
            return data['employees']
        except FileNotFoundError:
            print(f"Warning: {self.employees_file} not found. Using empty employee list.")
            return []
    
    def create_employee_text(self, employee: dict) -> str:
        """Create searchable text representation of employee."""
        skills_text = ", ".join(employee['skills'])
        projects_text = ", ".join(employee['projects'])
        
        text = f"""
        Name: {employee['name']}
        Skills: {skills_text}
        Experience: {employee['experience_years']} years
        Projects: {projects_text}
        Department: {employee.get('department', 'Unknown')}
        Location: {employee.get('location', 'Unknown')}
        Availability: {employee['availability']}
        """
        return text.strip()
    
    def create_employee_embeddings(self) -> np.ndarray:
        """Create embeddings for all employees."""
        if not self.employees:
            return np.array([])
        
        employee_texts = [self.create_employee_text(emp) for emp in self.employees]
        embeddings = self.embeddings_model.encode(employee_texts)
        return embeddings
    
    def retrieve_relevant_employees(self, query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """Retrieve most relevant employees based on query."""
        if not self.employees or len(self.employee_embeddings) == 0:
            return []
            
        query_embedding = self.embeddings_model.encode([query])
        similarities = cosine_similarity(query_embedding, self.employee_embeddings)[0]
        
        # Get top-k most similar employees
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        relevant_employees = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                relevant_employees.append((self.employees[idx], float(similarities[idx])))
        
        return relevant_employees
    
    def generate_response(self, query: str, relevant_employees: List[Tuple[dict, float]]) -> str:
        """Generate natural language response using OpenAI."""
        if not relevant_employees:
            return "I couldn't find any employees matching your criteria. Please try refining your search."
        
        # Prepare context for the LLM
        context = "Here are the relevant employees I found:\n\n"
        for employee, score in relevant_employees:
            context += f"**{employee['name']}** ({employee['experience_years']} years experience)\n"
            context += f"Skills: {', '.join(employee['skills'])}\n"
            context += f"Recent Projects: {', '.join(employee['projects'])}\n"
            context += f"Department: {employee.get('department', 'Unknown')}\n"
            context += f"Location: {employee.get('location', 'Unknown')}\n"
            context += f"Availability: {employee['availability']}\n"
            context += f"Relevance Score: {score:.2f}\n\n"
        
        prompt = f"""
        You are an HR assistant helping to find the right employees for specific requirements.
        
        User Query: "{query}"
        
        {context}
        
        Please provide a helpful response that:
        1. Directly addresses the user's query
        2. Highlights the most relevant candidates and why they're a good fit
        3. Mentions specific skills and experience that match the requirements
        4. Provides practical next steps or suggestions
        5. Uses a professional but conversational tone
        
        If multiple candidates are found, rank them by relevance and explain the differences.
        If availability is a concern, mention it appropriately.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful HR assistant that provides detailed, actionable recommendations for employee resource allocation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to template-based response if OpenAI fails
            return self.generate_fallback_response(query, relevant_employees)
    
    def generate_fallback_response(self, query: str, relevant_employees: List[Tuple[dict, float]]) -> str:
        """Generate a template-based response if OpenAI is not available."""
        if not relevant_employees:
            return "I couldn't find any employees matching your criteria. Please try refining your search."
        
        response = f"Based on your query '{query}', I found {len(relevant_employees)} relevant candidate(s):\n\n"
        
        for i, (employee, score) in enumerate(relevant_employees, 1):
            response += f"**{i}. {employee['name']}** ({employee['experience_years']} years experience)\n"
            response += f"   • Skills: {', '.join(employee['skills'])}\n"
            response += f"   • Recent Projects: {', '.join(employee['projects'])}\n"
            response += f"   • Availability: {employee['availability']}\n"
            response += f"   • Match Score: {score:.1%}\n\n"
        
        response += "Would you like more details about any of these candidates or help with scheduling interviews?"
        return response
    
    def process_query(self, query: str) -> dict:
        """Main method to process a query and return results."""
        # Step 1: Retrieve relevant employees
        relevant_employees = self.retrieve_relevant_employees(query)
        
        # Step 2: Generate response
        response = self.generate_response(query, relevant_employees)
        
        # Step 3: Prepare final result
        employees_list = [emp for emp, score in relevant_employees]
        confidence_score = relevant_employees[0][1] if relevant_employees else 0.0
        
        return {
            "response": response,
            "relevant_employees": employees_list,
            "confidence_score": confidence_score
        }