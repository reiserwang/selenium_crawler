
from optparse import Option
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException,NoSuchElementException, NoSuchWindowException,ElementClickInterceptedException,ElementNotInteractableException
import random
import threading
import time

# Add target URL below: 
links = [


]

MAX_LINK_TRAVERSED = 1000
VISIT_REPEATED_PAGE = False
BROWSER_HEADLESS = True
RANDOM_PAGE_CLICKS = 5 


# Launch Chrome browser in headless mode
options = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
if BROWSER_HEADLESS:
    options.add_argument("headless")



thread_pool = list()

def getlink(link):
    #browser.execute_script("window.open('');")
    #browser.switch_to.window(browser.window_handles[1])
    browser.get(link)
    # Network transport takes time. Wait until the page is fully loaded
    def is_ready(browser):
        return browser.execute_script(r"""
            return document.readyState === 'complete'
        """)
    WebDriverWait(browser,12 ).until(is_ready)
    # Scroll to bottom of the page to trigger JavaScript action
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    WebDriverWait(browser, 10).until(is_ready)
    navigationStart = browser.execute_script("return window.performance.timing.navigationStart")
    responseStart = browser.execute_script("return window.performance.timing.responseStart")
    domComplete = browser.execute_script("return window.performance.timing.domComplete")

    backendPerformance_calc = responseStart - navigationStart
    frontendPerformance_calc = domComplete - responseStart
    print(link,"Back End: %s" % backendPerformance_calc,"Front End: %s" % frontendPerformance_calc, "Threads: %s" % threading.active_count() )
    
    #collect link elements
    
    elems = browser.find_elements(by=By.TAG_NAME, value="a")
    #elems = browser.find_elements(by=By.XPATH, value='//a[@href]')
    for elem in elems:
        href = elem.get_attribute('href')
        
        add = 0
        if href is not None:
            if len(links) < MAX_LINK_TRAVERSED:
                if VISIT_REPEATED_PAGE:
                    links.append(href)
                else: 
                    if not href  in links:
                        links.append(href)
    # Random page clicks
    if RANDOM_PAGE_CLICKS > 0:
        for clicks in range (RANDOM_PAGE_CLICKS):
            try:
                elements = browser.find_elements(by = By.XPATH,value = '//*[@id]') #Finds all elements in the page
                element = random.choice(elements) #Selects a random element from the list of elements
                element.click() #Clicks on the selected element 
                browser.execute_script("arguments[0].click();", element) #javescript click

            except Exception:
                continue

for count,link in enumerate(links):
    # Load web page
    print(count,end=' ')
    try:
        
        thread = threading.Thread(target=getlink, args=(link,), name=f'Thread_{count}')
        thread_pool.append(thread)
        thread.start()
        thread_pool.append(thread)
        
        for t in thread_pool:
            t.join(timeout = 10)
        
        
    except WebDriverException:
        browser.close(         
        )
        browser = webdriver.Chrome(ChromeDriverManager().install())
        continue
    
    except NoSuchWindowException:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        continue
    
    except NoSuchWindowException:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        continue
    
    
    except ElementClickInterceptedException:
        continue
    except ElementNotInteractableException:
        continue
    except TimeoutException:
        continue
    except Exception:
        continue

        
# Close the browser on
browser.close()
