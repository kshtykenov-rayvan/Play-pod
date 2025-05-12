from . import help
from . import start
from . import other

__all__ = ["help", "start", "other"]

def setup(dp):
    dp.include_router(help.router)
    dp.include_router(start.router)
    dp.include_router(other.router)