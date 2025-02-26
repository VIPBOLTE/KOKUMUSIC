import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AXeO80QwprAOOPWp8JaKtmejYsbpO5bSV1TU3zYqybXGOaZOPm8o3LeFbNdybYR6lzgj1eqNvVjZ9K943LQ3BnYBLbnb6orx6DuV_m3KqDMRLOxX_LbkAEgMc__Al9_NHaQuXjA01J6prtp4j58kTOULHMUxtZAkjPXvCfB61r4Tk4VyjKEdaCgYKAdESARESFQHGX2Min8LCgeASZOUlDFoPKRkmug0187",
    "expires": 1740612939.934953,
    "refresh_token": "1//0571wCZwVsXn3CgYIARAAGAUSNwF-L9IrSNNUc2qF2eHUyPN8p4EEVMSh-ck14K6hx0RPssFlp2uOLqL2JTfM6UGbSwNFm_liIt8",
    "token_type": "Bearer"
}

def vipboy():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
