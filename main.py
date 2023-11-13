# This script processes a webpage's Document Object Model (DOM) and generates a JSON file for web scraping purposes.
# The input is a TXT file containing the fully rendered DOM. The output is a JSON file with structured data of all webpage elements.

# The script performs the following steps:
# 1. Reads the DOM content from the TXT file.
# 2. Parses the DOM using lxml library, which provides easy extraction and XPath generation.
# 3. Iterates over all elements in the DOM, extracting their textual content, XPath, IDs, classes, and other attributes.
# 4. Structures this data into a list of dictionaries, each representing an element.
# 5. Converts this list into a JSON format and writes it to an output file.
# 6. Ensures the output file has the same base name as the input file, handling naming conflicts if they occur.
# 7. Prints the number of tokens in the output JSON file, which can be used to estimate the cost of using the file for LLMs.

# The resulting JSON file can be used by developers to script data extraction from similar webpages, identifying elements by their XPath and content.

import json
import os
from lxml import etree
from lxml import html

# Function to read DOM content from a TXT file
def read_dom_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to parse the DOM content using lxml
def parse_dom(dom_content):
    dom_tree = html.fromstring(dom_content)
    dom_tree = etree.ElementTree(dom_tree)
    return dom_tree

# Function to check if an element's tag is relevant for scraping
def is_relevant_element(tag):
    relevant_tags = {'div', 'span', 'a', 'p', 'ul', 'li', 'button', 'input'}
    return tag in relevant_tags

# Function to trim the text content of an element to a maximum length
def trim_text(text, max_length=100):
    return text[:max_length] + '...' if len(text) > max_length else text

# Function to extract data from all relevant elements in the DOM
def extract_element_data(dom_tree):
    elements_data = []
    for element in dom_tree.iter():
        if isinstance(element, etree._Comment) or not is_relevant_element(element.tag):
            continue
        element_dict = {
            'content': trim_text(''.join(element.itertext()).strip()),
            'id': element.get('id'),
            'class': element.get('class'),
            'attributes': {k: v for k, v in dict(element.attrib).items() if k in {'id', 'class', 'name', 'href'}},
            'xpath': dom_tree.getpath(element)
        }
        elements_data.append(element_dict)
    return elements_data

# Function to write the extracted element data to a JSON file
def write_json_to_file(elements_data, file_path):
    json_output = json.dumps(elements_data, indent=4)
    json_file_path = generate_unique_filename(file_path, 'json')
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_output)
    return json_file_path

# Function to generate a unique filename for the output JSON file
def generate_unique_filename(file_path, extension):
    base_name, _ = os.path.splitext(file_path)
    counter = 1
    new_file_path = f"{base_name}_{counter}.{extension}"

    while os.path.exists(new_file_path):
        counter += 1
        new_file_path = f"{base_name}_{counter}.{extension}"

    return new_file_path

def count_tokens_in_json(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    tokens = content.split()
    return len(tokens)

# Main function to orchestrate the DOM processing and JSON file generation 
def main():
    input_file_path = "dom1.txt"
    dom_content = read_dom_from_file(input_file_path)
    dom_tree = parse_dom(dom_content)
    elements_data = extract_element_data(dom_tree)
    output_json_path = write_json_to_file(elements_data, input_file_path)
    num_tokens = count_tokens_in_json(output_json_path)
    print(f"JSON output saved to: {output_json_path}")
    print(f"Number of tokens in JSON output: {num_tokens}")
    
# Entry point of the script
if __name__ == "__main__":
    main()