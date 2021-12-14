#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import urllib.parse
import json
import requests

_gcfg = {
    "pops": {
        "global": ['TLV50-C2','BAH53-C1','DXB50-C1', 'FJR50-C1','FRA2-C1','FRA2-C2','FRA6-C1','FRA50-C1','FRA56-C2','FRA56-P4','FRA60-P1','FRA60-P3'],  # in case you find new edge-pop code
        "china": ['BJS9-E1', 'PVG52-E1', 'SZX51-E1', 'ZHY50-E1']  # the sources of edge-pop code for china
     },
    "http": True,   # enable http url
    "https": False,  # enable https url
    "china": False,  # in case china cloudfront
    "threads": 32,  # how many threads 
    "timeout": (3,3),  # url connection timeout
    "origin": "",   # origin domain(optional)
    "cname" : os.environ.get('alt_cname'),    # the alternative cname
    "action": "GET" # the http action
}

def cf_pops_domain_gen(origin):
    doaminparts = origin.split('.')
    distri = doaminparts[0]
    cfdomain = '.'.join(doaminparts[1:])
    return [distri+"."+ code.lower() +"."+cfdomain for code in _gcfg['pops']['global']];

def cf_url_gen(origin, urls):
    cfurls = []
    for dn in cf_pops_domain_gen(origin):
        if _gcfg['http']:
            cfurls += ["http://"+dn+u for u in urls]
        if _gcfg['https']:
            cfurls += ["https://"+dn+u for u in urls]
    return cfurls

def cf_pops_url_warmup(url):
    try:
        r = requests.request(_gcfg['action'], url, headers={"Host": _gcfg['cname']}, verify=False, timeout=_gcfg['timeout'])
        if r.status_code >= 400:
            print("warning: %s refreshing failing, ignore!!!"%url)
        else:
            print("SUCCESS: %s warmup done!"%url)
            print("headers: %s" % r.headers.get('X-Cache','header no fund'))
    except Exception as e:
        print("error: %s %s"%(str(e), url)) # didn't care the output
    return None

def cf_refresh_task(origin, urls):

    target_urls = cf_url_gen(origin, urls)
    for t in target_urls:
        cf_pops_url_warmup(t)

def lambda_handler(event, context):
    CF_CNAME = os.environ.get('cloudfront_cname')
    obj_key = event['Records'][0]['s3']['object']['key']
    obj_key = urllib.parse.unquote(obj_key)

    # submit to pre warm job
    cf_refresh_task(CF_CNAME, ['/' + obj_key])
