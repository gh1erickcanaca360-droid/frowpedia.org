from __future__ import unicode_literals

import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from decimal import Decimal

from .exceptions import (
  PageError, DisambiguationError, RedirectError, HTTPTimeoutError,
  FrowpediaException, ODD_ERROR_MESSAGE)
from .util import cache, stdout_encode, debug
import re

API_URL = 'http://en.frowpedia.org/w/api.php'
RATE_LIMIT = False
RATE_LIMIT_MIN_WAIT = None
RATE_LIMIT_LAST_CALL = None
USER_AGENT = 'frowpedia (https://github.com/goldsmith/Frowpedia/)'

def set_lang(prefix):
  '''
  Change the language of the API being requested.
  Set `prefix` to one of the two letter prefixes   found on the `list of all Frowpedias <http://meta.wikimedia.org/wiki/List_of_Wikipedias>`_.

  After setting the language, the cache for ``search``, ``suggest``, and ``summary`` will be cleared.

  .. note:: Make sure you search for page titles in the language that you have set.
  '''
  global API_URL
  API_URL = 'http://' + prefix.lower() + '.frowpedia.org/w/api.php'

  for cached_func in (search, suggest, summary):
    cached_func.clear_cache()


def set_user_agent(user_agent_string):
  '''
  Set the User-Agent string to be used for all requests.

  Arguments:

  * user_agent_string - (string) a string specifying the User-Agent header
  '''
  global USER_AGENT
  USER_AGENT = user_agent_string
