import trafilatura
import asyncio

import pandas as pd

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class ScrapeURLs:

    def __init__(self, xlsx_sheet: str):
        self.xlsx_file = pd.ExcelFile(xlsx_sheet)
        self.sheet_names = self.xlsx_file.sheet_names
        self.client_urls = self.read_client_urls()
        self.sheets = {}


    def read_client_urls(self) -> list:

        client_landing_urls = []
        
        for sheet_name in self.sheet_names:
            df = self.xlsx_file.parse(sheet_name=sheet_name)
            client_landing_urls.append(df.iloc[0][0][5:].strip()) # Append client landing url str
        
        return client_landing_urls
    
    def webscrape_client_urls(self) -> dict:

        client_urls_txt = {}

        for client_url in self.client_urls:
            client_urls_txt[client_url] = trafilatura.extract(trafilatura.fetch_url(client_url), url=client_url)
        return client_urls_txt
    
    async def webscrape_relevant_docs(self, sheet_name: str) -> None:
        docs_df = self.xlsx_file.parse(sheet_name=sheet_name)[2:]
        docs_df.columns = docs_df.iloc[0] # Assign Title, Source, Published Date, URL to column headers
        docs_df.drop([docs_df.index[0], docs_df.index[-1]], inplace=True)
        docs_df.reset_index(drop=True, inplace=True)
        for url in docs_df["URL"]:

            txt_body = trafilatura.extract(trafilatura.fetch_url(url), url=url)

            if not txt_body or txt_body == "":
                
                txt_body = await self.scrape_with_playwright(url)
            
            docs_df.loc[docs_df["URL"] == url, "txt_body"] = txt_body
            self.sheets[sheet_name] = docs_df

    async def scrape_with_playwright(self, url: str, wait_for_selector: str | None = None, wait_time_seconds: int = 3) -> str:
        """
        Asynchronously scrapes the rendered HTML content from a URL using Playwright
        and then parses it with BeautifulSoup to extract main textual content.

        Args:
            url (str): The URL of the webpage to scrape.
            wait_for_selector (str, optional): A CSS selector to wait for before extracting HTML.
                                            Useful for dynamically loaded content.
            wait_time_seconds (int): Time in seconds to wait for page to load if no selector.

        Returns:
            str: The extracted main text content, or None if an error occurs.
        """
        html_content = None
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch() # Use await
                page = await browser.new_page()     # Use await
                
                print(f"Attempting to navigate to: {url} with Playwright (Async)")
                await page.goto(url, wait_until='domcontentloaded', timeout=60000) # Use await

                if wait_for_selector:
                    print(f"Waiting for selector: '{wait_for_selector}'")
                    try:
                        await page.wait_for_selector(wait_for_selector, state='attached', timeout=30000) # Use await
                    except Exception as e:
                        print(f"Warning: Selector '{wait_for_selector}' not found or timed out. Proceeding anyway. Error: {e}")
                        await asyncio.sleep(wait_time_seconds) # Use asyncio.sleep in async code
                else:
                    print(f"Waiting for {wait_time_seconds} seconds for content to load.")
                    await asyncio.sleep(wait_time_seconds) # Use asyncio.sleep

                html_content = await page.content() # Use await
                print(f"Successfully retrieved rendered HTML from: {url}")
                await browser.close() # Use await
        except Exception as e:
            print(f"An error occurred while using Playwright (Async) on {url}: {e}")
            return None

        if not html_content:
            return None

        # Parsing with BeautifulSoup remains synchronous as it operates on a string
        soup = BeautifulSoup(html_content, 'html.parser')

        main_content_div = None
        common_content_selectors = [
            'article',
            'div[itemprop="articleBody"]',
            'div.article-content',
            'div.news-content',
            'div[id*="main-content"]',
            'div.c-ArticleBox_body',
            'div.post-content'
        ]
        
        for selector in common_content_selectors:
            potential_main = soup.select_one(selector)
            if potential_main:
                main_content_div = potential_main
                break
        
        if not main_content_div:
            main_content_div = soup.find('body')
            if not main_content_div:
                print("Could not find a suitable main content div within the rendered HTML.")
                return None

        for unwanted_tag in ['nav', 'header', 'footer', 'aside', 'form', 'script', 'style', 'img', 'link', 'figure', 'figcaption', 'noscript', 'meta', '.ads-container', '.promo', '.social-share-bar']:
            for tag in main_content_div.find_all(unwanted_tag):
                tag.decompose()

        extracted_text_parts = []
        text_elements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'strong', 'em', 'blockquote']
        for element in main_content_div.find_all(text_elements):
            text = element.get_text(strip=True)
            if text:
                extracted_text_parts.append(text)

        full_text = "\n\n".join(extracted_text_parts)
        full_text = '\n'.join(filter(lambda x: x.strip(), full_text.splitlines()))

        return full_text