import os, glob
from software_program import SoftwareProgram

def get_software_list():
    prohibited_words = ['windows', 'install', 'setup', 'unins']
    software_full_paths = [path for path in glob.iglob('c:/**/*.exe', recursive=True) if all(word not in path.casefold() for word in prohibited_words)]
    software_list = []
    for index, path in enumerate(software_full_paths):
        name = os.path.basename(path)
        program_location = os.path.dirname(path)
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


