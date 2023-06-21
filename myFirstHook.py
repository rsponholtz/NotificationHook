"""
# SAPHana hook sample
# License:      GNU General Public License (GPL)
# this is a sample script with no guarantees of fitness for any purpose
# and it needs to be updated with your own behavior to be executed
# on HANA failover
# Copyright:    (c) 2015-2016 SUSE Linux GmbH
# Copyright:    (c) 2017-2022 SUSE LLC
"""
try:
    from hdb_ha_dr.client import HADRBase
except ImportError as e:
    print("Module HADRBase not found - running outside of SAP HANA? - {0}".format(e))
    import os

"""
To use this HA/DR hook provide please:
1) create directory /usr/shared/myHooks, which should be owned by <sid>adm
2) copy this file to /usr/shared/myHooks
3) add the following lines to your global.ini:
[ha_dr_provider_myfirsthook]
provider = myFirstHook
path = /hana/shared/myHooks
execution_order = 5

4) create the directory /srhook, writable by <sid>adm

please see documentation on HANA hooks here:
https://help.sap.com/docs/SAP_HANA_PLATFORM/6b94445c94ae495c83a19646e7c3fd56/1367c8fdefaa4808a7485b09815ae0f3.html?version=2.0.01
"""
fhSRHookVersion = "0.162.0"

try:
    class myFirstHook(HADRBase):

        def __init__(self, *args, **kwargs):
            # delegate construction to base class
            super(myFirstHook, self).__init__(*args, **kwargs)
            self.tracer.info("myFirstHook init()")
                
        def about(self):
            return {"provider_company": "SAMPLE",
                       "provider_name": "myFirstHook",  # class name
                "provider_description": "Execute after takeover",
                    "provider_version": "1.0"}
                                                                                                                     
        def postTakeover(self, rc, **kwargs):
            """
            Hook description:
            * time of call: as soon as all services with a volume return from their
              assign-call (open SQL port)
            * caller: the master host
            * landscape: called only once on the master
            * behavior upon failure: error trace is written

            @param rc: the return code of the actual takeover process; 0=success,
                       1=waiting for forced takeover, 2=failure
            @type rc: int
            @param **kwargs: place holder for later usage (new parameters) to
                   keep the interface stable
            @type **kwargs: dict
            @return: information about success
            @rtype: int

            ***this is strictly a sample, and you will need to implement your own ***
            ***logic here***
            """
            with open('/srhook/readme.txt', 'a') as f:
                f.write("HANA failed over to secondary node")
                f.write('\n')
            return 0
except NameError as e:
    print("Could not find base class ({0})".format(e))
