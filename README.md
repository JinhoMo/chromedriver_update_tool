# chromedriver_update_tool

## description

Update chrome driver (for selenium Webdriver) to equalize chrome version

## Requrements

Windows 10, Python3 and some (urllib3, BeautifulSoup4, lxml, certifi(maybe install automatically install urllib3))

more detail please sea conda environment YAML file : [driver_update.yml](./driver_update.yml)

### Purpase - After chrome verson 74, you must select chrome driver version

For example describe this probrem by script. Test verson info is below.

- Chrome Browser version : 75.0.3770.142
- Chrome Driver : 73.0.3683.68

```python
>>> from selenium import webdriver
>>> driver = webdriver.Chrome("C:\SeleniumWebdriver\chromedriver.exe")
```

You may look error like below

```python
DevTools listening on ws://127.0.0.1:57646/devtools/browser/7ba36c8c-b0eb-4ee7-9e75-e15e254f71a2

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\username\Miniconda3\envs\scraping_test\lib\site-packages\selenium\webdriver\chrome\webdriver.py", line 81, in __init__
    desired_capabilities=desired_capabilities)
  File "C:\Users\username\Miniconda3\envs\scraping_test\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 157, in __init__
    self.start_session(capabilities, browser_profile)
  File "C:\Users\username\Miniconda3\envs\scraping_test\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 252, in start_session
    response = self.execute(Command.NEW_SESSION, parameters)
  File "C:\Users\username\Miniconda3\envs\scraping_test\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\username\Miniconda3\envs\scraping_test\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome version must be between 70 and 73
  (Driver info: chromedriver=73.0.3683.68 (47787ec04b6e38e22703e856e101e840b65afe72),platform=Windows NT 10.0.18362 x86_64)
```

Most important message is last line

>Message: session not created: ***Chrome version must be between 70 and 73***
(Driver info: chromedriver=73.0.3683.68  (47787ec04b6e38e22703e856e101e840b65afe72),platform=Windows NT 10.0.18362 x86_64)

This error indicates, chrome browser version is diffrent from chrome driver support version. To soleve this problem, update chrome driver manualiy. And create more complex situation by automatic update chrome browser.

And It's the purpase for this script So, I make a script for this problem.

#### 2. How to use

First, clone script from repository

```cmd
git clone https://github.com/hytmachineworks/chromedriver_update_tool.git
```

and execute script

```cmd
> cd chromedriver_update_tool
> python ChromeVersionChecker.py
```

execute result is below

```cmd
chrome browser version : 75.0.3770
chrome driver version : 73.0.3683
version check NG
try to dl new chromedriver...
download succeed
retry version check...
chrome browser version : 75.0.3770
chrome driver version : 75.0.3770
Chrome Browser and Driver update success
```

You can makesure updated chrome driver version.
