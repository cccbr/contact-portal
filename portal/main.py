""" FastAPI Server
"""
from __future__ import annotations

import os.path
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, Field

from portal import jiraclient


class FormDB(SQLModel):# pylint: disable=too-few-public-methods
    """ Form
    """
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    location: str = Field()
    age: str = Field()
    phone: str = Field()
    email: str = Field()
    existing: bool = Field()
    existing_experience: str = Field()
    confirm_data: bool = Field()
    allow_contact: bool = Field()


class FormData(BaseModel):# pylint: disable=too-few-public-methods
    """Data Model
    """
    name: str = Field()
    location: str = Field()
    needs: str = Field(default="")
    age: str = Field()
    phone: str = Field()
    email: str = Field()
    contactpref: str = Field()
    existing: bool = Field(default=False)
    existing_experience: str = Field(default="")
    confirm_data: bool = Field()
    allow_contact: bool = Field()


SQLITE_FILENAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILENAME}"
BASE = os.path.basename(os.path.dirname(__file__))
connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=connect_args)


async def create_db_and_tables():
    """Create Database
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_session():
    """Get Session
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# use base path
app.mount(
    "/static",
    StaticFiles(directory=f"{BASE}/static", follow_symlink=True, check_dir=False),
    name="static",
)

templates = Jinja2Templates(directory=f"{BASE}/templates")


@asynccontextmanager
async def lifespan(_app: FastAPI): # noqa
    """ Setup App

    :param app:
    :return:
    """
    await create_db_and_tables()
    yield


@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request):
    """ Render Generic Form
    """
    print("foo")
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/")
def submit_form(form_data: Annotated[FormData, Form()]):
    """ Process Form Submission
    """
    # Validate form

    # Send DB
    # Send Jira
    client = jiraclient.get_jira_client()
    if client:
        data = {
            "project": {"key": "ENQ"},
            "summary": f"Enquiry: {form_data.name}",
            "description": f"""
            First Name: {form_data.name}\n
            Location: {form_data.location}\n
            Needs: {form_data.needs}\n
            Phone: {form_data.phone}\n
            E-mail: {form_data.email}\
            Prefer: {form_data.contactpref}\n
            Age: {form_data.age}\n
            Previous: {form_data.existing}\n
            {form_data.existing_experience}\n
            """,
            "issuetype": {"name": "Task"},
        }
        client.create_issue(data)
    else:
        # Couldn't initialise Connection
        with open("contact.log", "a", encoding='utf-8') as fobj:
            fobj.write(form_data.name)

    # Confirm
    return 200
