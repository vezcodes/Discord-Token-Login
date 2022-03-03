# Imports Libraries

import requests
import random
import os
import re
import io
import sys
import time
import json
import shutil
import ctypes
import random
import zipfile
import requests
import threading
import subprocess

from time import sleep
from selenium import webdriver, common
from colorama import Fore, Back
from urllib.request import urlopen, urlretrieve
from distutils.version import LooseVersion
from bs4 import BeautifulSoup
from time import sleep


# Defines the color Cyan
cyan = Fore.CYAN


# Defines the version
THIS_VERSION = '1.2'


# Defines the banner
banner = cyan + f'''
___________     __                   .____                 .__        
\__    ___/___ |  | __ ____   ____   |    |    ____   ____ |__| ____  
  |    | /  _ \|  |/ // __ \ /    \  |    |   /  _ \ / ___\|  |/    \ 
  |    |(  <_> )    <\  ___/|   |  \ |    |__(  <_> ) /_/  >  |   |  \\
  |____| \____/|__|_ \\___  >___|  / |_______ \____/\___  /|__|___|  /
                    \/    \/     \/          \/    /_____/         \/ 
                       v {THIS_VERSION}
                       Credits to: Vez Codez & Rdimo

'''


# Our Main Function
def main():
    os.system('cls')
    print(banner)
    token = input(Fore.CYAN + f"Hello there, you'll have to specify the token twice.\n{Fore.YELLOW}[{Fore.WHITE}>{Fore.YELLOW}]{cyan} Token:")
    loginToken()


# Defines The target versions 
google_target_ver = 0
edge_target_ver = 0


# Defines the user agents
heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]


# Installs Chromium Driver
class Chrome_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://chromedriver.storage.googleapis.com/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if google_target_ver:
            self.target_version = google_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect


    def get_release_version_number(self):
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return LooseVersion(urlopen(self.__class__.DL_BASE + path).read().decode())

    def fetch_chromedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Edge_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://msedgedriver.azureedge.net/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if edge_target_ver:
            self.target_version = edge_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "edgedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_edgedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open("ms"+self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect


    def get_release_version_number(self):
        path = (
            "LATEST_STABLE"
            if not self.target_version
            else f"LATEST_RELEASE_{str(self.target_version).split('.', 1)[0]}"
        )
        urlretrieve(
            f"{self.__class__.DL_BASE}{path}",
            filename=f"{os.getenv('temp')}\\{path}",
        )
        with open(f"{os.getenv('temp')}\\{path}", "r+") as f:
            _file = f.read().strip("\n")
            content = ""
            for char in [x for x in _file]:
                for num in ("0","1","2","3","4","5","6","7","8","9","."):
                    if char == num:
                        content += char
        return LooseVersion(content)

    def fetch_edgedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract("ms"+self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Opera_Installer(object):
    DL_BASE = "https://github.com"
    def __init__(self, *args, **kwargs):
        self.platform = sys.platform
        self.links = ""

        r = requests.get(self.__class__.DL_BASE+"/operasoftware/operachromiumdriver/releases")
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if "operadriver" in link.get('href'):
                self.links += f"{link.get('href')}\n"

        for i in self.links.split("\n")[:4]:
            if self.platform in i:
                self.fetch_edgedriver(i)

    def fetch_edgedriver(self, driver):
        executable = "operadriver.exe"
        driver_name = driver.split("/")[-1]
        cwd = os.getcwd() + os.sep

        urlretrieve(self.__class__.DL_BASE+driver, filename=driver_name)
        with zipfile.ZipFile(driver_name) as zf:
            zf.extractall()
        shutil.move(cwd+driver_name[:-4]+os.sep+executable, cwd+executable)
        os.remove(driver_name)
        shutil.rmtree(driver_name[:-4])

def getDriver():
    #supported drivers
    drivers = ["chromedriver.exe", "msedgedriver.exe", "operadriver.exe"]
    print(f"\n{Fore.BLUE}Checking Driver. . .")
    sleep(0.5)

    for driver in drivers:
        #Checking if driver already exists
        if os.path.exists(os.getcwd() + os.sep + driver):
            print(f"{Fore.GREEN}{driver} already exists, continuing. . .{Fore.RESET}")
            sleep(0.5)
            return driver
    else:
        print(f"{Fore.RED}Driver not found! Installing it for you")
        #get installed browsers + install driver + return correct driver
        if os.path.exists(os.getenv('localappdata') + '\\Google'):
            Chrome_Installer()
            print(f"{Fore.GREEN}chromedriver.exe Installed!{Fore.RESET}")
            return "chromedriver.exe"
        elif os.path.exists(os.getenv('appdata') + '\\Opera Software\\Opera Stable'):
            Opera_Installer()
            print(f"{Fore.GREEN}operadriver.exe Installed!{Fore.RESET}")
            return "operadriver.exe"
        elif os.path.exists(os.getenv('localappdata') + '\\Microsoft\\Edge'):
            Edge_Installer()
            print(f"{Fore.GREEN}msedgedriver.exe Installed!{Fore.RESET}")
            return "msedgedriver.exe"
        else:
            print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : No compatible driver found. . . Proceeding with chromedriver')
            Chrome_Installer()
            print(f"{Fore.GREEN}trying with chromedriver.exe{Fore.RESET}")
            return "chromedriver.exe"



# Tries to obtain the headers
def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers


# Our Login Functio 
def loginToken():
    token = input(Fore.CYAN + f"{Fore.YELLOW}[{Fore.WHITE}>{Fore.YELLOW}]{cyan} Token:")
    j = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token)).json()
    user = j["username"] + "#" + str(j["discriminator"])
    script = """
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"%s"`
            location.reload();
        """ % (token)
    type_ = getDriver()

    if type_ == "chromedriver.exe":
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        try:
            driver = webdriver.Chrome(options=opts)
        except common.exceptions.SessionNotCreatedException as e:
            print(e.msg)
            sleep(2)
            print("Enter anything to continue. . . ")
            input()
            main()
    elif type_ == "operadriver.exe":
        opts = webdriver.opera.options.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        try:
            driver = webdriver.Opera(options=opts)
        except common.exceptions.SessionNotCreatedException as e:
            print(e.msg)
            sleep(2)
            print("Enter anything to continue. . . ")
            input()
            main()
    elif type_ == "msedgedriver.exe":
        opts = webdriver.EdgeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        try:
            driver = webdriver.Edge(options=opts)
        except common.exceptions.SessionNotCreatedException as e:
            print(e.msg)
            sleep(2)
            print(f"Enter anything to continue. . .")
            input()
            main()
    else:
        print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : Coudln\'t find a suitable driver to automatically login to {user}')
        sleep(3)
        print(f"{Fore.YELLOW}Paste this script into the console of a browser:{Fore.RESET}\n\n{Back.RED}{script}\n{Back.RESET}")
        print("Enter anything to continue. . . ", end="")
        input()
        main()

    print(f"{Fore.GREEN}Logging into {Fore.CYAN}{user}")
    driver.get("https://discordapp.com/login")
    driver.execute_script(script)
    main()


# Goes to the main function if exists, it exists so it goes to line 51
if __name__ == '__main__':
    main()
