"""Module for summarising text data with an LLM."""
import os
import json
import openai
import concurrent.futures

import pandas as pd

from prompts import ArticleURLTextPrompts

from dotenv import load_dotenv
load_dotenv("env/alphix_test.env")

class LLMHelper:
    """Class for summarising text and generating ad images."""

    def __init__(self):
        self.gpt_model = os.getenv("OPENAI_MODEL_NAME")
        self.image_model = os.getenv("OPENAI_IMAGE_MODEL_NAME")
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarise_txt(self, sys_prompt: str, user_prompt: str) -> dict:
        """Summarise article text."""
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        raw_text = response.choices[0].message.content
        json_str = raw_text.split('```json\n')[-1].split('\n```')[0]
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
    
    def generate_ad_image(self, ad: dict, n_ads: int = 1, size: str = "1024x1024") -> tuple[str, dict] | list[tuple[str, dict]]:
        """Generate ad image based on imagery suggestion."""

        if ad["format"] == "Carousel Ad":
            slides = []
            for slide in ad["slides"]:
                response = self.client.images.generate(
                    model=self.image_model,
                    prompt=slide["imagery_suggestion"],
                    n=n_ads,
                    size=size
                )
                slides.append((response.data[0].url, slide))
            return slides

        response = self.client.images.generate(
            model=self.image_model,
            prompt=ad['imagery_suggestion'],
            n=n_ads,
            size=size
        )
        return response.data[0].url, ad