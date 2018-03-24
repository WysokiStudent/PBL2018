import errno, os, _winreg, re

proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()


if proc_arch == 'x86' or proc_arch == 'amd64':
    arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
else:
    raise Exception("Unhandled arch: %s" % proc_arch)


def checkRegEx(key):
    i = 0
    while(True):
        try:
            matchObj = re.match(r'(.*)[Nn][Aa][Mm][Ee](.*?).*',_winreg.EnumValue(key, i)[0])
            if(matchObj):
                return matchObj.group()
            else:
                i +=1
        except WindowsError:
            return False;


def goDeeper(key):
    numberOfSubkeys = _winreg.QueryInfoKey(key)[0]
    if(numberOfSubkeys == 0):
        value = checkRegEx(key)
        if (value):
            print _winreg.QueryValueEx(key, value)[0]
        return
    else:
        for i in xrange (0, numberOfSubkeys):
            subKey_name = _winreg.EnumKey(key, i)
            subKey = _winreg.OpenKey(key, subKey_name, 0, _winreg.KEY_READ)
            value = checkRegEx(subKey)
            if (value):
                print _winreg.QueryValueEx(subKey, value)[0], "   ", subKey_name
            goDeeper(subKey)


for arch_key in arch_keys:
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE", 0, _winreg.KEY_READ | arch_key)
    for i in xrange (0, _winreg.QueryInfoKey(key)[0]):
        goDeeper(key)




