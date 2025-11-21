import logging
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import config


logger = logging.getLogger(__name__)


class InstagramURLCollector:
    
    def __init__(self):
        self.username = config.insta_username
        self.password = config.insta_password
        self.target_profile = config.insta_target_profile
        self.max_scroll_attempts = config.max_scroll_attempts
        self.delay_between_requests = config.delay_between_requests
        self.wait_timeout = config.wait_timeout
        self.driver = None
    
    def _init_driver(self):
        options = webdriver.ChromeOptions()
        if config.headless_browser:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
    
    def _login(self):
        logger.info(f"Fazendo login como {self.username}...")
        
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        WebDriverWait(self.driver, self.wait_timeout).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password + Keys.RETURN)
        
        WebDriverWait(self.driver, self.wait_timeout).until(
            EC.url_contains("instagram.com")
        )
        
        logger.info("Login realizado com sucesso!")
        time.sleep(3)
        
        for _ in range(3):
            try:
                btn = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Agora nao')]"))
                )
                btn.click()
                time.sleep(0.5)
            except:
                pass
    
    def _open_profile(self):
        logger.info(f"Abrindo perfil: @{self.target_profile}")
        
        self.driver.get(f"https://www.instagram.com/{self.target_profile}/")
        time.sleep(3)
    
    def collect_urls(self) -> List[str]:
        try:
            self._init_driver()
            self._login()
            self._open_profile()
            
            return self._scroll_and_collect()
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def _scroll_and_collect(self) -> List[str]:
        logger.info("Iniciando coleta de URLs com scrolling...")
        
        post_links = []
        scroll_attempts = 0
        
        while scroll_attempts < self.max_scroll_attempts:
            
            anchors = self.driver.find_elements(
                By.XPATH,
                f"//a[starts-with(@href, '/{self.target_profile}/p/') or starts-with(@href, '/{self.target_profile}/reel/')]"
            )
            
            new_urls_count = 0
            for a in anchors:
                href = a.get_attribute("href")
                if href not in post_links:
                    post_links.append(href)
                    new_urls_count += 1
            
            progress_pct = ((scroll_attempts + 1) / self.max_scroll_attempts) * 100
            logger.info(
                f"Scroll {scroll_attempts + 1}/{self.max_scroll_attempts} | "
                f"URLs: {len(post_links)} | Novos: {new_urls_count} | "
                f"Progresso: {progress_pct:.1f}%"
            )
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.delay_between_requests)
            
            scroll_attempts += 1
        
        logger.info(f"Coleta concluída! Total de URLs: {len(post_links)}")
        return post_links
