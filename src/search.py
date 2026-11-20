"""問一個問題，從 data/chunks.jsonl 找出最相關的幾條法規。

用法：
    python src/search.py "What must a bank do when it suspects money laundering?"
"""
import json
import os
import sys

import numpy as np

CHUNKS_FILE = "data/chunks.jsonl"
EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768        # 要跟 ingest.py 一樣，向量才能比較
TOP_K = 3


def load_chunks():
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def embed_query(question):
    from google import genai
    from google.genai.types import EmbedContentConfig

    client = genai.Client(
        vertexai=True,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    resp = client.models.embed_content(
        model=EMBED_MODEL,
        contents=question,
        # 問題用 RETRIEVAL_QUERY，文件用 RETRIEVAL_DOCUMENT：模型對兩邊做不同最佳化
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY", output_dimensionality=EMBED_DIM),
    )
    return np.array(resp.embeddings[0].values)


def top_k(query_vec, chunks, k=TOP_K):
    """cosine 相似度 = 兩個向量的夾角有多小，1 最像、0 無關。"""
    matrix = np.array([c["embedding"] for c in chunks])      # 形狀：(塊數, 768)
    # 先把每個向量除以自己的長度（正規化），之後內積就等於 cosine
    matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    q = query_vec / np.linalg.norm(query_vec)
    scores = matrix @ q                                      # 一次算出所有塊的分數
    best = np.argsort(scores)[::-1][:k]                      # 分數由大到小，取前 k 個
    return [(float(scores[i]), chunks[i]) for i in best]


def main():
    if len(sys.argv) < 2:
        print('用法：python src/search.py "你的問題"')
        return
    question = sys.argv[1]
    chunks = load_chunks()
    for score, c in top_k(embed_query(question), chunks):
        print(f"\n[{score:.3f}] {c['title']} 第 {c['article']} 條  ({c['id']})")
        print(f"  {c['source']}")
        print("  " + c["text"].split("\n\n", 1)[1][:300].replace("\n", " ") + " ...")


if __name__ == "__main__":
    main()
