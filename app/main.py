from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from .models import Employee, ChatQuery, ChatResponse
from .rag_system import RAGSystem

# Initialize FastAPI app
app = FastAPI(
    title="HR Resource Query Chatbot API",
    description="AI-powered HR assistant for finding the right employees using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = RAGSystem()

@app.get("/")
async def root():
    return {"message": "HR Resource Query Chatbot API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat_query(query: ChatQuery):
    """Process a natural language query and return relevant employees."""
    try:
        result = rag_system.process_query(query.query)
        
        return ChatResponse(
            response=result["response"],
            relevant_employees=result["relevant_employees"],
            confidence_score=result["confidence_score"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/employees", response_model=List[Employee])
async def get_all_employees():
    """Get all employees in the database."""
    return rag_system.employees

@app.get("/employees/search")
async def search_employees(
    skills: str = None,
    min_experience: int = None,
    availability: str = None,
    department: str = None
):
    """Search employees with basic filters."""
    filtered_employees = rag_system.employees
    
    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        filtered_employees = [
            emp for emp in filtered_employees
            if any(skill.lower() in [s.lower() for s in emp["skills"]] for skill in skill_list)
        ]
    
    if min_experience:
        filtered_employees = [
            emp for emp in filtered_employees
            if emp["experience_years"] >= min_experience
        ]
    
    if availability:
        filtered_employees = [
            emp for emp in filtered_employees
            if emp["availability"].lower() == availability.lower()
        ]
    
    if department:
        filtered_employees = [
            emp for emp in filtered_employees
            if emp.get("department", "").lower() == department.lower()
        ]
    
    return {"employees": filtered_employees, "count": len(filtered_employees)}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "employees_loaded": len(rag_system.employees)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)