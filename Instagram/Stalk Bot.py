from bs4 import BeautifulSoup

def extract_text_from_span_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    span_tags = soup.find_all('span', {'dir': 'auto', 'class':'_ap3a _aaco _aacw _aacx _aad7 _aade'})
    
    extracted_texts = []
    for span in span_tags:
        text = span.get_text(strip=True)  # Get the text content of the span tag
        extracted_texts.append(text)
    
    return extracted_texts

def save_texts_to_file(texts, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for text in texts:
            file.write(text + '\n')

def main():
    # input_file = "Followers.html"  # Replace with the path to your HTML file
    # output_file = "Followers Result.html"  # Output file name

    input_file = "Following.html"  # Replace with the path to your HTML file
    output_file = "Following Result.html"  # Output file name
    
    extracted_texts = extract_text_from_span_tags(input_file)
    save_texts_to_file(extracted_texts, output_file)
    
    print(f"Extracted text saved to '{output_file}'")

if __name__ == "__main__":
    main()
