#!/bin/bash

output_file="py_md_yaml_files.txt"
> "$output_file"

find . -type f \( -name '*.py' -o -name '*.md' -o -name '*.yaml' \) ! -path '*/.git/*' -print0 | while IFS= read -r -d '' file; do
    echo "--- File: $file ---" >> "$output_file"
    cat "$file" >> "$output_file"
    echo -e "\n" >> "$output_file"
done