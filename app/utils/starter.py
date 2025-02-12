import getpass
from app.services.user import UserService
from app.models.user import Users
from app.models.database import get_session
from app.config import settings
from app.utils.logger import log_info


def _prompt_for_password():
    while True:
        password = getpass.getpass("Enter a password for the admin user: ")
        confirm_password = getpass.getpass("Confirm the password: ")
        if password == confirm_password:
            return password
        print("Passwords do not match. Please try again.")


def insert_root_user():
    session = next(get_session())
    user_service = UserService(session)
    root_user = user_service.get_by_email(settings.root_user_email)
    if root_user:
        log_info("Root user already exists.")
        return

    log_info("Root user not found, creating one...")
    password = (
        _prompt_for_password()
        if not settings.root_user_password or settings.root_user_password == ""
        else settings.root_user_password
    )
    model = Users(
        email=settings.root_user_email,
        first_name="root",
        last_name="root",
        password=password,
    )
    user_service.create(model)
    log_info("Root user created.")
