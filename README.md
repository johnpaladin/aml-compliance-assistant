# AML Compliance Assistant

A RAG-based Q&A assistant that helps bank compliance staff answer AML/KYC questions, grounded in Taiwan's public regulations, with citations for every answer. Deployed on Google Cloud.

> Portfolio project. The client scenario is fictional; all regulatory sources are public.

## Status

🚧 Week 1: scoping and data collection.

## Scope (v1)

- Domain: AML / KYC only
- Users: ~50 compliance staff across 3 branches (fictional bank)
- Interface: standalone web app
- Region: GCP `asia-east1`

See [docs/requirements.md](docs/requirements.md) for the full requirements.

## Planned stack

- Gemini + Vertex AI embeddings
- FastAPI backend on Cloud Run
- Evals: retrieval hit rate + LLM-as-judge, run in CI

## Data

Public Taiwan AML/CFT regulations. See [data/SOURCES.md](data/SOURCES.md) for sources and retrieval dates.

## License

Code under MIT. Regulatory texts are public government documents.
