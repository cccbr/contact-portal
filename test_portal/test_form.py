import re
from playwright.sync_api import Page, expect


def test_portal_form(page: Page):
    """Test Submit of User form with required data"""
    page.set_default_timeout(900)
    page.goto("http://127.0.0.1:8000/form")
    expect(page).to_have_title(re.compile("We All Bellringing - Join Bellringing"))
    page.get_by_label("Name:").fill("Joe Bloggs")
    page.get_by_label("Location:").fill("Somewhere")
    # page.get_by_label("Supportive Needs").fill("None")
    page.get_by_label("Age").select_option("30-50")
    page.get_by_label("Phone No.").fill("1234")
    page.get_by_label("E-mail", exact=True).fill("joe@example.com")
    page.get_by_label("Preferred Contact").select_option("E-mail")
    page.get_by_label(
        "Have you any previous experience of ringing?", exact=True
    ).check()
    page.get_by_label("Previous Experience Detail", exact=True).fill("Maybe")
    page.get_by_label(
        "Are you happy for us and trusted partners to contact you?"
    ).check()
    page.get_by_label(
        "Are you happy for us to store your personal information?"
    ).check()
    page.get_by_role("button", name=re.compile("send", re.IGNORECASE)).click()
