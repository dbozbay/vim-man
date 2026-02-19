import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def get_asset_path(*paths: str) -> str:
    return os.path.join(ASSETS_DIR, *paths)


def get_font_path(font_name: str) -> str:
    return get_asset_path("fonts", font_name)


def get_image_path(image_name: str) -> str:
    return get_asset_path("images", image_name)
