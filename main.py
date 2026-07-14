import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI(title="AI Content Generator")
app.mount("/static", StaticFiles(directory="static"), name="static")


class GenerateRequest(BaseModel):
    topic: str


@app.get("/")
def read_index():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate")
def generate_content(request: GenerateRequest):
    from agent import critic_chain, writer_chain
    from tools import scrape_url, web_search

    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    search_results = web_search.invoke({"query": topic})
    urls = re.findall(r"url:\s*(https?://\S+)", search_results)

    scraped_sections = []
    for url in urls[:3]:
        scraped_sections.append(f"Source: {url}\n{scrape_url.invoke({'url': url})}")

    scraped_content = "\n\n".join(scraped_sections).strip()
    if not scraped_content:
        scraped_content = search_results

    blog_post = writer_chain.invoke(
        {
            "topic": topic,
            "scraped_content": scraped_content,
        }
    )
    critique = critic_chain.invoke({"blog_post": blog_post})

    return {
        "status": "success",
        "blog_post": blog_post,
        "critique": critique,
    }
