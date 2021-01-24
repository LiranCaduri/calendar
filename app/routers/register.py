from app.internal import user
from app.database import schemas
from app.database.database import get_db
from app.dependencies import templates
from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="",
    tags=["register"],
    responses={404: {"description": "Not found"}},
)


@router.get("/register")
async def register_user_form(request: Request) -> templates:
    '''
    rendering register route get method
    '''
    return templates.TemplateResponse("register.html", {
        "request": request,
        "errors": None
    })


@router.post("/register")
async def register(
                request: Request, db: Session = Depends(get_db)) -> templates:
    '''
    rendering register route post method.
    '''
    form = await request.form()
    form_dict = dict(form)
    try:
        # creating pydantic schema object out of form data

        new_user = schemas.UserCreate(**form_dict)
    except ValidationError as e:
        # if pydantic validations fails, rendering errors to register.html

        errors = {error['loc'][0]: " ".join((
            error['loc'][0].capitalize(),
            error['msg'])) for error in e.errors()}
        return templates.TemplateResponse("register.html", {
            "request": request,
            "errors": errors,
            "form_values": form_dict})
    try:
        # attempt creating User Model object, and saving to database

        user.create(db=db, user=new_user)

        '''
        if creating User Model objects fails due to registered unique details -
        rendering errors to register.html
        '''
    except IntegrityError:
        db.rollback()
        errors = {}
        db_user_email = user.get_by_mail(db, email=new_user.email)
        db_user_username = user.get_by_username(
            db, username=new_user.username)
        if db_user_username:
            errors['username'] = "That username is already taken"
        if db_user_email:
            errors['email'] = "Email already registered"
        return templates.TemplateResponse("register.html", {
            "request": request,
            "errors": errors,
            "form_values": form_dict})

    return templates.TemplateResponse("home.html", {
        "request": request,
        "message": "User created",
        "status_code": 201})
