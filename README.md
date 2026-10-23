\# East India GeoAssistant



\## Project Overview



East India GeoAssistant is a prototype application for searching school-related geographic records using Elasticsearch and Streamlit.



The application provides a web interface where users can search for school names, view matching records, inspect available metadata, and see Elasticsearch relevance scores.



\## Implemented Features



\- GeoPackage-to-JSONL data export.

\- Elasticsearch setup with separate indices for chunks, entities, and relations.

\- Indexing of 1,062 school-related geographic features.

\- Phrase-based retrieval using Elasticsearch.

\- Streamlit web interface for searching and displaying results.

\- Configurable result limit.

\- Display of available record properties and relevance scores.

\- Handling of empty queries, unmatched queries, and search errors.



\## Technology Stack



\- Python

\- Elasticsearch 8.19.3

\- Streamlit

\- GeoServer 2.27.2

\- Kibana 8.19.3

\- GeoPackage and JSONL

\- Docker Desktop



\## Dataset



The supplied GeoPackage contains 1,062 school-tagged building features.



\- Features with non-empty names: 623

\- Features without names: 439

\- Coordinate reference system: EPSG:4326



The dataset contains geographic feature metadata, including available names, OpenStreetMap identifiers, feature classifications, types, and geometries.



It does not provide admissions circulars, board affiliations, seat counts, or cut-off marks. The application must not invent this information.



\## Project Structure



```text

east\_india\_geoassistant/

├── app/

│   ├── geo\_cli.py

│   ├── es\_search.py

│   └── streamlit\_app.py

├── data/

│   ├── schools.gpkg

│   └── schools\_features.jsonl

├── diagram/

│   └── architecture.mmd

├── es/

│   └── mappings\_notes.md

├── evidence/

│   └── FILES\_NEEDED.md

├── ingest/

│   ├── entity\_schema.json

│   └── geopackage\_to\_geojsonl.py

├── retrieve/

│   ├── graph.py

│   └── metrics.py

├── requirements.txt

└── README.md

```



\## Setup



Use Python 3.10 or later, Docker Desktop, and PowerShell on Windows.



Activate the virtual environment:



```powershell

.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Configure the Elasticsearch URL and credentials in a local `.env` file. Do not commit or submit this file.



Start the Elasticsearch service using the configured Docker setup and confirm that it is reachable.



\## Data Export



To regenerate the JSONL dataset from the GeoPackage:



```powershell

python ingest\\geopackage\_to\_geojsonl.py --input data\\schools.gpkg --output data\\schools\_features.jsonl

```



\## Indexing



The exported records are indexed in Elasticsearch under `east\_india\_chunks`.



The indexing process stores each feature's available properties, searchable text, and geometry. Re-run indexing when the dataset is regenerated.



\## Running the Search Application



Start the Streamlit interface:



```powershell

streamlit run app\\streamlit\_app.py

```



Open the local URL shown in the terminal, normally:



```text

http://localhost:8501

```



Enter a school name or partial name and click Search. The interface displays matching records, relevance scores, and available metadata.



The command-line search can also be run with:



```powershell

python app\\es\_search.py "Darbhanga Public School"

```



\## Tests Performed



The following manual tests have been performed:



1\. Exact phrase search for "Darbhanga Public School" returned one matching record.

2\. Exact phrase search for "Delhi Public School" returned one matching record.

3\. A query for an unknown school name returned no matching records.

4\. Partial-name search for "Darbhanga" returned three matching records.

5\. The Streamlit interface successfully displayed search results and record metadata.



These are functional checks, not a formal retrieval-quality evaluation.



\## Current Limitations



The current implementation is a search prototype. It uses Elasticsearch phrase-based retrieval and does not yet implement a complete Retrieval-Augmented Generation (RAG) pipeline.



The following assessment components remain incomplete or require additional evidence:



\- Local LLM and embedding-model integration.

\- Vector and hybrid retrieval.

\- Entity extraction and resolution evaluation.

\- Relation extraction and graph-based retrieval evaluation.

\- Reranking and confidence calibration.

\- Abstention and citation verification.

\- Formal retrieval metrics and held-out evaluation.

\- Complete end-to-end RAG answers.

\- Security and access-control evidence.

\- Architecture diagram export and final assessment documentation.



Missing source documents and evaluation datasets must be obtained before the corresponding experiments can be reported.



\## Security



Never include passwords, API keys, `.env` files, personal data, or other secrets in the submitted archive.



\## Credits and Disclosure



This prototype uses Python, Elasticsearch, Streamlit, GeoServer, Kibana, and geographic data supplied with the starter project. OpenStreetMap identifiers are retained in the source records.



Third-party dependencies and source-data attribution should be reviewed before submission.



\## Reproducibility



Record the software versions, configuration steps, ingestion commands, test queries, and observed results used for the final demonstration. Do not report unrun experiments or fabricated evaluation results.



