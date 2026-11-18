# Compliance Q&A Assistant: Requirements

Nov 17, 2026 · Chris

Fictional client: the 12-person Compliance Department of a mid-sized Taiwanese commercial bank. The goal is a compliance Q&A assistant that answers only from internal and regulatory documents and cites a source for every answer, starting with the repetitive questions that come in from branches and business units.

## Background and pain points

The Compliance Department spends about 200–300 hours a month answering internal questions, close to two full-time people. Core work such as regulatory analysis keeps getting pushed back.

- **High, repetitive volume**: about 40–50 questions a day (phone, email, Teams), 15–20 minutes each on average. Many repeat questions other units have already asked.
- **Inconsistent answers**: different team members sometimes give different answers to the same question.
- **No record**: there is no ticketing system, so the team cannot track question types or reuse past answers.
- **Knowledge-loss risk**: many answers live only in senior staff's heads or old emails, and the key senior officer retires next year.
- **Skepticism toward AI**: the bank once tried a chatbot that made up regulation article numbers. The client's rule: "a wrong answer is worse than no answer."

## Users and key scenarios

Version 1 serves two user groups and covers the three most common question types.

| User | Purpose | Accessible documents |
| --- | --- | --- |
| Branch and business-unit staff | Self-serve lookups instead of calling Compliance | Regulations, regulatory rulings, current internal policies |
| Compliance staff | Quick article lookup, reuse of past answers, audit preparation | All of the above, plus audit reports and past answers |

Three main question types:

1. **Anti-money laundering (AML)**: e.g. "A customer wants to wire money to country X. What extra checks do we need?"
2. **Special account opening**: accounts for foreign nationals, and identifying the beneficial owners of corporate accounts.
3. **Export controls and sanctions**: "Is this company on a sanctions list?" "Is this item a controlled good?" (trade finance, cross-border remittance)

## Data sources

Each of the four document types has issues to resolve first. The portfolio build uses public regulations plus fictional internal documents, and no real customer data.

| Document | Format | Issues to handle | Access |
| --- | --- | --- | --- |
| Regulations and regulatory rulings | PDF; older ones are scans | OCR for scans; tag issue date and amendment status | All staff |
| Internal policies and SOPs | Word, on a shared drive | Multiple versions of the same file; identify the current one | All staff |
| Past answers | Outlook email | Contain customer personal data, which must be masked before ingestion; unorganized | Compliance |
| Audit reports | To be confirmed | Restricted to specific managers | Compliance and audit managers |

Public sources: the Laws & Regulations Database of the R.O.C., FSC announcements and rulings, and Bankers Association self-regulatory rules.

## Functional requirements

1. **Q&A**: users ask in plain Chinese; the system answers only from the document library.
2. **Citations**: every answer lists its source document and article or paragraph, with a link to the original text.
3. **Say "I don't know"**: when there is no basis, the system clearly answers "no relevant rule found" and suggests contacting Compliance.
4. **Version awareness**: answers use only current versions, and citations show each document's issue or amendment date.
5. **Permission filtering**: users only see documents they are allowed to see; branch staff cannot reach audit reports.
6. **Escalate to a human**: for gray areas, or when the user is not satisfied, one click hands the question to Compliance staff.
7. **Query logging**: every Q&A is logged, to track question types, find document gaps, and support audits.
8. **Sanctions list lookup** (phase 2): connect to sanctions-list data to answer whether a company or item is restricted.

## Constraints

- **Data residency**: customer data stays in Taiwan by default, in line with FSC rules on cloud use and outsourcing by banks, and requires Information Security sign-off.
- **Personal data protection**: historical emails must be masked before ingestion; answers must not leak customer data.
- **Role-based access**: reuse the bank's existing accounts and roles rather than building a separate permission system.
- **Limited operations staff**: IT is short-staffed, so each option must account for who runs it.

Two deployment options will be compared for the client to choose from:

| Option | Advantages | To confirm |
| --- | --- | --- |
| On-premises | Data never leaves the bank | Hardware cost, IT operations load, time to launch |
| GCP Taiwan region | No hardware purchase, faster launch, lighter operations | Compliance with outsourcing rules and filing process; Information Security's view |

The portfolio build is deployed on GCP.

## Success criteria

Before launch, measure the metrics below on a 60–100 question test set. Questions come from real past inquiries, each with a reference answer and the documents it should cite. Targets are provisional and need client confirmation.

| Metric | How it is measured | Provisional target |
| --- | --- | --- |
| Retrieval hit rate | Whether the documents that should be cited are retrieved | ≥ 90% |
| Answer accuracy | Human or LLM-as-judge scoring against the reference answer | ≥ 85% |
| Citation accuracy | Whether the cited sources actually support the answer | ≥ 95% |
| Correct refusal rate | For questions the library cannot answer, whether the system says it doesn't know | ≥ 95% |
| Response time | From question to complete answer | ≤ 5 seconds |

After launch, track whether Compliance's monthly hours spent on inquiries fall from 200–300.

## Out of scope and open questions

**Out of scope**: gray-area judgments (e.g. whether a customer's transaction pattern is suspicious) stay with people. The system surfaces the relevant rules but does not decide.

**Open questions**:

- [ ] Interview Ms. Chen (senior officer): the case types she handles, which can be written as SOPs and which rely on experience
- [ ] Rollout size: how many branches and users in version 1
- [ ] Timeline and budget: target launch date, who approves procurement
- [ ] IT and Information Security contacts, and their views on the two deployment options
- [ ] Target values for the success criteria
- [ ] Interface: standalone web app or Teams integration
- [ ] Deliver an "on-premises vs. Taiwan cloud" comparison to Mr. Lin (Assistant VP): cost, time to launch, operating responsibility

## Working assumptions for this build

The client is fictional, so the portfolio build proceeds on these assumptions until the open questions are answered.

- Version 1 pilots with 3 branches, about 50 users.
- Standalone web app; Teams integration is a later option.
- The provisional targets above are used as eval pass thresholds.
- Scope of v1 data: Taiwan AML/KYC regulations plus fictional internal SOPs; sanctions lookup stays in phase 2.
- Deployment: GCP, Taiwan region (asia-east1).
