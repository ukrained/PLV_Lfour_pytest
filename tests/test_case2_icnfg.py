import re
import subprocess


def test_case2_icnfg(setup_iface):
    """ test tap interface configuration """
    # cnfigure interface and get basic data
    (ifname, ip, ipv6, mtu) = setup_iface

    # compile command
    ifcnfg_cmd = f"ifconfig {ifname}"

    # get interface metadata from ifconfig
    res = subprocess.run(ifcnfg_cmd.split(), stdout=subprocess.PIPE)
    res.check_returncode()

    iface_info = res.stdout.decode() # decode from bytes

    # prepare regular expresions
    ptrns = [(r".*mtu\s(?P<mtu>[0-9]*).*", "mtu"),
             (r".*inet\s(?P<inet>[0-9\.]*).*", "inet"),
             (r".*inet6\s(?P<inet6>[0-9a-f\:\.]*).*", "inet6")]

    # expected values are the configured ones
    expected_values = {
        "mtu": mtu,
        "inet": ip,
        "inet6": ipv6
    }

    # compile and search each pattern in the info
    for ptrn, group_name in ptrns:
        pattern = re.compile(ptrn, re.MULTILINE)
        match = re.search(pattern, iface_info)

        if match:
            # check if match is correct
            print(f" # found {group_name} = {match.group(group_name)}")
            assert match.group(group_name) == expected_values[group_name]