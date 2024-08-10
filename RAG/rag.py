import os
from langchain.schema import Document
from chromaClient import ChromaClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
import yaml
import json
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()
config.read('config.ini')

def load_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def create_documents_from_text(text):
    return [Document(page_content=text)]

def chunk_documents(input_path):
    text_content = load_text_file(input_path)
    docs = create_documents_from_text(text_content)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits    
     
def fetch_relevant_docs(settings):
    with open('query.yaml', 'r') as file:
            query = yaml.safe_load(file)

    # Access variables from the config file
    strength_query = query['strength_query']
    weakness__query = query['weakness_query']
    opportunity_query = query['opportunity_query']
    threat_query = query['threat_query']

    chunks = chunk_documents(settings['text_path'])
    client = ChromaClient(collection_name=settings['collection'], persist_directory=settings['db'])
    client.add_documents(chunks)

    strength_results = client.similarity_search(strength_query)
    weakness_results = client.similarity_search(weakness__query)
    opportunity_results = client.similarity_search(opportunity_query)
    threat_results = client.similarity_search(threat_query)
    return [strength_results, weakness_results, opportunity_results, threat_results]

def save_docs2json(results, filename):
    with open(filename, 'w') as file:
        json.dump([doc.page_content for doc in results], file, indent=4)

def save_docs(results, year):
    file_names = ['strength_results.json', 'weakness_results.json', 'opportunity_results.json', 'threat_results.json']
    for result, file_name in zip(results, file_names):
        save_docs2json(result, os.path.join("result",file_name, f'_{year}'))


def main():
    settings_22 = config['setting_2022']
    settings_23 = config['setting_2023']
    result_22 = fetch_relevant_docs(settings_22)
    result_23 = fetch_relevant_docs(settings_23)
    save_docs(result_22, 2022)
    save_docs(result_23, 2023)


if __name__ == "__main__":
    main()
