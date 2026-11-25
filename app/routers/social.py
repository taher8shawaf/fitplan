"""Following friends and seeing their workouts.

Privacy rules:
- Emails are never shown or searchable; people find each other by @username or name.
- A private user's workouts are hidden from everyone but themselves.
"""

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, col, func, or_, select

from app.deps import CurrentUser, SessionDep
from app.models import Follow, User, WorkoutLike, WorkoutLog
from app.schemas import FeedItem, ProfileView, PublicUser, SocialSettingsIn, UserOut
from app.services.social import normalize_username, valid_username, workout_summary

router = APIRouter(tags=["social"])
NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, "User not found")


# ---------- helpers ----------
def count(session: Session, stmt) -> int:
    return session.exec(select(func.count()).select_from(stmt.subquery())).one()


def is_following(session: Session, follower_id: int, followee_id: int) -> bool:
    return session.get(Follow, (follower_id, followee_id)) is not None


def public_user(session: Session, me: User, other: User) -> PublicUser:
    return PublicUser(
        username=other.username,
        name=other.name,
        is_following=is_following(session, me.id, other.id),
        follows_you=is_following(session, other.id, me.id),
        followers=count(session, select(Follow).where(Follow.followee_id == other.id)),
        following=count(session, select(Follow).where(Follow.follower_id == other.id)),
    )


def user_by_username(session: Session, username: str) -> User:
    user = session.exec(select(User).where(User.username == normalize_username(username))).first()
    if not user:
        raise NOT_FOUND
    return user


def can_see_workouts(me: User, owner: User) -> bool:
    return owner.id == me.id or not owner.is_private


def feed_item(session: Session, me: User, log: WorkoutLog, owner: User) -> FeedItem:
    likes = count(session, select(WorkoutLike).where(WorkoutLike.workout_log_id == log.id))
    return FeedItem(
        id=log.id,
        user=public_user(session, me, owner),
        day=log.day,
        created_at=log.created_at,
        likes=likes,
        liked_by_me=session.get(WorkoutLike, (me.id, log.id)) is not None,
        is_mine=owner.id == me.id,
        **workout_summary(session, log),
    )


# ---------- my settings ----------
@router.patch("/api/me/social", response_model=UserOut)
def update_social_settings(data: SocialSettingsIn, user: CurrentUser, session: SessionDep):
    if data.username is not None:
        username = normalize_username(data.username)
        if not valid_username(username):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Username: 3-20 letters, numbers, _ or .")
        taken = session.exec(select(User).where(User.username == username, User.id != user.id)).first()
        if taken:
            raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
        user.username = username
    if data.is_private is not None:
        user.is_private = data.is_private
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOut(id=user.id, email=user.email, name=user.name, username=user.username, is_private=user.is_private)


# ---------- people ----------
@router.get("/api/users/search", response_model=list[PublicUser])
def search_users(user: CurrentUser, session: SessionDep, q: str = Query(min_length=2, max_length=40)):
    term = normalize_username(q)
    results = session.exec(
        select(User)
        .where(
            User.id != user.id,
            or_(col(User.username).startswith(term), col(User.name).ilike(f"%{q.strip()}%")),
        )
        .limit(20)
    )
    return [public_user(session, user, u) for u in results]


@router.get("/api/users/me/following", response_model=list[PublicUser])
def my_following(user: CurrentUser, session: SessionDep):
    rows = session.exec(
        select(User).join(Follow, col(Follow.followee_id) == col(User.id)).where(Follow.follower_id == user.id)
    )
    return [public_user(session, user, u) for u in rows]


@router.get("/api/users/me/followers", response_model=list[PublicUser])
def my_followers(user: CurrentUser, session: SessionDep):
    rows = session.exec(
        select(User).join(Follow, col(Follow.follower_id) == col(User.id)).where(Follow.followee_id == user.id)
    )
    return [public_user(session, user, u) for u in rows]


@router.get("/api/users/{username}", response_model=ProfileView)
def view_profile(username: str, user: CurrentUser, session: SessionDep):
    other = user_by_username(session, username)
    visible = can_see_workouts(user, other)
    logs = (
        list(
            session.exec(
                select(WorkoutLog)
                .where(WorkoutLog.user_id == other.id)
                .order_by(col(WorkoutLog.day).desc(), col(WorkoutLog.id).desc())
                .limit(10)
            )
        )
        if visible
        else []
    )
    return ProfileView(
        user=public_user(session, user, other),
        is_me=other.id == user.id,
        is_private=other.is_private,
        workouts_count=count(session, select(WorkoutLog).where(WorkoutLog.user_id == other.id)) if visible else None,
        workouts=[feed_item(session, user, log, other) for log in logs],
    )


@router.post("/api/users/{username}/follow", status_code=status.HTTP_204_NO_CONTENT)
def follow(username: str, user: CurrentUser, session: SessionDep):
    other = user_by_username(session, username)
    if other.id == user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You can't follow yourself")
    if not is_following(session, user.id, other.id):
        session.add(Follow(follower_id=user.id, followee_id=other.id))
        session.commit()


@router.delete("/api/users/{username}/follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(username: str, user: CurrentUser, session: SessionDep):
    other = user_by_username(session, username)
    link = session.get(Follow, (user.id, other.id))
    if link:
        session.delete(link)
        session.commit()


# ---------- feed ----------
@router.get("/api/feed", response_model=list[FeedItem])
def feed(
    user: CurrentUser,
    session: SessionDep,
    limit: int = Query(20, ge=1, le=50),
    before_id: int | None = Query(None, description="for paging: return workouts older than this id"),
):
    """Your workouts plus those of people you follow (unless they're private), newest first."""
    followed = select(Follow.followee_id).where(Follow.follower_id == user.id)
    stmt = (
        select(WorkoutLog, User)
        .join(User, col(User.id) == col(WorkoutLog.user_id))
        .where(
            or_(
                WorkoutLog.user_id == user.id,
                (col(WorkoutLog.user_id).in_(followed)) & (User.is_private == False),  # noqa: E712
            )
        )
        .order_by(col(WorkoutLog.id).desc())
        .limit(limit)
    )
    if before_id is not None:
        stmt = stmt.where(WorkoutLog.id < before_id)
    return [feed_item(session, user, log, owner) for log, owner in session.exec(stmt)]


def visible_log(session: Session, user: User, log_id: int) -> WorkoutLog:
    log = session.get(WorkoutLog, log_id)
    if not log:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    owner = session.get(User, log.user_id)
    if not can_see_workouts(user, owner):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return log


@router.post("/api/workouts/logs/{log_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def like(log_id: int, user: CurrentUser, session: SessionDep):
    visible_log(session, user, log_id)
    if session.get(WorkoutLike, (user.id, log_id)) is None:
        session.add(WorkoutLike(user_id=user.id, workout_log_id=log_id))
        session.commit()


@router.delete("/api/workouts/logs/{log_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike(log_id: int, user: CurrentUser, session: SessionDep):
    like_row = session.get(WorkoutLike, (user.id, log_id))
    if like_row:
        session.delete(like_row)
        session.commit()
