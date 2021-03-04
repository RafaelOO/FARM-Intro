from typing import Optional, Dict, List, Union
import uuid
from pydantic import BaseModel, Field
from datetime import datetime
import pydantic
from bson.objectid import ObjectId 
from fastapi.encoders import jsonable_encoder

class PydanticObjectId(ObjectId):
    # fix for FastApi/docs
    __origin__ = pydantic.typing.Literal
    __args__ = (str, )
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    # @classmethod
    # def __modify_schema__(cls, field_schema):
    #     field_schema.update(type='string')

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
pydantic.json.ENCODERS_BY_TYPE[PydanticObjectId]=str

class Name(BaseModel):
    firstname: str =Field(...)
    surname: str =Field(...)

class Interview(BaseModel):
    interviewer: Optional[str]
    date:Optional[str]
    company:Optional[str]
    notes:Optional[str]
    passed:Optional[bool]

class Salary(BaseModel):
    min:Optional[int]
    max:Optional[int]
    comments:Optional[str]

class Initial_Interview(Interview):
   salary_expectation: Optional[Salary]
   notice_period:Optional[int]


class InterViewHistory(BaseModel):
    initial_interview:Optional[Initial_Interview]
    techinical_interview:Optional[Interview]
    client_interviews:Optional[List[Interview]]

class Status(BaseModel):
    recruting: Optional[str]
    work_with_us:Optional[bool]
    available:Optional[bool]

class Comments(BaseModel):
    author: str
    comment: str
    timestamp:datetime
    phase:str

class DocumentationBasic(BaseModel):
    file:Optional[str]
    submitted:Optional[datetime]
    client: Optional[str]

class Documentation(BaseModel):
    cv:Optional[DocumentationBasic]
    matrix:Optional[DocumentationBasic]

class WorkWithUs(BaseModel):
    company_name:Optional[str]
    from_: Optional[str]
    to:Optional[str]
    role:Optional[str]
    level:Optional[int]
     

class Candidate(BaseModel):
    id: PydanticObjectId = Field(description="User id", alias='_id')
    name: Name
    # completed: bool = False
    email: Optional[str]
    linkedin: Optional[str]
    telephone: Optional[str]
    english: Optional[str]
    first_contact: Optional[Dict[str, str]]
    current_last_job: Optional[Dict[str, str]]
    skills: Optional[Dict[str, int]]
    profile: Optional[Dict[str, int]]
    jobs_history: Optional[List[Dict[str, str]]]
    # comments: Optional[List[Dict[str, Union[datetime, str]]]]
    comments: Optional[List[Comments]]
    interview_history:Optional[InterViewHistory]
    status:Status
    documentation: Documentation
    work_with_us:Optional[List[WorkWithUs]]
    # class Config:
    #     allow_population_by_field_name = True
    #     schema_extra = {
    #         "example": {
    #             "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
    #             "name": "My important task",
    #             "completed": True,
    #         }
    #     }
    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         ObjectId: str
    #     }
    # class Config:
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: lambda x: str(x)}
    class Config:
        fields = {'id': '_id'}

class UpdateCandidateModel(BaseModel):
    name: Optional[Name]
    email: Optional[str]
    linkedin: Optional[str]
    telephone: Optional[str]
    english: Optional[str]
    first_contact: Optional[Dict[str, str]]
    current_last_job: Optional[Dict[str, str]]
    skills: Optional[Dict[str, int]]
    profile: Optional[Dict[str, int]]
    jobs_history: Optional[List[Dict[str, str]]]
    comments: Optional[List[Dict[str, str]]]
    interview_history:Optional[InterViewHistory]
    status:Optional[Status]
    documentation: Optional[Documentation]
    work_with_us:Optional[List[WorkWithUs]]

    class Config:
        fields = {'id': '_id'}
