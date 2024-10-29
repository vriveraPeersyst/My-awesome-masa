#!/bin/bash

output_file="all_files_except_json_txt_csv.txt"
> "$output_file"

find . -type f ! -name '*.json' ! -name '*.txt' ! -name '*.csv' ! -path '*/.git/*' -print0 | while IFS= read -r -d '' file; do
    echo "--- File: $file ---" >> "$output_file"
    cat "$file" >> "$output_file"
    echo -e "\n" >> "$output_file"
done