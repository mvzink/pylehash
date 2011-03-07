#!/usr/bin/env python

from pylehash import get_switch_from_args, run_switch

if __name__ == '__main__':
    port, switch = get_switch_from_args()
    run_switch(port, switch)
