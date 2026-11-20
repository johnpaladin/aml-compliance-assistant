"""把 data/raw/*_en.md 的法規切成條文塊、產生 embedding，存到 data/chunks.jsonl。

用法：
    python src/ingest.py              # 切塊 + embedding（需要 GCP）
    python src/ingest.py --dry-run    # 只切塊、印統計，不呼叫 API
"""
import argparse
import json
import os
import re
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/chunks.jsonl")
MAX_CHARS = 2000          # 超過這個長度的條文，依段落再拆
EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768           # 輸出向量維度；768 夠用、檔案小、搜尋快


def parse_header(lines):
    """讀檔案開頭的 metadata：第一行是 '# 法規名稱'，下面是 '- PCODE: xxx' 這種列表。"""
    meta = {"title": lines[0].lstrip("# ").strip()}
    for line in lines[1:]:
        if line.startswith("## "):          # 碰到第一條條文就停
            break
        m = re.match(r"- (\w[\w ]*?): (.+)", line)
        if m:
            meta[m.group(1).lower()] = m.group(2).strip()   # 'PCODE' -> 'pcode'
    return meta


def split_articles(text):
    """依 '## Article N' 切開，回傳 [(條號, 條文內容), ...]。"""
    # re.split 用括號把條號「抓」出來，結果長這樣：
    # [開頭的 metadata, '1', '第1條內容', '2', '第2條內容', ...]
    parts = re.split(r"^## Article (\S+)\s*$", text, flags=re.MULTILINE)
    pairs = []
    for i in range(1, len(parts), 2):      # 從 index 1 開始，每次跳 2 格
        article_no = parts[i]
        body = parts[i + 1].strip()
        pairs.append((article_no, body))
    return pairs


def split_long(body, max_chars=MAX_CHARS):
    """條文太長時，依空行（段落）切開，再把相鄰段落湊到不超過 max_chars。

    為什麼不每 2000 字硬切：會把一句話或一款規定切成兩半，
    兩塊都只剩半個意思，檢索時哪一塊都對不上。
    """
    if len(body) <= max_chars:
        return [body]
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    pieces, current = [], ""
    for p in paragraphs:
        # 加上這段會超過上限，而且 current 已經有內容 → 先收一塊
        if current and len(current) + len(p) + 2 > max_chars:
            pieces.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    if current:
        pieces.append(current)
    return pieces


def build_chunks():
    chunks = []
    for path in sorted(RAW_DIR.glob("*_en.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_header(text.splitlines())
        for article_no, body in split_articles(text):
            pieces = split_long(body)
            for n, piece in enumerate(pieces, start=1):
                chunk_id = f"{meta['pcode']}-art-{article_no}"
                if len(pieces) > 1:
                    chunk_id += f"-p{n}"
                chunks.append({
                    "id": chunk_id,
                    "pcode": meta["pcode"],
                    "title": meta["title"],
                    "article": article_no,
                    "part": n,
                    "source": meta.get("source", ""),
                    # 前面加「法規名稱 + 條號」，embedding 才知道這段屬於哪部法
                    "text": f"{meta['title']}, Article {article_no}\n\n{piece}",
                })
    return chunks


def embed_all(chunks):
    """對每塊呼叫 Vertex AI embedding API，把向量放進 chunk['embedding']。"""
    from google import genai                    # 放在這裡 import：--dry-run 不用裝套件
    from google.genai.types import EmbedContentConfig

    client = genai.Client(
        vertexai=True,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    config = EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",   # 告訴模型：這是要被搜尋的文件
        output_dimensionality=EMBED_DIM,
    )
    for i, chunk in enumerate(chunks, start=1):
        # 一次送一塊：gemini-embedding-001 每次請求只收一段文字
        resp = client.models.embed_content(
            model=EMBED_MODEL, contents=chunk["text"], config=config
        )
        chunk["embedding"] = resp.embeddings[0].values
        print(f"[{i}/{len(chunks)}] {chunk['id']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="只切塊，不呼叫 API")
    args = parser.parse_args()

    chunks = build_chunks()
    lengths = [len(c["text"]) for c in chunks]
    print(f"{len(chunks)} 塊，平均 {sum(lengths) // len(lengths)} 字元，最長 {max(lengths)} 字元")

    if args.dry_run:
        for c in chunks[:3]:
            print("-" * 40, c["id"], "\n", c["text"][:200])
        return

    embed_all(chunks)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")   # JSONL：一行一塊
    print(f"已寫入 {OUT_FILE}")


if __name__ == "__main__":
    main()
