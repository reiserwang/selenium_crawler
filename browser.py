
from optparse import Option
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException,NoSuchElementException, NoSuchWindowException,ElementClickInterceptedException,ElementNotInteractableException, StaleElementReferenceException
import random
import threading
import time
from multiprocessing import Pool, cpu_count
from urllib.parse import urlparse
from urllib.parse import urlsplit

# Add target URL below: 
links = [


]


search_phrase =[

]


netloc = []


BROWSER = 'Chrome'
MAX_LINK_TRAVERSED = 1000
VISIT_REPEATED_PAGE = False
BROWSER_HEADLESS = True
RANDOM_PAGE_CLICKS = 3 
VISIT_LINK_DOMAIN_LONLY = True
TEXT_FIELD_SEARCH = False
EXPAND_SEARCH_PHRASE = True
XPATH_URL_CRAWLER = "//a[not(contains(href,'javascript'))]"
XPATH_SEARCH_TEXT_INPUT = "//input[@id='SearchKeyword']"
XPATH_PAGE_CLICK = "//a[@href] | //input[@type='checkbox']"

for uri in links:
    parsed_uri = urlparse(uri)
    if parsed_uri.netloc not in  netloc:
        netloc.append(parsed_uri.netloc)


# Launch selected  browser 

if BROWSER == 'Chrome':
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import ChromeService
    options = webdriver.ChromeOptions()
    if BROWSER_HEADLESS:
        options.add_argument("headless")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
elif BROWSER == 'Edge':
    from selenium.webdriver.edge.options import Options
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service as EdgeService
    browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))



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
    
    elems = browser.find_elements(by = By.XPATH,value = XPATH_URL_CRAWLER)
    #elems = browser.find_elements(by=By.XPATH, value='//a[@href]')
    for elem in elems:        
        href = urlsplit(elem.get_attribute('href')).geturl()
        if href and len(links) < MAX_LINK_TRAVERSED :
            if VISIT_REPEATED_PAGE:
                links.append(href)
                print ("\t", href)
            else: 
                if not href  in links:
                    if VISIT_LINK_DOMAIN_LONLY:
                        parsed_url = urlparse(href)
                        if parsed_url.netloc in netloc:
                            links.append(href)
                            print ("\t", href)
                    else:       
                        links.append(href)
                        print ("\t", href)
                    
                    
    
    # input phrase in search text
    if TEXT_FIELD_SEARCH:
        search_field = []
        try:
            search_field =  browser.find_element(by = By.XPATH,value = XPATH_SEARCH_TEXT_INPUT ) 
            if search_field:         
                #text_field = random.choice(search_fields)
                text_key = random.choice(search_phrase)
                browser.implicitly_wait(30)
                WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable(search_field))
                
                search_field.send_keys(text_key,Keys.ENTER)
                WebDriverWait(browser, 10).until(is_ready)
                print("\tSend text: ", text_key," in search.")
            #text_field.send_keys(Keys.ENTER)

        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:            
            pass
    # Random page clicks
    if RANDOM_PAGE_CLICKS:
        elements = []
        try:
            elements = browser.find_elements(by = By.XPATH,value = XPATH_PAGE_CLICK ) #Finds all elements in the page
            if elements: 
                for click in range(RANDOM_PAGE_CLICKS):
                    element = random.choice(elements) #Selects a random element from the list of elements
                    
                    browser.implicitly_wait(30)
                    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(element))
                    element.click() #Clicks on the selected element

               
                               
            #browser.execute_script("arguments[0].click();", element) #javescript click
            print('\tSent click(s)')

        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:            
            pass        



for count,link in enumerate(links):
    # Load web page
    print(count,"(of ",len(links),")",end=' ')
    try:
        
        thread = threading.Thread(target=getlink, args=(link,), name=f'Thread_{count}')
        thread_pool.append(thread)
        thread.start()
        thread_pool.append(thread)
        
        thread.join(timeout = 10)
        """
        for t in thread_pool:
            t.join(timeout = 10)
        """

       
            
    except WebDriverException:
        browser.close(         
        )
        if BROWSER == "Chrome":
            browser = webdriver.Chrome(ChromeDriverManager().install())
        if BROWSER == "Edge":
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        continue
    
    except NoSuchWindowException:
        if BROWSER == "Chrome":
            browser = webdriver.Chrome(ChromeDriverManager().install())
        if BROWSER == "Edge":
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        continue
    
    except NoSuchWindowException:
        if BROWSER == "Chrome":
            browser = webdriver.Chrome(ChromeDriverManager().install())
        if BROWSER == "Edge":
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
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
for link in links:
    print(link)
