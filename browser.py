
from optparse import Option
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException,NoSuchElementException, NoSuchWindowException,ElementClickInterceptedException,ElementNotInteractableException, StaleElementReferenceException
import random
import logging
import time
from urllib.parse import urlparse, urlsplit, urljoin

# Add target URL below: 
links = [


]


search_phrase =[

]


netloc = []


BROWSER = 'Chrome'
MAX_LINK_TRAVERSED = 1000
VISIT_REPEATED_PAGE = False
BROWSER_HEADLESS = False
RANDOM_PAGE_CLICKS = 3 
VISIT_LINK_DOMAIN_LONLY = True
TEXT_FIELD_SEARCH = True
LINK_ON_SEARCH_RESULTS = True
EXPAND_SEARCH_PHRASE = True
PERFORMANCE_CALC = False
REMOVE_QUERY_STRING = True
REMOVE_UTM＿QUERY_STRING = True
#XPATH_URL_CRAWLER = "//a[not(contains(href,'javascript'))]"
XPATH_URL_CRAWLER = "//a[@href]"
XPATH_SEARCH_TEXT_INPUT = "//div[@class='index-search']//input[@id='SearchKeyword']"
XPATH_PAGE_CLICK = "//a[@href] | //input[@type='checkbox']"
JStyle = "10px solid red"

def getlink(link):
    try:

        browser.get(link)
        # Network transport takes time. Wait until the page is fully loaded
        def is_ready(browser):
            return browser.execute_script(r"""
                return document.readyState === 'complete'
            """)
        WebDriverWait(browser,10).until(is_ready)
        # Scroll to bottom of the page to trigger JavaScript action
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        browser.implicitly_wait(10)
        WebDriverWait(browser, 10).until(is_ready)

        if PERFORMANCE_CALC:
            navigationStart = browser.execute_script("return window.performance.timing.navigationStart")
            responseStart = browser.execute_script("return window.performance.timing.responseStart")
            domComplete = browser.execute_script("return window.performance.timing.domComplete")

            backendPerformance_calc = responseStart - navigationStart
            frontendPerformance_calc = domComplete - responseStart
            logging.info(link,"Back End: %s" % backendPerformance_calc,"Front End: %s" % frontendPerformance_calc )
        

        #collect link elements
        
        elems = browser.find_elements(by = By.XPATH,value = XPATH_URL_CRAWLER)
        #elems = browser.find_elements(by=By.XPATH, value='//a[@href]')
        for elem in elems: 
            #browser.execute_script("arguments[0].style.border=" + JSStyle, element)       
            href = urlsplit(elem.get_attribute('href')).geturl()
            if REMOVE_QUERY_STRING:
                urljoin(href, urlparse(href).path)
            """
            if REMOVE_UTM＿QUERY_STRING:
                parsed_url = list(urlparse(href))
                print(parsed_url)
                parsed_url[4] = '&'.join(
                    [x for x in parsed_url[4].split('&') if not re.match(r'utm_', x)])
                href= urlunparse(parsed_url)
            """
            if ".pdf" in href:
                continue
            
            if href and len(links) < MAX_LINK_TRAVERSED :
                if VISIT_REPEATED_PAGE:
                    links.append(href)
                    logging.info("\t", href)
                else: 
                    if not href  in links:
                        if VISIT_LINK_DOMAIN_LONLY:
                            parsed_url = urlparse(href)
                            if parsed_url.netloc in netloc:
                                links.append(href)
                                logging.info("\t", href)
                        else:       
                            links.append(href)
                            logging.info("\t", href)
                        
                        
        #find h2 keywords
        elems = browser.find_elements(by = By.XPATH,value = "//h2")
        for elem in elems: 
            kw=elem.get_attribute('value').strip()
            if kw not in search_phrase:
                search_phase.append(kw)
            logging.debug("\t keyword found:", kw)
            
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
                    logging.debug("\tSend text: ", text_key," in search.")

                    if LINK_ON_SEARCH_RESULTS:
                        WebDriverWait(browser, 10).until(is_ready)
                        elements = []
                        elements = browser.find_elements(by = By.XPATH,value = XPATH_PAGE_CLICK ) #Finds all elements in the page
                        if elements: 
                            for click in range(RANDOM_PAGE_CLICKS):
                                element = random.choice(elements) #Selects a random element from the list of elements
                                browser.execute_script("arguments[0].style.border=" + JSStyle, element)
                                browser.implicitly_wait(30)
                                WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(element))
                                element.click() #Clicks on the selected element
                                logging.debug("Clicked on search results.")

            except ElementNotInteractableException:
                logging.exception()
                pass
            except StaleElementReferenceException:
                logging.exception()           
                pass
        # Random page clicks
        if RANDOM_PAGE_CLICKS:
            elements = []
            try:
                elements = browser.find_elements(by = By.XPATH,value = XPATH_PAGE_CLICK ) #Finds all elements in the page
                if elements: 
                    for click in range(RANDOM_PAGE_CLICKS):
                        element = random.choice(elements) #Selects a random element from the list of elements
                        browser.execute_script("arguments[0].style.border=" + JSStyle, element)
                        browser.implicitly_wait(30)
                        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(element))

                        element.click() #Clicks on the selected element
               
                                
                #browser.execute_script("arguments[0].click();", element) #javescript click
                logging.info('\tSent click(s)')

            except ElementNotInteractableException:
                logging.exception()
                pass
            except StaleElementReferenceException: 
                logging.exception()         
                pass        
    except WebDriverException:
        logging.exception()
        pass    

            
if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    for uri in links:
        parsed_uri = urlparse(uri)
        if parsed_uri.netloc not in  netloc:
            netloc.append(parsed_uri.netloc)

    # Launch selected  browser 

    if BROWSER == 'Chrome':
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        options = webdriver.ChromeOptions()
        if BROWSER_HEADLESS:
            options.add_argument("headless")
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    elif BROWSER == 'Edge':
        from selenium.webdriver.edge.options import Options
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        from selenium.webdriver.edge.service import Service as EdgeService
        browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))




    thread_pool = list()
    

    for count,link in enumerate(links):

        
        # Load web page
        logging.debug(count,"(of",len(links),")")
        
        try:
            getlink(link)
            """
            thread = threading.Thread(target=getlink, args=(link,), name=f'Thread_{count}')
            thread_pool.append(thread)
            thread.start()
            thread_pool.append(thread) 
            """         
                
        except WebDriverException:
            logging.exception()
            browser.close(         
            )
            if BROWSER == "Chrome":
                browser = webdriver.Chrome(ChromeDriverManager().install())
            if BROWSER == "Edge":
                browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            continue
        
        except NoSuchWindowException:
            logging.exception()
            if BROWSER == "Chrome":
                browser = webdriver.Chrome(ChromeDriverManager().install())
            if BROWSER == "Edge":
                browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            continue
        
        except NoSuchWindowException:
            logging.exception()
            if BROWSER == "Chrome":
                browser = webdriver.Chrome(ChromeDriverManager().install())
            if BROWSER == "Edge":
                browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            continue
        
        
        except ElementClickInterceptedException:
            logging.exception()
        
            continue
        except ElementNotInteractableException:
            logging.exception()
            continue
        except TimeoutException:
            logging.exception()
            continue
        except Exception:
            continue
    # Close the browser on
    browser.close()
    for link in links:
        logging.info(link)
