import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

INSTANCE_PATH = os.path.join(
    BASE_DIR,
    "instance"
)

# create folder automatically
if not os.path.exists(INSTANCE_PATH):
    os.makedirs(INSTANCE_PATH)


class Config:
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            INSTANCE_PATH,
            "database.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False