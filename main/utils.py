from httplib2 import Http
from lxml import etree

def lookup(lat, lng):
    h = Http()
    resp, content = h.request(
        "http://congress.mcommons.com/districts/lookup.xml?lat=%s&lng=%s" % (
            lat, lng))
    content = etree.fromstring(content)
    federal = "%s-%s" % (content.find("federal").find("state").text,
                         content.find("federal").find("district").text)
    state_upper = "%s-%s" % (content.find("state_upper").find("state").text,
                             content.find("state_upper").find("district").text)
    state_lower = "%s-%s" % (content.find("state_lower").find("state").text,
                             content.find("state_lower").find("district").text)

    return federal, state_upper, state_lower

