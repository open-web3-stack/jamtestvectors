#!/usr/bin/env python

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, '../../lib')))

from validate_asn1 import validate_group  # noqa: E402

os.chdir(script_dir)

# Makes the SEQUENCE of OPTIONAL values ASN.1 compliant (using CHOICE)
def tweak_sequence_of_options(state_obj):
    items = state_obj['rho']
    for i in range(len(items)):
        if items[i] is None:
            items[i] = {"none": None}
        else:
            items[i] = {"some": items[i]}
    return state_obj

def tweak_callback(json_obj):
    tweak_sequence_of_options(json_obj['pre_state'])
    tweak_sequence_of_options(json_obj['post_state'])
    return json_obj

for spec in ["tiny", "full"]:
    validate_group("disputes", "disputes.asn", spec, tweak_callback)
