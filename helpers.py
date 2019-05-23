import os
import json

import constant
import model

def getModel():
    if not os.path.exists(constant.CONFIG_FILE):
        with open(constant.CONFIG_FILE, 'w') as f:
            json.dump(constant.DEFAULT_MODEL, f, indent=2)
    return model.Model(constant.CONFIG_FILE)