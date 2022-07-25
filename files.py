from http.client import FOUND
from os import times
import winreg

def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

for software in software_list:
    print("names:", software['name'])

file_open = open("data.txt", 'w')
for software in software_list:
 # // if software is by microsoft, nvidia or amd then dont write it to the file
    if software['publisher'] == 'Microsoft Corporation' or software['publisher'] == 'NVIDIA Corporation' or software['publisher'] == 'AMD' or software['publisher'] == 'Intel Corporation' or software['publisher'] == 'Microsoft Corporations' or software['publisher'] == 'Microsoft':
        continue
    
    #// save it to a list as newlist
    newlist = [software['name']]
    #// remove Duplicates
    newlist = list(dict.fromkeys(newlist))
    #// write to the file with a newline
    file_open.write('\n'.join(newlist))
    file_open.write('\n')
file_open2= open("raw.txt", 'w')
for software in software_list:

    file_open2.write('Name | %s, | Version | %s, | Publisher | %s' % (software['name'], software['version'], software['publisher']) + '\n')



