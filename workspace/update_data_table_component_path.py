# filename: update_data_table_component_path.py

def update_data_table_component_path():
    # File path of the Angular component to be updated
    file_path = r"C:\projects\portfoliomanager\workspace\csv-report-viewer\src\app\components\data-table\data-table.component.ts"

    # Reading the existing content of the data-table component
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # Updated content to replace only the needed parts
    new_content = []
    fetch_data_updated = False

    for line in content:
        if 'this.csvService.fetchCsv' in line and not fetch_data_updated:
            # Update the fetchCsv method with the file path in the assets directory
            new_line = "    this.csvService.fetchCsv('assets/reports/csv/2025-03-08.csv').subscribe(data => {\n"
            new_content.append(new_line)
            fetch_data_updated = True
        else:
            new_content.append(line)

    # Write back the modified content
    with open(file_path, 'w') as file:
        file.writelines(new_content)

if __name__ == "__main__":
    update_data_table_component_path()