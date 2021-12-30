from dataIO import fileIO
import os

false_strings = ["false", "False", "f", "F", "0", ""]

if fileIO("config.json", "check"):
    config = fileIO("config.json", "load")
else:
    config = {
        "lucha_floor_token_id": os.environ["LUCHA_FLOOR_TOKEN_ID"],
        "lucha_icon_url": os.environ["LUCHA_ICON_URL"],
        "opensea_api_key": os.environ["OPENSEA_API_KEY"],
        "embedded_description": os.environ["EMBEDDED_DESCRIPTION"]
    }