class ClientLandingPagePrompts:

    sys_prompt = """
        You are an AI assistant specialised in analysing financial services content. 
        Your task is to extract key information from the provided client landing page 
        and their About Us page to build a comprehensive understanding of their offering and messaging.
    """

    @staticmethod
    def summarise_client_message(landing_page_txt: str, about_us_txt: str) -> dict:
        prompt = f"""
            **Client Landing Page Text:**
            {landing_page_txt}

            **Client About Us Text:**
            {about_us_txt}

            ---

            **Please extract the following information and present it in a structured JSON format:**

            1.  **"core_investment_philosophy":** (e.g., "long-term value investing in undervalued assets", "growth equity focused on disruptive technologies", "income generation through diversified fixed income")
            2.  **"key_value_proposition":** (What problem do they solve for clients? What's their unique selling point? e.g., "expert-led active management", "cost-effective passive strategies", "personalised financial planning")
            3.  **"target_audience":** (Who are they primarily trying to attract? e.g., "institutional investors", "individual high-net-worth clients", "retail investors seeking retirement solutions")
            4.  **"primary_products_services":** (List major offerings, e.g., "Mutual Funds", "ETFs", "Wealth Management", "Hedge Funds")
            5.  **"brand_tone_and_style":** (Describe the overall tone and communication style: e.g., "Authoritative and data-driven", "Approachable and educational", "Innovative and forward-looking", "Conservative and trustworthy")
            6.  **"key_themes_messaging":** (What are the dominant messages or recurring themes in their content? e.g., "sustainable investing", "risk management", "market volatility resilience", "long-term growth")
            7.  **"compliance_sensitivities":** (Identify any specific areas where compliance might be particularly critical based on their claims or offerings, e.g., "claims of high returns", "complex derivatives", "personalised advice")

            ```json
            {{
            "core_investment_philosophy": "...",
            "key_value_proposition": "...",
            "target_audience": "...",
            "primary_products_services": [],
            "brand_tone_and_style": "...",
            "key_themes_messaging": [],
            "compliance_sensitivities": []
            }}
            ```
            """
        return prompt
        
class ArticleURLTextPrompts:

    sys_prompt = """
        You are an AI assistant specialised in analysing financial news content. 
        """

    @staticmethod
    def summarise_article_prompt(article_txt: str) -> str:
        prompt = f"""
            Your task is to provide a concise semantic profile of a given news article, focusing on its main points, key themes, 
            and overall narrative or implication for financial markets/sectors.

            **News Article Text:**
            {article_txt}

            **Please extract the following information and present it in a structured JSON format:**

            1.  **"article_summary":** (A concise, neutral summary of the main points of the article, max 150 words.)
            2.  **"key_themes":** (A list of 3-5 dominant financial, economic, or market themes discussed or implied by the article. E.g., ["inflationary pressures", "interest rate policy", "tech sector growth", "geopolitical risk", "supply chain disruptions"].)
            3.  **"implied_market_narrative":** (Describe the overall implication or sentiment the article conveys for specific markets, sectors, or asset classes. Is it bullish, bearish, cautious, uncertain, or highlighting a specific trend? E.g., "suggests a cautious outlook for equity markets due to potential rate hikes", "points to increased optimism in renewable energy investments", "highlights ongoing uncertainty in emerging markets".)
            4.  **"primary_entities_mentioned":** (A list of major companies, indices, financial institutions, or key figures mentioned. E.g., ["Bank of America", "Federal Reserve", "S&P 500", "Jerome Powell"].)
            5.  **"impacted_sectors_assets":** (A list of specific economic sectors, industries, or asset classes (e.g., equities, bonds, commodities, real estate) that are most directly impacted or discussed in the context of the article. E.g., ["banking sector", "fixed income", "tech stocks", "consumer staples"].)
            6.  **"sentiment_analysis":** (Categorise the overall sentiment of the article regarding the topics it discusses. Choose from: "Positive", "Neutral", "Negative", "Mixed", "Uncertain".)

            ```json
            {{
            "article_summary": "...",
            "key_themes": [],
            "implied_market_narrative": "...",
            "primary_entities_mentioned": [],
            "impacted_sectors_assets": [],
            "sentiment_analysis": "..."
            }}
            ```
            Note: If the the news article has been webscraped, some of the articles are behind a paywall or have prevented
            the article being scraped. In such cases they return text along the lines of: "We've detected unusual activity from your computer..."
            or "temporary error...". If this is the case, return empty values in the json output.
            """
        return prompt
    
class AdGenerationPrompts:

    sys_prompt = """
    You are an expert marketing strategist and creative director, specializing in generating compelling, context-aware digital ad creative for asset management firms. Your goal is to develop ad concepts that powerfully link a client's core investment message with current financial news developments, ensuring strict compliance and a tone aligned with the client's brand.
    """

    @staticmethod
    def generate_ad_copy(client: str, client_summary: str, relevant_article_summaries: list):

        prompt = f""" 

        **THE CLIENT**

        The client is: {client}

        **CLIENT PROFILE:**

        Below is a summary and semantic profile of the client, derived from their landing page. This represents their core message, value proposition, and brand identity.

        {client_summary}
        ---

        **RELEVANT NEWS CONTEXT:**

        Below are the semantic profiles of a few highly relevant news articles. Integrate themes and implications from these into the ad creative where appropriate, ensuring the ad feels timely and relevant.

        {relevant_article_summaries}
        ---

        **CREATIVE BRIEF:**

        Generate ad copy and imagery suggestions for the following digital ad formats. For each format:

        1.  **Linkage:** Explicitly link the client's message with the news context. The ad should resonate with what's happening now, while promoting the client's solutions.
        2.  **Tone & Compliance:** Maintain the client's `Brand Tone & Style` and strictly adhere to their `Compliance Sensitivities`.
        3.  **Clarity & Conciseness:** Ad copy should be direct and impactful, appropriate for each format.
        4.  **Imagery:**  Propose a scene-level visual concept as a DALL-E 3 prompt. 
        Focus on evocative, specific, and dynamic elements that tell a story or convey an emotion related to the client's message within the news context.
        Avoid generic office scenes, screens, globes, maps, arrows, or stock metaphors. Instead, aim for imagery that is unexpected, metaphorical, 
        or uses unusual perspectives to visually represent the client's solution or the challenge it addresses. 
        Each format should feature a distinct visual narrative that avoids repetition of concepts. 
        Think creatively about scale, light, atmosphere, and the juxtaposition of elements to create truly "outside the box" visuals.

        ---

        **AD TYPE DESCRIPTIONS:**

        LinkedIn Single Image Ad: A single image ad is a form of online advertisement that utilizes a single static image, along with accompanying text like a headline, description, and call-to-action (CTA), to engage an audience.
        Banner Ad: A banner ad is a type of online advertisement, typically rectangular, that appears on web pages to attract users and drive traffic to the advertiser's website. These ads often feature a combination of visuals and a call to action.
        Carousel Ad: A carousel ad is an online advertising format that displays multiple images or videos within a single ad unit, allowing users to swipe or click through to view different content.

        **AD FORMATS & REQUIREMENTS:**

        **1. LinkedIn Single Image Ad:**
            * **Headline:** Max 10 words.
            * **Main Copy:** Max 50 words.
            * **Call to Action (CTA):** Standard LinkedIn CTAs (e.g., "Learn More", "Download Whitepaper", "Visit Website").
            * **Image Suggestion:** Detailed description (A prompt that will work well for DALL-E-3 image generation).

        **2. Banner Ad:**
            * **Headline:** Max 7 words. Very concise.
            * **Main Copy:** Max 20 words (optional, if space allows).
            * **CTA:** Short and punchy.
            * **Image Suggestion:** Concise description.

        **3. Carousel Ad (3 slides - LinkedIn/Facebook):**
            * **Overall Theme/Narrative:** A unifying concept for the carousel.
            * **Slide 1:**
                * Headline: Max 10 words.
                * Copy: Max 30 words.
                * Image Suggestion: Description.
            * **Slide 2:**
                * Headline: Max 10 words.
                * Copy: Max 30 words.
                * Image Suggestion: Description.
            * **Slide 3:**
                * Headline: Max 10 words.
                * Copy: Max 30 words.
                * Image Suggestion: Description.
            * **Overall CTA:** One final CTA for the entire carousel.
            
            NOTE: You *must* the different slides all relate to one another and the sequence of images follow each other naturally.

        **4. Display Creative (General Web Display):**
            * **Headline:** Max 15 words.
            * **Main Copy:** Max 60 words.
            * **CTA:** Clear and direct.
            * **Image Suggestion:** Detailed description.

        ---

        **OUTPUT STRUCTURE:**

        Please provide your output as a single JSON object. The top-level key should be "ad_creatives", containing an array of ad objects, one for each format. Each ad object should include:

        ```json
        {{
        "ad_creatives": [
            {{
            "format": "LinkedIn Single Image Ad",
            "headline": "...",
            "main_copy": "...",
            "call_to_action": "...",
            "imagery_suggestion": "...",
            "linkage_justification": "Explanation of how client message links to news theme."
            }},
            {{
            "format": "Banner Ad",
            "headline": "...",
            "main_copy": "...",
            "call_to_action": "...",
            "imagery_suggestion": "...",
            "linkage_justification": "..."
            }},
            {{
            "format": "Carousel Ad",
            "overall_theme": "...",
            "slides": [
                {{
                "slide_number": 1,
                "headline": "...",
                "copy": "...",
                "imagery_suggestion": "..."
                }},
                {{
                "slide_number": 2,
                "headline": "...",
                "copy": "...",
                "imagery_suggestion": "..."
                }},
                {{
                "slide_number": 3,
                "headline": "...",
                "copy": "...",
                "imagery_suggestion": "..."
                }}
            ],
            "overall_call_to_action": "...",
            "linkage_justification": "..."
            }},
            {{
            "format": "Display Creative",
            "headline": "...",
            "main_copy": "...",
            "call_to_action": "...",
            "imagery_suggestion": "...",
            "linkage_justification": "..."
            }}
        ]
        }}
        ```
        """

        return prompt

