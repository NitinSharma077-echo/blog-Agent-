
from langchain_ollama import ChatOllama
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url

import os
load_dotenv()

llm=ChatOllama(model=os.getenv("Ollama_Model", "gemma4"),base_url=os.getenv("Ollama_server", "http://localhost:11434"),temperature=0.1)


writer_prompt=ChatPromptTemplate.from_template(
    """
    Write a detailed 1500-2000 word blog post about {topic}.
    Use the following scraped content as the primary source: 
    {scraped_content}

    Tone: Engaging, professional, and authoritative.

    Structure:
    1. Compelling Title
    2. Introduction (Hook + what will be covered)
    3. Main Body (detailed sections based on scraped content)
    4. Conclusion (Summary + Final thoughts)

    IMPORTANT: Do not hallucinate. If something is not in the scraped_content, say "Information not available in the provided sources."
    """
)
    


researcher_prompt=ChatPromptTemplate.from_template(
    """
    You are a web researcher. 
    Given a topic: {topic}

    Your job is to find the most relevant and recent articles (last 6 months).

    1. Use the `web_search` tool to find URLs.
    2. Use the `scrape_url` tool to extract content from the most relevant URLs.
    3. Return ONLY the scraped content.
    """
)

writer_chain=writer_prompt | llm | StrOutputParser()

critic_prompt=ChatPromptTemplate.from_template(
    """
    You are a content critic. 
    Read the blog post written by the Writer:
    {blog_post}

    Analyze it based on these criteria:
    1. Factual Accuracy (Does it match the scraped_content?)
    2. Readability (Is it easy to understand?)
    3. Tone (Is it engaging and professional?)
    4. Structure (Is it well-organized?)
    5. Completeness (Does it cover the topic well?)
    6. Plagiarism (Did the writer hallucinate or copy too much?)

    Give specific feedback and suggestions for improvement.
    """
)

critic_chain=critic_prompt | llm | StrOutputParser()


