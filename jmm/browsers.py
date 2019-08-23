#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser automation

Selenium doc can be found at:
https://selenium-python.readthedocs.io/api.html

 More examples and infos: Pamela Fox
      http://blog.pamelafox.org/2012/01/testing-facebook-login-with-selenium.html

 Helpers :
      https://gist.github.com/pamelafox/1624214#file-selenium_dom-py-L29

"""

import time
import enum
import json

import selenium.webdriver.support.ui as ui

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.common.exceptions import WebDriverException

## doc at: https://pyautogui.readthedocs.io/en/latest/
# import pyautogui


class SeleniumHelper(object):
    class Browser(enum.Enum):
        """docstring for SeleniumHelper.Browser"""
        Firefox = "firefox"
        Chrome = "chrome"
        Safari = "safari"

        @classmethod
        def value_for(cls, name):
            name = name.lower().strip()
            name = "firefox" if name == "ff" else name
            # SeleniumHelper.Browser
            return cls(name)

        def new_browser(self):
            if self == self.Firefox:
                return webdriver.Firefox()
            elif self == self.Chrome:
                return webdriver.Chrome()
            elif self == self.Safari:
                return webdriver.Safari()
            else:
                return webdriver.Chrome()

        @classmethod
        def new_browser_for(cls, name):
            instance = cls(name).new_browser()
            return instance
        
        @classmethod
        def new_available_browser(cls, preferred_browsers=None):
            """Returns a new browser instance among the most common browsers
            or a list of browsers.
            :param preferred_browsers: list of webdrivers constructor functions
                        or None to use a default list.
            """
            def browser_or_none(constructor):
                try:
                    return constructor()
                except selenium.common.exceptions.WebDriverException:
                    return None
            
            wd = webdriver
            drivers = [wd.Chrome, wd.Firefox, wd.Safari,
                       wd.Opera, wd.Edge, wd.Ie]
            drivers = preferred_browsers if preferred_browsers is not None else drivers
            
            for a_driver in drivers:
                browser = browser_or_none
                if browser is not None:
                    return browser
            return None
        
        @classmethod
        def restored_browser_session(cls, command_executor_url, session_id, close_new_browser=True):
            """
            :return: a selenium webdriver browser of the previous session.
                    return None if no previous session found with parameters.
            """
            try:
                ## This automatically opens up a new browser **app window**
                ## so the user might want to close this new window and only
                ## keep the previous one opened.
                driver = webdriver.Remote(command_executor=command_executor_url, desired_capabilities={})
                
                ## 
                if close_new_browser:
                    try:
                        driver.quit()
                    except Exception as err:
                        pass
                
                driver.session_id = session_id
            except ConnectionRefusedError:
                driver = None
            
            return driver
        
        @classmethod
        def reloaded_browser_session(cls, filepath, close_new_browser=True):
            """Reloads a previous session with infos from a file. Just like
            'restored_browser_session', but accepting a filepath to get the session infos from instead.
            
            :param str filepath: filepath of saved infos (filepath that was passed to `save_browser_session`)
            :return: webdriver driver or None if no file found.
            :raises: an error if the file content does not have the appropriate format
            """
            infos_dict = None
            browser = None
            try:
                with open(filepath) as fh:
                    infos_dict = json.load(fh)
                    command_executor_url =  infos_dict.get('command_executor_url')
                    session_id = infos_dict.get('session_id')
                    browser = cls.restored_browser_session(
                                command_executor_url,
                                session_id,
                                close_new_browser)
                    
            except FileNotFoundError:
                pass
            return browser
            
        @classmethod
        def save_browser_session(cls, driver, filepath=None):
            infos = ()
            command_executor_url = driver.command_executor._url
            session_id = driver.session_id
            infos = (command_executor_url, session_id)
            
            if filepath:
                with open(filepath, 'w') as fh:
                    infos_dict = {
                        'command_executor_url': command_executor_url,
                        'session_id': session_id
                    }
                    json.dump(infos_dict, fh)
            
            return infos
        pass


    def __init__(self, browser=None, browser_name=None, another=None, previous_session=None):
        """
        First, it will try to reuse any previous session (provided the argument has been passed).
        If no previous session could be restored, it will fallback to use the `another` driver argument
        as the webdriver.
        Finally, if none of the above produced a webdriver session, it will create a new browser
        
        :param another: another instance. The new one will reuse most of the
                        components like its browser driver instead of opening
                        /creating others.
                        If provided, the extra parameters like browser and
                        browser_name you may provide will be ignored.
        """
        super(object, self).__init__()
        self.driver = None
        
        ### Try re-using a previous session or create a new one if none exist
        if previous_session:
            if isinstance(previous_session, str):  # filepath to session infos
                self.driver = SeleniumHelper.Browser.reloaded_browser_session(previous_session, True)
            else:
                command_executor_url, session_id = previous_session
                self.driver = SeleniumHelper.Browser.restored_browser_session(command_executor_url, session_id, True)
        
        if self.driver is None:
            if another:
                self.driver = another.driver
            else:
                # Chrome considered a good browser so we use it first
                browser_name = "chrome" if browser_name is None else browser_name
                if browser and not isinstance(browser, str):
                    self.driver = browser
                else:
                    self.driver = SeleniumHelper.Browser.new_browser_for(browser_name)
                
                # use whatever is available otherwise
                if self.driver is None:
                    self.driver = SeleniumHelper.Browser.new_available_browser()
        
        self.wait = ui.WebDriverWait(self.driver, 1000)
    
    
    ### ---------------------- ###
    
    def get(self, url):
        self.driver.get(url)
        return self.driver
    
    # def getAWait(self, driver):
    def getAWait(self):
        driver = self.driver
        wait = ui.WebDriverWait(driver, 1000)
        return wait

    def waitTime(self, s=0, ms=0):
        # delta_t = s + (ms / 1000)
        # if verbose:
        #     print("Sleeping for %.1f seconds" % (delta_t))
        # time.sleep(delta_t)
        ##################
        tmp = s*1000 + ms
        t0 = time.time()
        self.wait.until( lambda _ : 1000*(time.time() - t0) > tmp )
    
    def waitTillExists(self, selector):
        doesExist = lambda _: self.elementExists(selector)
        # doesNotExist = lambda _: not doesExist(selector)
        self.wait.until( doesExist )
    
    def waitTillUrlContains(self, contains):
        self.wait.until(ExpectedConditions.url_contains(contains))
    
    def get_current_url(self):
        return self.browser.current_url
    
    ### ---------------------- ###
    
    def getEl(self, selector, *args, **kwargs):
        # return self.driver.find_element_by_css_selector(selector)
        return self.getChildElement(self.driver, selector, *args, **kwargs)
    
    def get_el(self,selector, *args, **kwargs):
        return self.getEl(selector, *args, **kwargs)

    def getElements(self, selector, *args, **kwargs):
        # return self.driver.find_elements_by_css_selector(selector)
        return self.getChildElements(self.driver, selector, *args, **kwargs)

    def getChildElement(self, parent, relative_selector, satisfying=None):
        if satisfying is None:
            # performance: use default implementation unless necessary
            return parent.find_element_by_css_selector(relative_selector)
        else:
            return self.getChildElements(parent, relative_selector, satisfying)
    
    def getChildElements(self, parent, relative_selector, satisfying=None):
        default_func = (lambda x: True)
        satisfying = default_func if satisfying is None else satisfying
        elmts = parent.find_elements_by_css_selector(relative_selector)
        elmts = [e for e in elmts if satisfying(e)]
        return elmts

    # def getSelectOption(self, select_element, relative_selector, handler):
    def getSelectOption(self, select_element, relative_selector):
        # We could also use the Select class
        # https://stackoverflow.com/a/28613320/4418092
        return select_element.find_element_by_css_selector(relative_selector)

    def elementExists(self, selector):
        try:
            _ = self.getEl(selector)
            return True
        except:
            return False
    
    def enterTextField(self, selector, text, clear=True):
        # On trouve le champ à remplir.
        text_field = self.getEl(selector)
        if clear:
            # On enlève les valeurs qui y sont peut-être déjà.
            text_field.clear()
        # On ajoute le texte voulu dans le champ de formulaire.
        text_field.send_keys(text)
        return text_field
    
    def enter_text_field(self, selector, text):
        return self.enterTextField(selector, text)
    
    def enter_textfield(self, *args, **kwargs):
        return self.enterTextField(*args, **kwargs)

    # def click_element(self, element, driver):
    def click_element(self, element):
        """Tries to perform a click on an element and fallbacks on JS click if browser click does not work.
        :param element: a selector or an element you want to click
        :return:
            Returns a boolean indicating whether the normal browser click was successful.
            If False, it means that another method (trick) had to be used to try clicking the button.

            Note that it does not tell whether or not the click was taken into account nor whether the click had
            the effect it should have had.
        """
        driver = self.driver
        if isinstance(element, str):
            selector = element
            if driver is None:
                print("here you must provide a browser if no element")
                raise Exception("here you must provide a browser if no element")
            element = self.getEl(selector)
        
        try:
            element.click()
            return True
        except Exception as err:
            # There is an overlay or another HTML element (like a "Accept Cookies" banner)
            # Then we try triggering the click through JS
            
            # print("Error with clicking validationButton: trying JS click")
            # IJavaScriptExecutor
            js_executor = driver
            js_executor.execute_script("arguments[0].click();", element);
        return False

    
    ### ---------------------- ###
    ###       Navigating       ###
    
    def scrollToHeight(self, height):
        self.driver.execute_script("window.scrollTo(0, %s)" % height)
    
    def scrollToPosition(self, x, y):
        self.driver.execute_script("window.scrollTo(%s, %s)" % (x,y))
    
    def scrollToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scrollDownNTimes(self, N, pauseTime = 0.5):
        driver = self.driver
        pauseTime = 0.5
        scrollIndefinitely = N < 0
        
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while scrollIndefinitely or N > 0:
            N -= 1
            
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(pauseTime)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height



# API of browser (driver)
# >>> b = browser
# >>> b.
# b.add_cookie(                          b.get_cookies(
# b.application_cache                    b.get_log(
# b.back(                                b.get_network_conditions(
# b.capabilities                         b.get_screenshot_as_base64(
# b.close(                               b.get_screenshot_as_file(
# b.command_executor                     b.get_screenshot_as_png(
# b.create_options(                      b.get_window_position(
# b.create_web_element(                  b.get_window_rect(
# b.current_url                          b.get_window_size(
# b.current_window_handle                b.implicitly_wait(
# b.delete_all_cookies(                  b.launch_app(
# b.delete_cookie(                       b.log_types
# b.desired_capabilities                 b.maximize_window(
# b.error_handler                        b.minimize_window(
# b.execute(                             b.mobile
# b.execute_async_script(                b.name
# b.execute_script(                      b.orientation
# b.file_detector                        b.page_source
# b.file_detector_context(               b.quit(
# b.find_element(                        b.refresh(
# b.find_element_by_class_name(          b.save_screenshot(
# b.find_element_by_css_selector(        b.service
# b.find_element_by_id(                  b.session_id
# b.find_element_by_link_text(           b.set_network_conditions(
# b.find_element_by_name(                b.set_page_load_timeout(
# b.find_element_by_partial_link_text(   b.set_script_timeout(
# b.find_element_by_tag_name(            b.set_window_position(
# b.find_element_by_xpath(               b.set_window_rect(
# b.find_elements(                       b.set_window_size(
# b.find_elements_by_class_name(         b.start_client(
# b.find_elements_by_css_selector(       b.start_session(
# b.find_elements_by_id(                 b.stop_client(
# b.find_elements_by_link_text(          b.switch_to
# b.find_elements_by_name(               b.switch_to_active_element(
# b.find_elements_by_partial_link_text(  b.switch_to_alert(
# b.find_elements_by_tag_name(           b.switch_to_default_content(
# b.find_elements_by_xpath(              b.switch_to_frame(
# b.forward(                             b.switch_to_window(
# b.fullscreen_window(                   b.title
# b.get(                                 b.w3c
# b.get_cookie(                          b.window_handles


### API of tag element in selenium webdriver
# e.clear(                               e.find_element_by_xpath(               e.get_attribute(                       e.screenshot(
# e.click(                               e.find_elements(                       e.get_property(                        e.screenshot_as_base64
# e.find_element(                        e.find_elements_by_class_name(         e.id                                   e.screenshot_as_png
# e.find_element_by_class_name(          e.find_elements_by_css_selector(       e.is_displayed(                        e.send_keys(
# e.find_element_by_css_selector(        e.find_elements_by_id(                 e.is_enabled(                          e.size
# e.find_element_by_id(                  e.find_elements_by_link_text(          e.is_selected(                         e.submit(
# e.find_element_by_link_text(           e.find_elements_by_name(               e.location                             e.tag_name
# e.find_element_by_name(                e.find_elements_by_partial_link_text(  e.location_once_scrolled_into_view     e.text
# e.find_element_by_partial_link_text(   e.find_elements_by_tag_name(           e.parent                               e.value_of_css_property(
# e.find_element_by_tag_name(            e.find_elements_by_xpath(              e.rect                              

