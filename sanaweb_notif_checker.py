from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
from config import SamaWebNotifCheckerConfig
from pyrogram import Client
from time import sleep
import jdatetime
from proxy import tg_proxy, proxy_host, proxy_port


class SamaWebNotifChecker:
    def __init__(self, user_id):
        self.cfg = SamaWebNotifCheckerConfig()
        self.driver = self._setup_driver()
        self.now_date = self._get_now_date()
        self.user_id = user_id
        self.api_id = ''
        self.api_hash = ''
        self.bot = Client(
            name='smweb',
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.cfg.token,
            proxy=tg_proxy
            )


    def run(self):
        self._login_to_samaweb()
        self.bot.start()
        self._check_new_notif()
        self.bot.stop()

    def loop(self):
        pass

    def _setup_driver(self):
        options = Options()
        excluded_url = 'https://samaweb.zaums.ac.ir/CAS/Account/Login'  # Exclude the specific URL from proxy

        # options.add_argument(f"--proxy-server={proxy_host}:{proxy_port}")
        options.add_argument(f"--no-proxy-server={excluded_url}")
        # options.add_argument("--headless=new") 

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    
    def _login_to_samaweb(self):
        sleep(3)
        self.driver.get(self.cfg.login_url)

        username_field = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/form/div[1]/div/input')
        username_field.send_keys('username')
        sleep(2)
        username_field = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/form/div[2]/div/input')
        username_field.send_keys('password')
        sleep(2)
        login_btn = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/form/div[3]/div/button')
        login_btn.click()
        print('- Logged in to system.')

    def _check_new_notif(self):
        notif_button = self.driver.find_element(By.XPATH, '//*[@id="notification-button"]')
        notif_counter = notif_button.find_element(By.XPATH, """.//span[2]""").text

        try:
            if notif_counter != '0':
                print(f'There is {notif_counter} notification/s')
                notif_button.click()
                class_arrowup = self.driver.find_element(By.XPATH, '//*[@id="notification-panel"]')
                sleep(3)
                for count in range(1, int(notif_counter) + 1):
                    row_arrowup = class_arrowup.find_element(By.XPATH, '//*[@id="notification-panel"]/div[2]')
                    div_count = str(count)
                    message_row = row_arrowup.find_element(By.XPATH, f'//*[@id="notification-panel"]/div[2]/div[{div_count}]')
                    notif_date = message_row.find_element(By.XPATH, f'//*[@id="notification-panel"]/div[2]/div[{div_count}]/div[3]/div').text
                    notif_text = message_row.find_element(By.XPATH, f'//*[@id="notification-panel"]/div[2]/div[{div_count}]/div[2]/div[2]').text
                    seen_notif = message_row.find_element(By.XPATH, '//*[@id="notification-panel"]/div[2]/div/div[3]/a')

                    print("You have a new notif.")
                    self.bot.send_message(self.user_id, text=f"تاریخ اعلان: {notif_date}\n\n{notif_text}")
                        # seen_notif.click()
                    print('Notif seen.')

        except Exception as e:
            print('New notif not found.')
        sleep(2)
 

    def _get_now_date(self):
        jdate = jdatetime.datetime.now()
        jdate = str(jdate)

        return str(jdate[0:10].replace('-', '/')) # -> 1402/04/21
    