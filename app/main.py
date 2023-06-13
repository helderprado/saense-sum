from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import FastAPI
from pydantic import BaseModel
from app.domain.article import Article
import re
from typing import Literal


def WHITESPACE_HANDLER(k): return re.sub(
    '\s+', ' ', re.sub('\n+', ' ', k.strip()))


model_name = "GiordanoB/mT5_multilingual_XLSum-sumarizacao-PTBR"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

app = FastAPI()


class ArticleURL(BaseModel):
    url: str
    summary_style: Literal["synopsis", "summary"]


@app.post("/summarize_article")
def summarize_article(request: ArticleURL):

    article = Article(url=request.url)

    if request.summary_style == "synopsis":
        min_length = 98
        max_length = 256
    else:
        min_length = 256
        max_length = 512

    input_ids = tokenizer(
        [WHITESPACE_HANDLER(article.document)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        min_length=min_length,
        no_repeat_ngram_size=2,
        num_beams=5
    )[0]

    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    return {"summary": summary}
