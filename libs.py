# validate github signature
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