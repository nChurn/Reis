import linecache
import sys
import traceback
import logging
logger = logging.getLogger(__name__)

def PrintException():
    print(traceback.format_exc())
