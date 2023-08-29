from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from time import sleep
from datetime import datetime
import sys
import os, random
namelist=[['Arnold','Chan'],['Jodhan','Peng'],['Werner','Gazuo'],['Sherri','Doyle']]
def parseProfile(profilePath):
    txt = open(profilePath).read().split('-' * 100 + '\n')
    essential = txt[0].split('\n')
    name = essential[0].split(' ')
    nametemp = random.randint(0,3)
    first_name = namelist[nametemp][0]
    last_name = namelist[nametemp][1]
    professional = essential[1]
    overview = essential[2]
    phone = essential[3].split(', ')[0]
    country = essential[3].split(', ')[1]
    hourRate = essential[4]
    workXP = [(
        i[0].replace('\n', '').split(', ')[0],
        i[0].replace('\n', '').split(', ')[1],
        i[1].replace('\n', '').split(', ')[0],
        i[1].replace('\n', '').split(', ')[1],
        i[2].replace('\n', '').split(' - ')[0],
        i[2].replace('\n', '').split(' - ')[1]
    ) for i in [j.split('\n') for j in txt[1].split('\n\n')]]

    education = [(
        i[0].replace('\n', ''),
        i[1].replace('\n', ''),
        i[2].replace('\n', ''),
        i[3].replace('\n', '').split(' - ')[0][:4],
        i[3].replace('\n', '').split(' - ')[1][:4]
    ) for i in [j.split('\n') for j in txt[2].split('\n\n')]]

    languages = [tuple(i.replace('\n', '').split(', ')) for i in txt[3].split('\n')][:-1]

    skills = [i for i in txt[4].split('\n')[0].replace('\n', '').split(', ')]
    services = [i for i in txt[4].split('\n')[1].replace('\n', '').split(', ')]

    last = txt[5].split('\n')
    street = last[0].replace('\n', '').split(', ')[0]
    zipcode = last[0].replace('\n', '').split(', ')[1]
    city = last[1].replace('\n', '').split(', ')[0]
    location = last[2]
    avatar = last[3]

    information = {
        'first_name': first_name,
        'last_name': last_name,
        'professional': professional,
        'overview': overview,
        'country': country,
        'hourRate': hourRate,
        'workXP': workXP,
        'education': education,
        'languages': languages,
        'skills': skills,
        'services': services,
        'street': street,
        'zipcode': zipcode,
        'city': city,
        'location': location,
        'phone': phone,
        'avatar': avatar
    }

    return information

def waitInfinite(callback, debug = False):
    yet = True
    while yet:
        try:
            callback()
            yet = False
        except NoSuchElementException:
            pass
        except JavascriptException:
            pass
        except StaleElementReferenceException:
            pass
            
def waitUntil(callback, driver, selector):
    yet = True
    while yet:
        try:
            callback(driver.find_element(By.CSS_SELECTOR, selector))
            yet = False
        except:
            pass

def clickByMouse(element):
    ActionChains(driver).click(element)\
                        .perform()

def selectDropDown(dropdownId, itemSelector, country):
    driver.execute_script(f'document.querySelector(\'#{dropdownId}\').click()')
    sleep(0.5)
    nations = driver.find_elements(By.CSS_SELECTOR, itemSelector)

    if str(type(country)) == "<class 'int'>":
        driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(country)}].click()')
    else:
        for i in range(len(nations)):
            try:
                if nations[i].text.find(country) >= 0:
                    driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(i)}].click()')
                    break
            except:
                pass

def selectDateDropDown(dropdownId, itemSelector, country):
    tmp = dropdownId.split('##')
    if len(tmp) == 2:
        dropdownId = tmp[0]
        driver.execute_script(f'document.querySelectorAll(\'div[aria-labelledby^="{dropdownId}"]\')[{tmp[1]}].click()')
    else:
        driver.execute_script(f'document.querySelector(\'div[aria-labelledby^="{dropdownId}"]\').click()')
    sleep(0.5)
    nations = driver.find_elements(By.CSS_SELECTOR, itemSelector)

    if str(type(country)) == "<class 'int'>":
        driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(country)}].click()')
    else:
        for i in range(len(nations)):
            try:
                if nations[i].text.find(country) >= 0:
                    driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(i)}].click()')
                    break
            except:
                pass

def verifyEmail():
    emailGetter.execute_script('x = document.querySelectorAll("td.from")[0];if(x.textContent == " Upwork Notifications ") x.click()')
    sleep(4)
    iframe = emailGetter.find_element(By.ID, "iframeMail")
    emailGetter.switch_to.frame(iframe)

def addSkill(driver, inp, skill, field = "skills-input"):
    
    waitUntil(lambda x: x.click(), driver, f'input[aria-labelledby="{field}"]')
    waitUntil(lambda x: x.send_keys(skill), driver, f'input[aria-labelledby="{field}"]')
    
    flag = True
    while flag:
        nations = driver.find_elements(By.CSS_SELECTOR, "span.air3-menu-item-text")
        flag = len(nations) == 0

    for i in range(len(nations)):
        try:
            if nations[i].text.find(skill) >= 0:
                driver.execute_script(f'document.querySelectorAll("span.air3-menu-item-text")[{str(i)}].click()')
                break
        except:
            pass
        
    sleep(0.5)

def addService(driver, services):
    waitUntil(lambda x: x.click(), driver, 'div[data-test="dropdown-toggle"]')
    sleep(1)
    for service in services:
        driver.execute_script(f'''
            // document.querySelector(\'div[data-test="dropdown-toggle"]\').click()
            var services = document.querySelectorAll('span.air3-menu-checkbox-labels');
            var toselect;
            for (let i = 0; i < services.length; i++) {{
                console.log(services[i], '{service}');
                if (services[i].textContent.indexOf('{service}') >= 0) {{
                    toselect = services[i].parentNode.parentNode;
                    break;
                }}
            }}
            if (toselect) {{
                if (toselect.getAttribute("aria-selected") == 'false') {{
                    toselect.parentNode.parentNode.parentNode.click();
                    setTimeout(() => toselect.click(), 300);
                }}
            }}
        ''')
        sleep(0.1)

def configLast(driver, country, street, city, zipcode, phone, photo):
    global photoDir
    selectDateDropDown("country-label", "span.air3-menu-item-text", country)
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="street-label"]').send_keys(street))
    
    addSkill(driver, driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="city-label"]'), city, "city-label")

    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="postal-code-label"]').send_keys(zipcode))
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby^="dropdown-label-phone-number"]').send_keys(phone))

    waitInfinite(lambda: driver.execute_script("document.querySelector('button[data-cy=\"open-loader\"]').click()"))
    sleep(0.5)

    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(photoDir +"input" +str(random.randint(0,9))+".jpg"))
    waitInfinite(lambda: driver.execute_script("document.querySelectorAll('button.air3-btn.air3-btn-primary')[1].click()"))


global expFlag, photoDir
expFlag = True
photoDir = 'C:\\Pictures\\'

curr_year = datetime.now().year
today = str(datetime.today().date())

profile = "upwork_fake_account.txt"

resume = os.path.abspath('myresume.pdf')
hasResume = True

profile = parseProfile(profile)

for i in range(30):
    emailGetter = webdriver.Chrome()
    emailGetter.get("https://www.minuteinbox.com/")
    tempURL = emailGetter.find_element(By.ID, "email").text
    
    #Sign up
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disk-cache-dir=/path/to/cache')
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    waiting = WebDriverWait(driver, 10)
    driver.get("https://www.upwork.com/nx/signup/?dest=home")

    driver.find_element(By.ID, "button-box-4").click()
    driver.find_element(By.CSS_SELECTOR, "button[data-qa='btn-apply']").click()

    driver.find_element(By.ID, "first-name-input").send_keys(profile['first_name'])
    driver.find_element(By.ID, "last-name-input").send_keys(profile['last_name'])

    #Get Temp URL
    driver.find_element(By.ID, "redesigned-input-email").send_keys(tempURL)
    driver.find_element(By.ID, "password-input").send_keys("jack?EGG8QUEENSKYPE")

    sleep(1)
    selectDropDown("dropdown-label-7", "li.up-menu-item", profile['country'])
    driver.execute_script('document.querySelectorAll("span.up-checkbox-replacement-helper")[1].click()')
    sleep(1)
    print("ba")
    driver.execute_script('document.getElementById("button-submit-form").click()')
    print("aa")
    sleep(9)

    waitInfinite(verifyEmail)
    verifiedURL = emailGetter.find_elements(By.TAG_NAME, 'a')[1].get_attribute('href')

    name = profile['first_name'] + profile['last_name']

    driver.get(verifiedURL)
    sleep(9)

    try:
        emailGetter.quit()
    except:
        try:
            emailGetter.close()
        except:
            pass

    driver.execute_script('document.querySelector("button.air3-btn.mr-7.air3-btn-primary").click()')
    # driver.find_element(By.NAME, "button[data-qa='btn-apply']").click()
    print('a')
    sleep(1)
    driver.find_element(By.XPATH, '//input[@value="FREELANCED_BEFORE"]').click()
    print('b')
    # driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary").click()')
    driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    sleep(2)

    page_url = 'https://www.upwork.com/nx/create-profile/goal/'
    driver.get(page_url)
    sleep(1)
    driver.find_element(By.XPATH, '//input[@value="MAIN_INCOME"]').click()
    # driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary").click()')
    driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    sleep(2)

# 3/3
    while True:
        try:
            sleep(1)
            panel = driver.find_element(By.XPATH, '//input[@data-ev-label="button_box_checkbox"]')
            driver.execute_script("arguments[0].click();", panel)
            sleep(0.5)
            driver.execute_script('document.querySelector("input.air3-checkbox-input.sr-only").click()')
            # step4checkbox = driver.find_element(By.XPATH, '//input[@class="air3-checkbox-input sr-only"]')
            # driver.execute_script("arguments[0].click();", step4checkbox)
            sleep(2)
            driver.find_element(By.XPATH, '//*[@data-ev-label="wizard_next"]').click()
            break
        except:
            print("error")
            sleep(0.5)
            pass
    
    sleep(4)

    # panel = driver.find_element(By.XPATH, '//input[@data-ev-label="button_box_checkbox"]')
    # driver.execute_script("arguments[0].click();", panel)
    # sleep(1)
    # step4checkbox = driver.find_element(By.XPATH, '//input[@class="air3-checkbox-input sr-only"]')
    # driver.execute_script("arguments[0].click();", step4checkbox)
    # sleep(2)
    # driver.find_element(By.XPATH, '//*[@data-test="next-button"]').click()
    # print('nnnn')
    # sleep(8)

    # driver.execute_script('document.querySelector("button.air3-btn.mb-0.mr-md-6.air3-btn-link").click()')
    # print("e")

    # driver.execute_script('document.querySelector("button.air3-btn.mb-0.mr-md-6.air3-btn-link").click()')
    # print("f")
    page_url = 'https://www.upwork.com/nx/create-profile/resume-import/'
    driver.get(page_url)
    sleep(2)
    waitInfinite(lambda: driver.execute_script('document.getElementsByClassName("mb-3 air3-btn air3-btn-secondary d-none d-md-block")[1].click()'))

    dz = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    dz.send_keys(resume)
    sleep(8)

    nexBtn = driver.find_element(By.CSS_SELECTOR, "button.air3-btn.air3-btn-primary.mb-0")
    driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()')    
    sleep(2)
    # inp_prof = driver.find_element(By.CSS_SELECTOR, "input[aria-labelledby=\"title-label\"]")
    # # inp_prof.click()
    # inp_prof.clear()
    input_role = driver.find_element(By.CSS_SELECTOR, "input.air3-input.form-control")
    input_role.clear()

    input_role.send_keys(profile['professional'])
    nexBtn = driver.find_element(By.CSS_SELECTOR, "button[data-ev-label='wizard_next']")
    clickByMouse(nexBtn)

    sleep(1)
    driver.find_element(By.XPATH, "//*[@data-ev-label='wizard_next']")
    sleep(1)
    driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()')
    sleep(1)

    if driver.current_url == "https://www.upwork.com/nx/create-profile/certifications":
        driver.execute_script('document.querySelector("input.air3-checkbox-input.sr-only").click()')
        driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()')

    waitInfinite(lambda: selectDateDropDown("dropdown-label-english", "span.air3-menu-item-text", 2))
    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'))

    sleep(1)
    inp_skills = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="skills-input"]')

    for i in profile['skills']:
        addSkill(driver, inp_skills, i)

    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'))

    sleep(1)
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="overview-label"]').clear())
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="overview-label"]').send_keys(profile['overview']))
    sleep(0.5)
    clickByMouse(driver.find_element(By.CSS_SELECTOR, 'button.air3-btn.air3-btn-primary.mb-0'))

    sleep(3)
    addService(driver, profile['services'])
    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'))

    sleep(1)

    inp_hr = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Hourly rate in $/hr"]')
    inp_hr.clear()
    inp_hr.send_keys(str(profile['hourRate']))
        
    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'))

    sleep(1)
    configLast(
        driver,
        profile['location'],
        profile['street'],
        profile['city'],
        profile['zipcode'],
        profile['phone'],
        profile['avatar']
    )

    sleep(4)
    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'))
    sleep(3)
    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.width-md.m-0.air3-btn-primary").click()'))

    driver.get("https://www.upwork.com/nx/find-work/best-matches/?landing=announcement-TONB-2806")

    try:
        open(name + '_email' + today + '.txt', 'a', encoding='utf-8').write(tempURL + '\n')
    except FileNotFoundError:
        open(name + '_email' + today + '.txt', 'a', encoding='utf-8').write(tempURL + '\n')

    try:
        emailGetter.quit()
    except:
        try:
            emailGetter.close()
        except:
            pass
