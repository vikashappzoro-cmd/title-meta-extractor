import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_seo_data(url):
    """
    Extracts title, meta title, and meta description from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Title
        title = soup.title.string if soup.title else "N/A"
        # Remove "<title>" and "</title>" tags if present
        if title.startswith("<title>") and title.endswith("</title>"):
            title = title[len("<title>"):-len("</title>")].strip()
        else:
            title = title.strip() # Remove leading/trailing whitespace

        # Extract Meta Title (from og:title or title tag)
        meta_title_tag = soup.find('meta', property='og:title') or \
                         soup.find('meta', {'name': 'title'})
        meta_title = meta_title_tag['content'].strip() if meta_title_tag else title

        # Extract Meta Description
        meta_description_tag = soup.find('meta', property='og:description') or \
                               soup.find('meta', {'name': 'description'})
        meta_description = meta_description_tag['content'].strip() if meta_description_tag else "N/A"

        return title, meta_title, meta_description
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", "N/A", "N/A"
    except Exception as e:
        return f"Error parsing HTML: {e}", "N/A", "N/A"

st.set_page_config(page_title="Title Meta Extractor", layout="wide")

st.title("Title Meta Extractor")
st.markdown("---")

st.write("Enter URLs (one per line) in the text area below:")
urls_input = st.text_area("URLs", height=200, placeholder="https://example.com\nhttps://another-example.org")

if st.button("Extract SEO Data"):
    if urls_input:
        urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
        if not urls:
            st.warning("Please enter at least one URL.")
        else:
            results = []
            for url in urls:
                with st.spinner(f"Extracting data from {url}..."):
                    title, meta_title, meta_description = extract_seo_data(url)
                    results.append({
                        "URL": url,
                        "Title": title,
                        "Meta Title": meta_title,
                        "Meta Description": meta_description
                    })
            
            st.markdown("### Extraction Results")
            for result in results:
                st.subheader(f"URL: {result['URL']}")
                st.write(f"**Page Title:** {result['Title']}")
                st.write(f"**Meta Title:** {result['Meta Title']}")
                st.write(f"**Meta Description:** {result['Meta Description']}")
                st.markdown("---")
    else:
        st.warning("Please enter URLs in the text area.")

st.markdown("---")
st.markdown("Made by Vikash Goyal")
