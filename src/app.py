import sys
import whois

def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def all_registered_domain(domain_name: str, tlds: list):
    resp = {
      "registered":[],
    }

    for tld in tlds:
        if is_registered(domain_name+'.'+tld):
            resp["registered"].append(domain_name+'.'+tld)

    return resp


### allocations

if len(sys.argv)<2:sys.exit()

tlds = []

with open("config/tlds.txt", 'r') as f:
    for tld in f:
        tlds.append(tld.strip())


domain_check_status = all_registered_domain(
    domain_name=sys.argv[1],
    tlds=tlds
)

if domain_check_status["registered"]:
    registered_domain_dump_filename = "dump/"+sys.argv[1]+"_registered_tlds.txt"
    with open(registered_domain_dump_filename, "w") as f:
        f.write('\n'.join(domain_check_status["registered"]))
    print(sys.argv[1]+f" : {len(domain_check_status['registered'])} TLDs are registered with the supplied Domain Name")
    print(sys.argv[1], ": Registered Domains are dumped at", registered_domain_dump_filename)
else:
    print(sys.argv[1]+f" : No Domains are registered with the {len(tlds)} supplied TLDs")
