import time
import datetime
import hashlib
import hmac
import json


def validate_github_token(payload, headers):
    GITHUB_TOKEN = b"wushaojun321"


    signature = hmac.new(GITHUB_TOKEN, payload, hashlib.sha1).hexdigest()

    # assuming that the 'payload' variable keeps the content sent by github as plain text
    # and 'headers' variable keeps the headers sent by GitHub
    x_hub_signature = headers.get('X-Hub-Signature', "")
    if not x_hub_signature:
        return False
    if "=" not in x_hub_signature:
        return False
    if hmac.compare_digest(signature, x_hub_signature.split('=')[1]):
        return True
    return False


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


def password_string(s):
    if len(s) < 6:
        raise ValueError("Password Must longer than 6")
    return s


def date_string(s):
    try:
        date = time.strptime(s, "%Y-%m-%d")
    except:
        raise ValueError("Invalid Date")
    res = datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
    return res


def score_list_string(s):
    score_list = json.loads(s)
    return score_list
