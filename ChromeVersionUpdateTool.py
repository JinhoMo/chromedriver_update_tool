# coding=utf-8
"""
create on : 2019/07/14
project name : chromedriver_update_tool
file name : ChromeVersionUpdateTool

description : Update chrome driver to equalize chrome version

"""
import subprocess
import re
from urllib import parse
import zipfile

import certifi

from bs4 import BeautifulSoup
from urllib3 import ProxyManager, make_headers, PoolManager

CHROME_DRIVER_DIR = "C:/SeleniumWebdriver/"
CHROME_DRIVER_ZIP = "chromedriver_win32.zip"
CHROME_DRIVER_EXE = "chromedriver.exe"
CHROME_DRIVER = CHROME_DRIVER_DIR + CHROME_DRIVER_EXE

# if you want to use proxy, set values by strings
# non auth proxy set value: "http_proxy"
# or auth proxy set value: "auth_proxy"
# you don't want to set proxy set value "default"
PROXY_MODE = "default"
PROXY_BASIC_AUTH = "username:password"
PROXY_URL_PORT = "http://your.own.proxy.url:8080"

CHROME_DRIVER_DL_SITE = "http://chromedriver.chromium.org/downloads/"


def get_internet_item(url, html=True):
    """ get html or data from given url

    :param url: target site url string
    :param html: download html or data boolean
    :return: html string
    """

    if PROXY_MODE == "http_proxy":
        http = ProxyManager(proxy_url=PROXY_URL_PORT)

    elif PROXY_MODE == "auth_proxy":
        auth_proxy_headers = make_headers(proxy_basic_auth=PROXY_BASIC_AUTH)
        http = ProxyManager(proxy_url=PROXY_URL_PORT,
                            proxy_headers=auth_proxy_headers,
                            cert_reqs="CERT_REQUIRED",
                            ca_certs=certifi.where())

    else:
        http = PoolManager(cert_reqs="CERT_REQUIRED",
                           ca_certs=certifi.where())

    r = http.request("GET", url)

    if r.status != 200:
        raise ConnectionError("http request failure")

    if html:
        data = r.data.decode()

    else:
        data = r.data

    return data


def check_browser_driver_version():
    """ check chrome browser and driver version choice correctly

    :return: result dict
    """

    # get chrome browser version
    browser_cmd = ["dir", r"C:\Program Files (x86)\Google\Chrome\Application"]

    chrome_dir_stdout = subprocess.run(browser_cmd, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, shell=True)

    chrome_dir_cp932 = chrome_dir_stdout.stdout.decode("cp932")
    chrome_dir = "-".join(chrome_dir_cp932.splitlines())

    if re.search(r"([0-9]+\.?)+", chrome_dir):
        browser_pattern = r"([0-9]+\.){3}([0-9]+)+\.?"
        browser_version = re.search(browser_pattern, chrome_dir).group()

    else:
        browser_version = "0.0.0.0"

    browser_version_parse = ".".join(browser_version.split(".")[:-1])

    print("chrome browser version : {}".format(browser_version_parse))

    # get chrome driver version
    driver_cmd = [CHROME_DRIVER, "-version"]

    driver_stdout = subprocess.run(driver_cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, shell=True)
    driver_stdout_cp932 = driver_stdout.stdout.decode("cp932")
    driver_stdout_str = "-".join(driver_stdout_cp932.splitlines())
    driver_version = re.search(r"([0-9]+\.?)+", driver_stdout_str).group()

    driver_version_parse = ".".join(driver_version.split(".")[:-1])

    print("chrome driver version : {}".format(driver_version_parse))

    # check both version
    if browser_version_parse == driver_version_parse:
        check_result = True

    else:
        check_result = False

    results = {"result": check_result,
               "browser_ver": browser_version, "driver_ver": driver_version}

    return results


def download_correctly_driver(target_version):
    """ download chromedriver correctly version

    :param target_version: chromedriver correctly version string
    :return: result boolean
    """
    # Search download page
    dl_site_html = get_internet_item(CHROME_DRIVER_DL_SITE)

    dl_site_soup = BeautifulSoup(dl_site_html, "lxml")
    main_pain = dl_site_soup.find("td", attrs={"id": "sites-canvas-wrapper"})
    href_list = [href["href"] for href in main_pain.find_all("a")
                 if href.has_attr("href")]

    dl_link_pattern = r"http(s)?://[\w.?=/]*" + target_version + r"[\w.]*"

    driver_zip_url = ""

    for href_item in href_list:

        re_href = re.match(dl_link_pattern, href_item)

        if re_href:
            dl_page_url = re_href.group()
            driver_version = re.search(r"([0-9]+\.?)+", dl_page_url).group()
            join_url = "/".join([driver_version, CHROME_DRIVER_ZIP])
            driver_zip_url = parse.urljoin(dl_page_url, join_url)
            break

    if not driver_zip_url:
        return False

    # Search download link
    dl_zip_binary = get_internet_item(driver_zip_url, html=False)

    with open(CHROME_DRIVER_DIR + CHROME_DRIVER_ZIP, "wb") as dl_zip:
        dl_zip.write(dl_zip_binary)

    with zipfile.ZipFile(CHROME_DRIVER_DIR + CHROME_DRIVER_ZIP) as extract_zip:
        extract_zip.extract(CHROME_DRIVER_EXE, CHROME_DRIVER_DIR)

    return True


def chromedriver_update():
    """ Update chrome driver to equalize chrome version

    :return: process success or not boolean
    """
    check_result = check_browser_driver_version()

    if check_result["result"]:
        print("version check OK")
        return True

    else:
        print("version check NG\ntry to dl new chromedriver...")

    chrome_ver = ".".join(check_result["browser_ver"].split(".")[:-1])

    try:
        download_result = download_correctly_driver(chrome_ver)

    except ConnectionError as error:
        print(error)
        return False

    if download_result:
        print("download succeed\nretry version check...")
        check_result = check_browser_driver_version()
        result = check_result["result"]

    else:
        print("download succeed\n"
              "But Browser Build No. is old\n"
              "please update your chrome browser")
        result = False

    return result


def main():
    result = chromedriver_update()

    if result:
        print("Chrome Browser and Driver update success")

    else:
        print("Chrome Browser and Driver update FAILURE")


if __name__ == "__main__":
    main()
