# -*- coding: utf-8 -*-
"""
Simple module that sends a GET request to https://api.ipify.org,
retrieving the WAN IP_v4 address to dipslay to the i3bar via py3status.
Any click on the module from a mouse button (right/left/middle/etc.)
will copy the address to clipboard.

Configuration parameters:
    sync_to_val: Unit-block of time that wan_check should sync to. Default
        value is 3600 seconds (3600s = 1h). The py3status .sync_to() function
        will read this as "at the beginning of every hour". A value of 900 for
        instance would occur every fifteen minutes, at :15, :30, :45, :00
    format: Simple display format for this module. Only one placeholder so not much
        to be done here unless you want to change/remove the string printed with it.
        (Default 'wan: {ip}') 
    url: The url to point the request at. This realies heavily on ipify.org continuing
        their support of their IPv4 API page.

Format placeholders:
    {ip} wan ipv4 address

@author Christopher Carlsen https://celticchristoph.github.io
@license BSD

SAMPLE OUTPUT
{'full_text': 'wan: 255.255.255.255', 'color': '#00FF00', 'cached_until': 1541826720.0}
"""
import requests
import time

class Py3status:
    """
    """

    # Config params
    sync_to_val = 3600
    format = 'wan: {ip}'
    url = 'https://api.ipify.org/'
    
    def on_click(self, event):
        clean_string = self.ip['ip'].rstrip('\r\n')
        self.py3.command_output("printf \"" + clean_string + "\" | xsel --clipboard", True)

    def wan_check(self):
        payload = {'format': 'json'}
        r = requests.get(self.url, params=payload)
        
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.cache_timeout = 10
            color = self.py3.COLOR_BAD
            self.ip =  {'ip':'n/a'}
        
        self.cache_timeout = 14400
        color = self.py3.COLOR_GOOD
        self.ip = r.json()
        
        # Used to ensure that the API wasn't being spammed
        # by continuous calls when this Module is running.
        #ip = {'ip': int(time.time())}

        return {'cached_until': self.py3.time_in(sync_to=self.sync_to_val),
                'full_text': self.py3.safe_format(self.format, self.ip),
                'color': color}

if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
