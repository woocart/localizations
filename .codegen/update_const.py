"""Generate const enums from WordPress API file to avoid human errors.

Usage: make codegen
"""

from pathlib import Path

import requests
import structlog

log = structlog.getLogger(__name__)

HEADER = '''\
"""WPLang definition constants."""
#  !!! This file is autogenerated !!!
#  !!! See .codegen/update_const.py for details. !!!

from typing import List


'''

# WPLang model
model = []
model.append("WPLANGS: List[str] = [")
model.append('  "en_US",  # WordPress base')
log.info("Fetching info")
res = requests.get("http://api.wordpress.org/translations/core/1.0/")
res.raise_for_status()
langs = res.json()["translations"]
for translation in langs:
    wplang = translation["language"]
    name = translation["english_name"]
    log.info("Adding", language=wplang, name=name)
    model.append(f'  "{wplang}",  # {name}')  # noqa: C408
model.append("]")
Path(".circleci/wplang.py").write_text(HEADER + "\n".join(model))
