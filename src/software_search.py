import os, glob, win32api
from software_program import SoftwareProgram

def get_software_list():
    prohibited_words = ['windows', 'install', 'setup', 'unins', '$', '{', '}']
    software_paths = []

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        software_paths.extend(os.path.dirname(path) for path in glob.iglob("".join([drive[:2], '/**/*.exe']), recursive=True)
                                if all(word not in path.casefold() for word in prohibited_words))

    for index, path in enumerate(software_paths):
        if "\\bin" in path:
            bin_index = path.index("\\bin")
            path = path[:bin_index]
        if "\\Bin" in path:
            bin_index = path.index("\\Bin")
            path = path[:bin_index]
        software_paths[index] = path
    
    software_paths = list(software_paths)
    for index in range(len(software_paths)):
        while not os.path.basename(software_paths[index])[0].isalpha():
            software_paths[index] = os.path.dirname(software_paths[index])
    software_paths = set(software_paths)

    # while True:
    #     software_paths = list(software_paths)
    #     for index in range(len(software_paths)):
    #         while not os.path.basename(software_paths[index])[0].isalpha():
    #             software_paths[index] = os.path.dirname(software_paths[index])
    #     old_software_paths = set(software_paths)
    #     common_paths = set(subpath for subpath in software_paths if any(subpath in path and subpath != path for path in software_paths))
    #     software_paths = [path for path in software_paths if all(subpath not in path for subpath in common_paths)]
    #     software_paths.extend(common_paths)
    #     software_paths = set(software_paths)
    #     if old_software_paths == software_paths:
    #         break


    software_list = []
    for index, path in enumerate(set(software_paths)):
        name = os.path.basename(path)
        program_location = path
        license_location = get_license_location(program_location)
        software_list.append(SoftwareProgram(index + 1, name, program_location, license_location))
    
    return software_list

def get_software_list_from_file(drive):
    prohibited_words = ['windows', 'install', 'setup', 'unins', '$', '{', '}']
    software_paths = []
    software_paths.extend(os.path.dirname(path) for path in glob.iglob("".join([drive[:2], '/**/*.exe']), recursive=True)
                                if all(word not in path.casefold() for word in prohibited_words))

    for index, path in enumerate(software_paths):
        if "\\bin" in path:
            bin_index = path.index("\\bin")
            path = path[:bin_index]
        if "\\Bin" in path:
            bin_index = path.index("\\Bin")
            path = path[:bin_index]
        software_paths[index] = path
    
    # software_paths = list(software_paths)
    # for index in range(len(software_paths)):
    #     while not os.path.basename(software_paths[index])[0].isalpha():
    #         software_paths[index] = os.path.dirname(software_paths[index])
    
    # software_paths = set(software_paths)
    # while True:
    #     software_paths = list(software_paths)
    #     for index in range(len(software_paths)):
    #         while not os.path.basename(software_paths[index])[0].isalpha():
    #             software_paths[index] = os.path.dirname(software_paths[index])
    #     old_software_paths = set(software_paths)
    #     common_paths = set(subpath for subpath in software_paths if any(subpath in path and subpath != path for path in software_paths))
    #     software_paths = [path for path in software_paths if all(subpath not in path for subpath in common_paths)]
    #     software_paths.extend(common_paths)
    #     software_paths = set(software_paths)
    #     if old_software_paths == software_paths:
    #         break

    software_paths = list(set(software_paths))
    for index in range(len(software_paths)):
        while not os.path.basename(software_paths[index])[0].isalpha():
            software_paths[index] = os.path.dirname(software_paths[index])
    common_paths = set(subpath for subpath in software_paths if any(subpath in path and subpath != path for path in software_paths))
    software_paths = [path for path in software_paths if all(subpath not in path for subpath in common_paths)]
    software_paths.extend(common_paths)

    software_list = []
    for index, path in enumerate(set(software_paths)):
        name = os.path.basename(path)
        program_location = path
        license_location = get_license_location(program_location)
        software_list.append(SoftwareProgram(index + 1, name, program_location, license_location))
    
    return software_list


def get_license_location(directory):
    for folder in os.listdir(directory):
        dirfile = os.path.join(directory, folder)
        if os.path.isdir(dirfile):
            if 'license' in folder.casefold():
                return dirfile
    return ''

if __name__ == "__main__":
    software_list = get_software_list()
    
    for software in software_list:
        print(software.index, software.name, software.program_location, software.license_location)