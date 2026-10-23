\# Evaluation Suite



\## Purpose

This folder is intended to contain evaluation questions, expected answers, retrieval judgments, and metrics for assessing the East India GeoAssistant.



\## Current Status

The current prototype has undergone basic manual search testing. A formal evaluation dataset and quantitative retrieval evaluation have not yet been completed.



\## Manual Test Cases



| Query | Expected observation | Observed result |

|---|---|---|

| Darbhanga Public School | Matching school record | One matching record |

| Delhi Public School | Matching school record | One matching record |

| XYZ Unknown School 123 | No matching record | No matches |

| Darbhanga | Matching records containing the term | Three matching records |



These checks demonstrate basic search functionality only. They do not establish the accuracy or completeness of a full RAG system.



\## Future Work

\- Create a reviewed set of evaluation questions.

\- Add expected entities and relevant-document judgments.

\- Calculate retrieval metrics such as Precision@k and Recall@k.

\- Evaluate answer correctness and grounding once an LLM-based RAG pipeline is implemented.

