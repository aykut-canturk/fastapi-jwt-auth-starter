# create fasapi app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# create FastAPI app
def create_app() -> FastAPI:
    app = FastAPI()

    # add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
