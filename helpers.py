import routers

# this function returns the router object and the command string to run
# other router OS may be added to this dictionary in the same fashion, like IOS, SR-OS, etc.
def get_vars(router_name, cmd, ipprefix):
  for r in routers.routers_list:
    if router_name == r['address'][0]:
      router = r
  switcher = {
    'bgp': {
      'JunOS': 'show route protocol bgp {} table inet.0 detail'.format(ipprefix),
      'IOS-XR': 'show bgp ipv4 unicast {}'.format(ipprefix)
    },
    'traceroute': {
      'JunOS': 'traceroute {} wait 1'.format(ipprefix),
      'IOS-XR': 'traceroute {} timeout 1 probe 2'.format(ipprefix)
    },
    'ping': {
      'JunOS': 'ping {} count 5'.format(ipprefix),
      'IOS-XR': 'ping {} count 5'.format(ipprefix)
    }
  }
  command = switcher.get(cmd).get(router['type'])
  return router, command

