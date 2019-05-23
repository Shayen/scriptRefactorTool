import os
import json

import constant
import model

def getModel():
    if not os.path.exists():
        with open(constant.CONFIG_FILE, 'w') as f:
            json.dump(constant.DEFAULT_MODEL, f, indent=2)
    model.Model(constant.CONFIG_FILE)