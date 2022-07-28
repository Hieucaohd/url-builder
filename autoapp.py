from flask.helpers import get_debug_flag

from core.app import create_app
from core.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(CONFIG)
