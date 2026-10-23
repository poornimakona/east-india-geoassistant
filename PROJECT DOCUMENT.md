\# East India GeoAssistant

\## Project Documentation



\### 1. Project Overview

East India GeoAssistant is a prototype application for searching school-related geographic records using Elasticsearch. It provides a simple web interface built with Streamlit.



\### 2. Objective

The objective is to make school records easier to search by school name and display the available information in a user-friendly interface.



\### 3. Technologies Used

\- Python

\- Streamlit

\- Elasticsearch 8.19.3

\- GeoPandas and GeoPackage data

\- GeoServer

\- Docker Desktop



\### 4. System Workflow

1\. School geographic data is exported from a GeoPackage file into JSON Lines format.

2\. The exported records are indexed in Elasticsearch.

3\. The user enters a school name in the Streamlit interface.

4\. The application submits a phrase-based search to Elasticsearch.

5\. Matching records, relevance scores, and available properties are displayed.



\### 5. Dataset

The dataset contains 1,062 school-tagged building features. The exported data uses the EPSG:4326 coordinate reference system.



The dataset includes named and unnamed features. It does not contain admission circulars, affiliation records, seat availability, or cutoff marks.



\### 6. Implemented Features

\- GeoPackage-to-JSONL data export.

\- Elasticsearch indexing of 1,062 records.

\- Phrase-based school-name search.

\- Streamlit web interface.

\- Display of matching records, relevance scores, and record properties.

\- Handling of empty queries and searches with no matches.

\- Basic command-line search support.



\### 7. Project Structure

\- `data/` — geographic dataset and exported records.

\- `ingest/` — data export and ingestion utilities.

\- `retrieve/` — retrieval-related utilities.

\- `es/` — Elasticsearch mapping notes.

\- `app/` — command-line search, Elasticsearch search, and Streamlit interface.

\- `geoserver/` — GeoServer-related configuration and documentation, if present.

\- `evalsuite/` — evaluation resources, if present.

\- `evidence/` — project evidence and supporting notes.

\- `diagram/` — architecture diagram source.

\- `requirements.txt` — Python dependencies.



\### 8. Setup and Execution

Activate the project's Python virtual environment and ensure Elasticsearch is running with the credentials configured locally in `.env`.



Export the dataset:



`python ingest/geopackage\\\_to\\\_geojsonl.py --input data/schools.gpkg --output data/schools\\\_features.jsonl`



Run the command-line search:



`python app/geo\\\_cli.py --data data/schools\\\_features.jsonl`



Run the web application:



`streamlit run app/streamlit\\\_app.py`



Open `http://localhost:8501` in a browser.



\### 9. Basic Testing

The following searches were tested manually:



\- `Darbhanga Public School` — returned one matching record.

\- `Delhi Public School` — returned one matching record.

\- `XYZ Unknown School 123` — returned no matching records.

\- `Darbhanga` — returned three matching records.



These are manual functional checks, not a formal retrieval evaluation.



\### 10. Current Limitations

This implementation is a working search prototype, not a complete Retrieval-Augmented Generation (RAG) system. It does not currently provide a verified local LLM generation pipeline, embedding-based retrieval, reranking, or a complete evaluation suite.



The available dataset does not support answering questions about admissions, affiliations, seat availability, or cutoff marks. Such information must not be inferred or fabricated.



\### 11. Security and Reproducibility

Credentials must be stored locally and must not be included in the submitted ZIP file. The virtual environment and temporary authentication files should also be excluded. Setup commands and dependencies should be documented so the prototype can be reproduced.



\### 12. Conclusion

The prototype demonstrates geographic school-data export, Elasticsearch indexing, and interactive school-name search. Further work is required to implement and evaluate the complete RAG and LLM workflow specified in the assessment.s



\### 13. Algorithm Notes



\*\*BM25:\*\* BM25 ranks text documents based on query-term matches, term frequency, inverse document frequency, and document-length normalisation. The current prototype uses Elasticsearch phrase-based matching; a dedicated BM25 retrieval mode has not yet been implemented.



\*\*HNSW:\*\* Hierarchical Navigable Small World is an approximate nearest-neighbour algorithm that organises vectors into a graph for efficient similarity search. Vector embeddings and HNSW search have not yet been implemented in this prototype.



\*\*Reciprocal Rank Fusion (RRF):\*\* RRF combines multiple ranked lists by assigning scores based on the rank of each result. Hybrid retrieval using RRF has not yet been implemented.



\*\*Cross-encoder:\*\* A cross-encoder scores a query and passage together to estimate their relevance. Reranking with a cross-encoder has not yet been implemented.



\*\*Softmax with temperature:\*\* Softmax converts scores into a probability distribution. Temperature controls how concentrated that distribution is. Confidence calibration and temperature scaling have not yet been implemented.



\*\*Greedy decoding:\*\* Greedy decoding selects the highest-scoring next token at each generation step. A local LLM generation pipeline has not yet been implemented. Greedy decoding does not guarantee that an answer is correct.



\*\*Graph traversal:\*\* Graph traversal follows relationships between connected entities to discover related information. The project contains graph-related utilities, but a complete graph-based retrieval pipeline has not yet been implemented and evaluated.



\### 14. Assistance, Libraries and Disclosures



ChatGPT was used for explanations, documentation assistance, and troubleshooting. Third-party software includes Python, Streamlit, Elasticsearch, Docker, GeoServer, and the libraries listed in requirements.txt.



The current implementation is an Elasticsearch-based school-search prototype. It does not yet implement or evaluate every task specified in the assessment.



The available dataset contains school-tagged building features. It does not provide verified admissions circulars, seat availability, cutoff marks, or board affiliations. These details must not be inferred or fabricated.



No passwords, API keys, or other credentials should be included in the submission ZIP.



\### 15. Future Work



\- Implement and evaluate entity extraction and entity resolution.

\- Generate embeddings and configure dense-vector search.

\- Build and evaluate graph relationships and graph traversal.

\- Implement keyword, vector, hybrid, and graph-expanded retrieval.

\- Add reranking and confidence calibration.

\- Implement grounded LLM answers with validated citations and abstention.

\- Complete the evaluation datasets, metrics, result tables, and architecture diagram.

