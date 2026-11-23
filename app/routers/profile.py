from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from app.deps import CurrentUser, SessionDep
from app.models import Profile
from app.schemas import ProfileIn, ProfileOut
from app.services.nutrition import calculate_targets

router = APIRouter(prefix="/api/profile", tags=["profile"])


def to_out(profile: Profile) -> ProfileOut:
    return ProfileOut(
        sex=profile.sex,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        activity_level=profile.activity_level,
        goal=profile.goal,
        targets=calculate_targets(profile).to_dict(),
    )


@router.get("", response_model=ProfileOut)
def get_profile(user: CurrentUser, session: SessionDep):
    profile = session.get(Profile, user.id)
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profile not set up yet")
    return to_out(profile)


@router.put("", response_model=ProfileOut)
def upsert_profile(data: ProfileIn, user: CurrentUser, session: SessionDep):
    profile = session.get(Profile, user.id)
    if profile is None:
        profile = Profile(user_id=user.id, **data.model_dump())
    else:
        for key, value in data.model_dump().items():
            setattr(profile, key, value)
        profile.updated_at = datetime.now(UTC)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return to_out(profile)
