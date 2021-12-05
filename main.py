import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_contrib.common.middlewares import StateRequestIDMiddleware
from fastapi_contrib.exception_handlers import setup_exception_handlers
from fastapi_contrib.routes import ValidationErrorLoggingRoute
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.datastructures import CommaSeparatedStrings
from fastapi_contrib.tracing.middlewares import OpentracingMiddleware
from fastapi_contrib.tracing.utils import setup_opentracing

from core import config
from core.EventsHandling import events
from core.endpoints.api_route import router
from pydantic import BaseConfig


def get_application():
    """
    Get FastAPI Application for service.
    """

    app = FastAPI(title=config.settings.project_name, version=config.settings.version)

    if not config.settings.allowed_hosts:
        ALLOWED_HOSTS = ["*"]
    else:
        ALLOWED_HOSTS = CommaSeparatedStrings(config.settings.allowed_hosts)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    BaseConfig.validate_all= False
    BaseConfig.arbitrary_types_allowed=True
    app.add_middleware(
        StateRequestIDMiddleware,
    )
    setup_exception_handlers(app)
    
    app.add_event_handler("startup", events.create_start_app_handler(app))
    app.add_event_handler("shutdown", events.create_stop_app_handler(app))
    app.router.route_class = ValidationErrorLoggingRoute
    setup_opentracing(app)
    app.add_middleware(OpentracingMiddleware)
    app.include_router(router, prefix=f"{config.settings.api_prefix }/v1")

    return app


app = get_application()
router = InferringRouter()


@cbv(router)
class RunModel:    
    @router.get("/")
    async def index(self):
        return {"message": "Hello"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
