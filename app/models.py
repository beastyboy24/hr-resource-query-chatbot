from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
    email: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None

class ChatQuery(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    relevant_employees: List[Employee]
    confidence_score: Optional[float] = None