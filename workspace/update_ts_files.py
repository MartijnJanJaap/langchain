# filename: update_ts_files.py

def update_csv_selector_ts_file():
    # Path to the `csv-selector.component.ts` file
    file_path = "C:\\projects\\portfoliomanager\\workspace\\csv-report-viewer\\src\\app\\components\\csv-selector\\csv-selector.component.ts"
    
    # Read the original file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # New content with additional console logs
    new_content = []
    for line in lines:
        if "ngOnInit()" in line:  # After ngOnInit definition, add console logs to verify data
            new_content.append(line)
            new_content.append('    console.log("Fetching CSV files...");\n')
        elif "this.csvFiles = files;" in line:  # Add logs to check if files are being fetched
            new_content.append("      console.log('Fetched files:', files);\n")
            new_content.append(line)
        else:
            new_content.append(line)

    # Write back the updated file
    with open(file_path, 'w') as file:
        file.writelines(new_content)
    
    print("Updated csv-selector.component.ts with additional logging to debug data loading.")

update_csv_selector_ts_file()