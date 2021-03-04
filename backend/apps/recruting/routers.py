from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from .models import Candidate, UpdateCandidateModel

router = APIRouter()


@router.post("/", response_description="Add new candidate")
async def create_task(request: Request, candidate: Candidate = Body(...)):
    candidate = jsonable_encoder(candidate)
    new_candidate = await request.app.mongodb["candidates"].insert_one(candidate)
    created_candidate = await request.app.mongodb["candidates"].find_one(
        {"_id": new_candidate.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_candidate)


@router.get("/", response_description="List all candidates")
async def list_candidates(request: Request):
    candidates = []
    for doc in await request.app.mongodb["candidates"].find().to_list(length=100):
        candidates.append(doc)
    return candidates


@router.get("/{id}", response_description="Get a single candidate from their id")
async def show_candidate(id: str, request: Request):
    if (candidate := await request.app.mongodb["candidates"].find_one({"_id": ObjectId(id)})) is not None:
        return candidate

    raise HTTPException(status_code=404, detail=f"Candidate {id} not found")

@router.get("/surname/{surname}", response_description="Get a single candidate from their surname")
async def show_candidate(surname: str, request: Request):
    if (candidate := await request.app.mongodb["candidates"].find_one({"name.surname": surname})) is not None:
        return candidate

    raise HTTPException(status_code=404, detail=f"Candidate {surname} not found")


@router.put("/{id}", response_description="Update a candidate")
async def update_candidate(id: str, request: Request, candidate: UpdateCandidateModel = Body(...)):
    candidate = {k: v for k, v in candidate.dict().items() if v is not None}

    if len(candidate) >= 1:
        update_result = await request.app.mongodb["candidates"].update_one(
            {"_id": id}, {"$set": candidate}
        )

        if update_result.modified_count == 1:
            if (
                updated_candidate := await request.app.mongodb["candidates"].find_one({"_id": id})
            ) is not None:
                return updated_candidate

    if (
        existing_candidate := await request.app.mongodb["candidates"].find_one({"_id": id})
    ) is not None:
        return existing_candidate

    raise HTTPException(status_code=404, detail=f"Candidate {id} not found")


@router.delete("/{id}", response_description="Delete Task")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb["candidates"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Candidate {id} not found")
