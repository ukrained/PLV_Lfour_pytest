import os
import pytest
import subprocess


@pytest.fixture
def tc1_data():
    """ gives input data as a tuple """
    return ('trun', 'anyname.file', 'I like PyTest.')

@pytest.fixture
def setup_fs(tc1_data):
    """ setup direcroty and file for test case 1 """
    # getting input data
    dirname, filename, test_string = tc1_data

    # get target file path
    filepath = os.path.join(dirname, filename)

    # make directory
    print("# create directory")
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # fill the file
    if os.path.exists(dirname) and filename:
        with open(filepath, 'w') as fp:
            print("# create file and write content")
            fp.write(test_string)

    # return control
    yield (dirname, filepath, test_string)

    # remove file and dir
    os.remove(filepath)
    os.rmdir(dirname)


@pytest.fixture
def tc2_data():
    # note 1: be carefull with IPv6 address. ifconfig may output it in different way.
    # note 2: IPv6 mininal MTU is 1280. Otherwise IPv6 address flush from interface.
    return ('mytap0', '192.168.2.20', '24', '192.168.2.255', 'fe80::c0a8:214', '64', '2000') # ifname, ip, ipmask, ipbrd, ipv6, ipv6mask, mtu

@pytest.fixture
def setup_iface(tc2_data):
    """ setup tap interface for the test """
    # get initial data
    (ifname, ip, ipmask, ipbrd, ipv6, ipv6mask, mtu) = tc2_data

    # compile shell commands
    setup_commands_list = [
        f"sudo ip tuntap add dev {ifname} mode tap",
        f"sudo ip addr add {ip}/{ipmask} brd {ipbrd} dev {ifname}",
        f"sudo ip addr add {ipv6}/{ipv6mask} dev {ifname}",
        f"sudo ip link set dev {ifname} mtu {mtu}",
        f"sudo ip link set dev {ifname} up"
    ]

    teard_commands_list = [
        f"sudo ip tuntap del dev {ifname} mode tap"
    ]

    # run configuration
    for cmd in setup_commands_list:
        print(f" #> {cmd}")
        res = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
        assert res.returncode == 0

    # return control to test
    yield (ifname, ip, ipv6, mtu)

    # delete interface afterall
    for cmd in teard_commands_list:
        print(f" #> {cmd}")
        res = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
