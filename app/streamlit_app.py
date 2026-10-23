import streamlit as st
from es_search import search_schools

st.set_page_config(page_title="East India GeoAssistant", page_icon="🏫", layout="wide")

st.title("East India GeoAssistant")
st.write("Search school records using Elasticsearch.")

query = st.text_input("Enter school name", placeholder="e.g. Darbhanga Public School")
limit = st.slider("Maximum results", 1, 10, 5)

if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("Please enter a school name.")
    else:
        try:
            with st.spinner("Searching school records..."):
                results = search_schools(query.strip(), limit)

            if results:
                st.success(f"Found {len(results)} matching school(s).")
                for i, school in enumerate(results, 1):
                    with st.container(border=True):
                        st.subheader(f"{i}. {school['name']}")
                        st.caption(f"Relevance score: {school['score']}")
                        with st.expander("View available record details"):
                            st.json(school["properties"])
            else:
                st.info("No matching schools found.")

        except Exception as error:
            st.error(f"Search failed: {error}")