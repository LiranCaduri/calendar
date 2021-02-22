from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from typing import List

from app.dependencies import get_db, SessionLocal
from app.database.models import UserFeature, Feature
from app.internal.security.dependancies import current_user
from app.internal.security.schema import UpdateFeatures, CurrentUser
from app.internal.security.ouath2 import create_jwt_token
from app.internal.utils import get_current_user
from app.internal.features import (
    create_user_feature_association,
    is_association_exists_in_db,
    get_user_features
)

router = APIRouter(
    prefix="/features",
    tags=["features"],
    responses={404: {"description": "Not found"}},
)


@router.get('/')
async def index(
    request: Request, session: SessionLocal = Depends(get_db)
) -> List:
    features = session.query(Feature).all()
    return features


@router.post('/add')
async def add_feature_to_user(
    request: Request,
    session: SessionLocal = Depends(get_db),
    user: str = Depends(current_user)
) -> UserFeature:
    form = await request.form()

    feat = session.query(Feature).filter_by(id=form['feature_id']).first()

    is_exist = is_association_exists_in_db(form=form, session=session)

    if feat is None or is_exist:
        # in case there is no feature in the database with that same id
        # and or the association is exist
        return False

    association = create_user_feature_association(
        db=session,
        feature_id=feat.id,
        user_id=user.id,
        is_enable=True
    )
    print('index', user)
    user = UpdateFeatures(
        user_id=user.user_id,
        username=user.username,
        features=get_user_features(
            session=session, user_id=user.user_id
        )
    )

    updated_features_token = create_jwt_token(user)
    response = Response(content=jsonable_encoder(association.__dict__))
    response.set_cookie(
        "Authorization",
        value=updated_features_token,
        httponly=True,
    )

    return response

from starlette.responses import RedirectResponse

@router.get('/update_features')
async def update_features(
        request: Request, db: SessionLocal = Depends(get_db), user: str =  Depends(current_user)):
    print("update features route: ", user.features)
    new_user = UpdateFeatures(user_id=user.user_id, username=user.username, features={'features': [1, 2, 3]})
    jwt_token = create_jwt_token(new_user)
    response = RedirectResponse(url="/new_features", status_code=302)
    response.set_cookie(
        "Authorization",
        value=jwt_token,
        httponly=True,
    )
    return response


@router.post('/delete')
async def delete_user_feature_association(
    request: Request,
    session: SessionLocal = Depends(get_db),
    user: str = Depends(current_user)
) -> bool:
    form = await request.form()

    user = get_current_user(session=session)
    feature_id = form['feature_id']

    is_exist = is_association_exists_in_db(form=form, session=session)

    if not is_exist:
        return False

    session.query(UserFeature).filter_by(
        feature_id=feature_id,
        user_id=user.id
    ).delete()
    session.commit()

    # resp = Response(content=jsonable_encoder('True'))
    # resp = create_cookie(response=resp, session=session)

    return True
