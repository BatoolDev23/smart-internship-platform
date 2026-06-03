from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api.deps import current_user_id, db, require_role
from app.api.schemas import (
    CompanyOut,
    MatchBreakdown,
    RecommendationItem,
    RecommendationOut,
)
from app.core.exceptions import NotFoundError
from app.infra.db.models import Company, StudentProfile, University
from app.ml.matcher import CompanyVec, StudentVec, rank

router = APIRouter()


@router.get("/me", response_model=RecommendationOut)
async def recommend_for_me(
    session: Annotated[AsyncSession, Depends(db)],
    user_id: Annotated[int, Depends(current_user_id)],
    _: Annotated[str, Depends(require_role("student"))],
):
    profile = (
        await session.exec(select(StudentProfile).where(StudentProfile.user_id == user_id))
    ).first()
    if not profile:
        raise NotFoundError("Profile not found")

    uni_gov: str | None = None
    if profile.university_id:
        uni = await session.get(University, profile.university_id)
        if uni:
            uni_gov = uni.governorate

    companies = (await session.exec(select(Company))).all()

    student = StudentVec(
        skills=profile.skills or "",
        knowledge_areas=profile.knowledge_areas or "",
        major=profile.major or "",
        experience_years=profile.experience_years or 0,
        home_lat=profile.home_latitude,
        home_lng=profile.home_longitude,
        home_governorate=profile.home_governorate or "",
        university_governorate=uni_gov,
        university_id=profile.university_id,
    )

    cvecs = [
        CompanyVec(
            id=c.id,
            slug=c.slug,
            name=c.name_en,
            fields=c.fields,
            training_fields=c.training_fields,
            city=c.city,
            governorate=c.governorate,
            latitude=c.latitude,
            longitude=c.longitude,
            is_strategic_partner=c.is_strategic_partner,
        )
        for c in companies
    ]

    ranked = rank(student, cvecs)
    by_id = {c.id: c for c in companies}

    items: list[RecommendationItem] = []
    for r in ranked:
        c = by_id[r["company_id"]]
        items.append(
            RecommendationItem(
                company=CompanyOut.model_validate(c, from_attributes=True),
                internship=None,
                score=r["score"],
                distance_km=r["distance_km"],
                reasons=r["reasons"],
                breakdown=MatchBreakdown(**r["breakdown"]),
            )
        )

    return RecommendationOut(
        items=items,
        student_home={
            "lat": profile.home_latitude,
            "lng": profile.home_longitude,
            "city": profile.home_city,
        }
        if profile.home_latitude is not None
        else None,
    )
