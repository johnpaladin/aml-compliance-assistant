# Data Sources

All documents are public regulations from the **Laws & Regulations Database of the R.O.C. (Taiwan)** (全國法規資料庫, https://law.moj.gov.tw).
Under Article 9 of Taiwan's Copyright Act, laws, regulations and official documents are not subject to copyright.

Retrieved: 2026-11-18

## Regulations (v1)

| PCODE | Title (zh) | Title (en) | Last amended | Files |
| --- | --- | --- | --- | --- |
| G0380131 | 洗錢防制法 | Money Laundering Control Act | 2024-07-31 | `raw/G0380131_zh.pdf`, `raw/G0380131_en.md` |
| I0030047 | 資恐防制法 | Counter-Terrorism Financing Act | 2018-11-07 | `raw/I0030047_zh.pdf`, `raw/I0030047_en.md` |
| G0380252 | 金融機構防制洗錢辦法 | Regulations Governing Anti-Money Laundering of Financial Institutions | 2021-12-14 | `raw/G0380252_zh.pdf`, `raw/G0380252_en.md` |
| G0380262 | 銀行業及其他經金融監督管理委員會指定之金融機構防制洗錢及打擊資恐內部控制與稽核制度實施辦法 | Regulations Governing Internal Audit and Internal Control System of AML/CFT of Banking Business and Other Financial Institutions Designated by the FSC | 2021-12-14 | `raw/G0380262_zh.pdf`, `raw/G0380262_en.md` |

Source pages:

- Chinese: `https://law.moj.gov.tw/LawClass/LawAll.aspx?PCODE=<PCODE>`
- English: `https://law.moj.gov.tw/ENG/LawClass/LawAll.aspx?pcode=<PCODE>`

File formats:

- `*_zh.pdf`: the Chinese PDF downloaded from the database.
- `*_en.md`: the English page converted to Markdown, one `## Article N` heading per article. The English site offers no PDF download.

## Excluded

| PCODE | Title | Reason |
| --- | --- | --- |
| G0380206 | 金融機構對達一定金額以上通貨交易及疑似洗錢交易申報辦法 (CTR/STR Regulations) | **Repealed (abolished) on 2017-06-26.** Cash transaction reports (NT$500,000 threshold) and suspicious transaction reports are now covered by G0380252. The database still serves its full text, so a naive crawler would ingest it. Kept out of the corpus and reserved as an eval case: the assistant must not cite a repealed regulation. |

## Notes

- **The Chinese text is authoritative.** English versions are official translations for reference and may lag behind the latest Chinese amendment. Check the date on each English page before relying on it.
- "Last amended" is the date shown on the Chinese page at retrieval time. Re-check before each data refresh; the system must answer only from current versions (see requirement 4 in [docs/requirements.md](../docs/requirements.md)).
- Fictional internal SOPs will be added under `internal/` and labeled as fictional.
- Bankers Association self-regulatory rules (銀行公會範本) are not government documents; they will be linked here rather than committed.
