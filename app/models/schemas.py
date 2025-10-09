from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId

# Helper class to handle MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# ---------------------------
# Resume Schema
# ---------------------------
class Resume(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    email: EmailStr
    skills: List[str]
    education: Optional[str] = None
    experience: Optional[str] = None
    salary_expectations: Optional[str] = None
    file_path: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Job Post Schema
# ---------------------------
class JobPost(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    title: str
    company: str
    description: str
    required_skills: List[str]
    min_experience: Optional[int] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


# ---------------------------
# Bifurcation Result Schema
# ---------------------------
class BifurcationResult(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    resume_id: str
    parsed_skills: List[str]
    parsed_education: Optional[str] = None
    parsed_experience: Optional[str] = None
    parsed_salary_expectations: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
