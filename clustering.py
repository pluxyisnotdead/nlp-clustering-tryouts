import csv
import os
    
from libgenparser import LibgenParser
    
def clean_row(row):
    cleaned_row = []
    for value in row:
        cleaned_value = value.strip()
        cleaned_row.append(cleaned_value)
    return cleaned_row
        
def clean_title(title):
    cleaned_title = title.translate(str.maketrans("", "", r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
    return cleaned_title.strip()
 
def generate_transformed_tags(tags):
    for tag in tags:
        yield tag
        yield tag.lower()
        yield tag.upper()
def read_tags(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        tags = [tag.strip() for tag in file.readlines()]
 
    return tags

def parse_tags(transformed_tags):
    libgen = LibgenParser()
    for tag in transformed_tags:
        parsed_tag = libgen.search_title(tag)
        for book in parsed_tag:
            title = book.get('Title')
            download_link = book.get('Download_link')
            cleaned_title = clean_title(title)
            yield {"Title": cleaned_title, "Download_link": download_link}
def write_to_csv(file_name):
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=";")
 
        writer.writerow(["Title", "Download_link"])
  
        for book in parsed_books:
            row = [book["Title"], book["Download_link"]]
            writer.writerow(row)
def remove_duplicates(csv_file_path, output_file_path, encoding='utf-8-sig'):
    unique_rows = {}
   
    with open(csv_file_path, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        headers = next(reader)
    
        for row in reader:
            key = tuple(row)
    
            if key not in unique_rows:
               unique_rows[key] = row

    with open(output_file_path, 'w', newline='', encoding=encoding) as file:
        writer = csv.writer(file)
        writer.writerow(headers)
    
        for row in unique_rows.values():
            writer.writerow(row)
    
    os.remove(csv_file_path)

print("Processing...")
tags = read_tags("tags.txt")
print("Tags have been read.")
transformed_tags = generate_transformed_tags(tags)
parsed_books = parse_tags(transformed_tags)
write_to_csv("temp.csv")
remove_duplicates("temp.csv", "parsed_books.csv")
