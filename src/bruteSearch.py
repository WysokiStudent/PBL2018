import errno, os, re, time
import winreg as _winreg

proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()  # checking if the arch is 64x
proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()  # checking if arch is 86x

if proc_arch == 'x86' or proc_arch == 'amd64':
    arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
else:
    raise Exception("Unhandled arch: %s" % proc_arch)

stack = []  # initialisation of list which will store results
start = time.time()
stack_with_paths = []


def detect_irrelevant_result(program_name):
    global stack
    # list of symbols with which program name cannot start
    prohibited_symbols = ['%', '@', '!', '*', '$', '#', '[', '(', '-', '{']
    # very long list of prohibited phrases (all of them are listed as system functions)
    prohibited_words = ['Multimedia-Restricted', 'Microsoft-', 'Microsoft.', 'Networking-MPSSVC', 'Package_', \
                        'RemoteDesktopServices', 'Sensors-Universal-', 'Sensors-Universal-', 'Windows-Defender-', \
                        'WindowsSearchEngine', 'C:\Windows', 'HyperV-', 'LanguageFeatures', 'Adobe-Flash-For-', \
                        'Containers-ApplicationGuard', 'Power.Energy', 'System.', 'WVTA', 'DataMsg', 'SupportedName',\
                        'Cryptographic Provider', 'IndirectData', 'IndirectData', 'Signature', '.dll', '.exe' ]
    if program_name == '':
        return False
    if program_name[0] in prohibited_symbols or program_name[0].islower():  # checking if the first char is ok
        return False  # names starting from lover case were in all cases system functions
    if program_name.isdigit():  # non purely numeric name
        return False
    if program_name == 'None':  # sometimes the variable is name correctly, but cantains nothing
        return False
    for iterator in range (len(prohibited_words) - 1): # checking for system programs key words
        if prohibited_words[iterator] in program_name:
            return False
    return True  # if any of previous cases triggered return, that means that program name is ok


def pull_stack():
    global stack, start
    for x in range(len(stack) - 1):
        print(x, stack[x])  # printin results
    end = time.time()
    print('program work time:', end - start)  # printing time


def push_stack(program_name):
    global stack
    try:
        program_name = str(program_name)  # removing non-unicode chars (™)
    except UnicodeEncodeError:
        program_name = str(program_name.encode('ascii', 'ignore'))
    if not detect_irrelevant_result(program_name):  # calling functions which check if name is pottentialy correct
        return False
    if len(stack) < 1:  # if stack is empty the new variable can just be added without additional checking
        stack.append(str(program_name))
        return True
    x = len(stack) - 1
    while x != 0:  # checking stack from top, because identical results are in most cases near to each other
        if stack[x] == program_name:  # if there already is such entry on stack, it wont be duplicated
            return False
        else:
            x -= 1

    stack.append(str(program_name))  # if the function didn
    return True
    # now = time.time()
    # print stack_iterator, stack[len(stack) - 1], now - start


def check_reg_ex(key_to_check):
    iterator = 0
    number_of_subkeys_to_check = _winreg.QueryInfoKey(key_to_check)[1]  # getting how many variables are inside key
    for x in range(number_of_subkeys_to_check):
        # if _winreg.EnumValue(key_to_check, iterator)[0] == "Title":  # some directories store program names in title
        #     return "Title"
        match_obj = re.match(r'(.*)[Nn][a][m][e](.*?).*',
                             _winreg.EnumValue(key_to_check, iterator)[0])  # looking for variable with 'name' inside
        if match_obj:
            return match_obj.group()
        iterator += 1
    return False


def cut_the_string(path):
    last_slash = 0
    for iterator in range(len(path) - 1):
        if path[iterator] == '/':
            last_slash = iterator
    return path[:last_slash]


def append_with_path(key, value_name):
    global stack_with_paths, stack
    if value_name == 'DisplayIcon':
        stack_with_paths[-1] = stack[-1] + '  ' + cut_the_string((_winreg.QueryValueEx(key, value_name))[0])
    else:
        stack_with_paths[-1] = stack[-1] + '  ' + _winreg.QueryValueEx(key, value_name)[0]


def check_for_path(key):
    number_of_subkeys_to_check = _winreg.QueryInfoKey(key)[1]
    for iterator in range(number_of_subkeys_to_check):
        if _winreg.EnumValue(key, iterator)[0] == "Install Dir":
            append_with_path(key, 'Install Dir')
            break
        if _winreg.EnumValue(key, iterator)[0] == "InstallDirection":
            append_with_path(key, 'InstallDirection')
            break
        if _winreg.EnumValue(key, iterator)[0] == 'DisplayIcon':
            append_with_path(key, 'DisplayIcon')
        if _winreg.EnumValue(key, iterator)[0] == 'InstallLocation':
            append_with_path(key, 'InstallLocation')


def go_deeper(key):
    variable_name = check_reg_ex(key)  # calling fucntion which check the variables inside key
    if variable_name:
        if push_stack(_winreg.QueryValueEx(key, variable_name)[0]):  # passing the value from variable name to be pushed
            check_for_path(key)
    number_of_subkeys = _winreg.QueryInfoKey(key)[0]  # checks the number of subkeys inside key
    if number_of_subkeys == 0:  # if there is no subkeys, key is closed
        key.Close()
        return
    else:
        for i in range(0, number_of_subkeys):  # for every subkey this function is called again
            subKey_name = _winreg.EnumKey(key, i)  # obtaining name of n-th subkey
            try:
                subKey = _winreg.OpenKey(key, subKey_name, 0, _winreg.KEY_READ)  # trying to open it
                go_deeper(subKey)  # entering the subkey if opened
            except WindowsError:  # had to be added due to fact, that access to few keys in registry is restricted
                pass


for arch_key in arch_keys:
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE", 0, _winreg.KEY_READ | arch_key)
    for i in range(0, _winreg.QueryInfoKey(key)[0]):
        go_deeper(key)

pull_stack()
