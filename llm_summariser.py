"""Module for summarising text data with an LLM."""
import os
import json
import requests
import concurrent.futures

import pandas as pd

from prompts import ArticleURLTextPrompts

from dotenv import load_dotenv
load_dotenv("env/alphix_test.env")

class LLMSummariser:
    """Class for summarising text."""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    def __init__(self, gpt_model: str):
        self.gpt_model = gpt_model

    def summarise_txt(self, sys_prompt: str, user_prompt: str) -> dict:
        """Summarise article text."""
        data = {
            "model": self.gpt_model,
            "messages": [
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }
        response = requests.post(url="https://api.openai.com/v1/chat/completions", headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLMSummariser.OPENAI_API_KEY}"},
                json=data)
        
        json_str = response.json()['choices'][0]['message']['content'].split('```json\n')[-1].split('\n```')[0]
        data_dict = json.loads(json_str)

        return data_dict
    
    def summarise_df(self, df: pd.DataFrame, max_workers: int = 5) -> pd.DataFrame:
        """Summarise articles concurrently for dataframe containing `txt_body` col."""
        assert "txt_body" in df.columns, "'txt_body' col must be in df columns."
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                lambda txt: self.summarise_txt(
                    ArticleURLTextPrompts.sys_prompt, ArticleURLTextPrompts.summarise_article_prompt(txt)
                ), df["txt_body"]
            ))
        df['summary'] = results
        return df