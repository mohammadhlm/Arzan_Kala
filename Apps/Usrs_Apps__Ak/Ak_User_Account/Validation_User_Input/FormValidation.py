import re
# Google Recaptcha Module
import json
import urllib
from Arzan_Kala import settings


def FullnameValidation(Fullname):
    if re.search(".*[^A-Za-z\s].*", str(Fullname)):
        return False
    else:
        return True


def PasswordValidation(Password):
    if re.search("^(?=.*[0-9]$)(?=.*[a-zA-Z])", str(Password)) is None:
        return False
    else:
        return True


def EmailValidation(Email):
    ListOfPopularEmail = [
        "gmail.com", "yahoo.com", "hotmail.com", "aol.com", "hotmail.co.uk", "hotmail.fr", "msn.com",
        "yahoo.fr", "wanadoo.fr", "orange.fr", "comcast.net", "yahoo.co.uk", "yahoo.com.br",
        "yahoo.co.in", "live.com", "rediffmail.com", "free.fr", "gmx.de", "web.de", "yandex.ru", "ymail.com",
        "libero.it", "outlook.com", "uol.com.br", "bol.com.br", "mail.ru", "cox.net", "hotmail.it", "sbcglobal.net",
        "sfr.fr", "live.fr", "verizon.net", "live.co.uk", "googlemail.com", "yahoo.es", "ig.com.br", "live.nl",
        "bigpond.com", "terra.com.br", "yahoo.it", "neuf.fr", "yahoo.de", "alice.it", "rocketmail.com",
        "att.net", "laposte.net", "facebook.com", "bellsouth.net", "yahoo.in", "hotmail.es", "charter.net",
        "yahoo.ca", "yahoo.com.au", "rambler.ru", "hotmail.de", "tiscali.it", "shaw.ca", "yahoo.co.jp",
        "sky.com", "earthlink.net", "optonline.net", "freenet.de", "t-online.de", "aliceadsl.fr", "arcor.de"
                                                                                                  "virgilio.it",
        "home.nl", "qq.com", "telenet.be", "me.com", "yahoo.com.ar", "tiscali.co.uk",
        "yahoo.com.mx", "voila.fr", "gmx.net", "mail.com", "planet.nl", "tin.it", "live.it", "ntlworld.com",
        "yahoo.co.id", "frontiernet.net", "hetnet.nl", "live.com.au", "yahoo.com.sg", "zonnet.nl", "club-internet.fr",
        "juno.com", "optusnet.com.au", "blueyonder.co.uk"
    ]
    if re.search('(.*[^\w\d\-\.@].*)', Email) is None:
        for Domain in ListOfPopularEmail:
            if re.search("(^[\w\d\.\s]+@{}$)".format(Domain.replace('.', '\.')), str(Email).strip()):
                return True
    else:
        return False
    return False


def RecaptchaValidation(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result["success"]
