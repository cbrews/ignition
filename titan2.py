# REPL init
import logging
logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

import titan2

sm = titan2.session_manager()
print(sm.start())