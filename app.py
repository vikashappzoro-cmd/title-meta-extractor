import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd # Import pandas for dataframes

def extract_seo_data(url):
    """
    Extracts title, meta title, and meta description from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Extract Page Title from <title> tag ---
        page_title = soup.title.string if soup.title else "N/A"
        # Clean up the page_title aggressively
        page_title = ' '.join(page_title.split()).strip() if page_title != "N/A" else "N/A"

        # --- Extract Meta Title ---
        # Prioritize og:title, then name="title", then fall back to page_title
        meta_title_tag_og = soup.find('meta', property='og:title')
        meta_title_tag_name = soup.find('meta', {'name': 'title'})
        
        meta_title = "N/A"
        if meta_title_tag_og and 'content' in meta_title_tag_og.attrs:
            meta_title = ' '.join(meta_title_tag_og['content'].split()).strip()
        elif meta_title_tag_name and 'content' in meta_title_tag_name.attrs:
            meta_title = ' '.join(meta_title_tag_name['content'].split()).strip()
        elif page_title != "N/A":
            meta_title = page_title # Fallback to page title if no specific meta title found

        # --- Extract Meta Description ---
        # Prioritize og:description, then name="description"
        meta_description_tag_og = soup.find('meta', property='og:description')
        meta_description_tag_name = soup.find('meta', {'name': 'description'})
        
        meta_description = "N/A"
        if meta_description_tag_og and 'content' in meta_description_tag_og.attrs:
            meta_description = ' '.join(meta_description_tag_og['content'].split()).strip()
        elif meta_description_tag_name and 'content' in meta_description_tag_name.attrs:
            meta_description = ' '.join(meta_description_tag_name['content'].split()).strip()

        return page_title, meta_title, meta_description
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}", "N/A", "N/A"
    except Exception as e:
        return f"Parsing Error: {e}", "N/A", "N/A"

st.set_page_config(page_title="Title Meta Extractor", layout="wide")

st.title("Title Meta Extractor")
st.markdown("---")

st.write("Enter URLs (one per line) in the text area below:")
urls_input = st.text_area("URLs", height=200, placeholder="https://sarahospitalityusa.com/blog/modern-lobby-furniture-design-trends-us-hotels\nhttps://sarahospitalityusa.com/blog/selecting-right-hotel-casegoods-is-an-art-want-to-master-it")

if st.button("Extract SEO Data"):
    if urls_input:
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
        if not urls:
            st.warning("Please enter at least one URL.")
        else:
            results_data = []
            for url in urls:
                with st.spinner(f"Extracting data from {url}..."):
                    page_title, meta_title, meta_description = extract_seo_data(url)
                    results_data.append({
                        "URL": url,
                        "Page Title": page_title,
                        "Meta Title": meta_title,
                        "Meta Description": meta_description
                    })
            
            if results_data:
                st.markdown("### Extraction Results")
                df = pd.DataFrame(results_data)
                st.dataframe(df, height=300, use_container_width=True) # Display as a table
            else:
                st.info("No data extracted. Please check the URLs.")
    else:
        st.warning("Please enter URLs in the text area.")

st.markdown("---")
st.markdown("Made by Vikash Goyal")
