# filename: update_ts_files.py

import os

def update_data_table_ts(file_path):
    updated_content = ""
    with open(file_path, 'r') as file:
        content = file.readlines()
        updated_content = "".join(content)

    replace_import = "import { CsvSelectorComponent } from '../csv-selector/csv-selector.component';"
    updated_import = "import { CsvSelectorComponent } from '../csv-selector/csv-selector.component';\nimport { Output, EventEmitter } from '@angular/core';"
    
    replace_on_init = "ngOnInit() {"
    add_csv_listener = "  csvFileSelected: string = '';\n"
    updated_on_init = f"ngOnInit() {{\n    this.csvFileSelected = this.csvService.fetchCsvFiles() || '';\n"

    replace_fetch = "fetchDataFromCsv();"
    updated_fetch = """
  updateCsvData(fileName: string) {
    this.csvService.fetchCsv(\`assets/reports/csv/\${fileName}.csv\`).subscribe(data => {
      this.data = this.csvService.parseCsv(data);
      if (this.data.length > 0) {
        this.headers = Object.keys(this.data[0]);
      }
    });
  }
  """

    if replace_import in updated_content:
        updated_content = updated_content.replace(replace_import, updated_import)
    
    if replace_on_init in updated_content:
        updated_content = updated_content.replace(replace_on_init, f"{add_csv_listener}{updated_on_init}")

    with open(file_path, 'w') as file:
        file.write(updated_content + updated_fetch)

def update_csv_selector_ts(file_path):
    updated_content = ""
    with open(file_path, 'r') as file:
        content = file.readlines()
        updated_content = "".join(content)

    replace_import = "import { CsvService } from '../../services/csv.service';"
    updated_import = "import { CsvService } from '../../services/csv.service';\nimport { Output, EventEmitter } from '@angular/core';"
    
    replace_on_file_select = "// Perform further actions based on selected file"
    updated_on_file_select = """
  @Output() csvFileSelected: EventEmitter<string> = new EventEmitter<string>();

  onCsvFileSelect(fileName: string) {
    this.csvFileSelected.emit(fileName);
  }
    """
    if replace_import in updated_content:
        updated_content = updated_content.replace(replace_import, updated_import)
    
    if replace_on_file_select in updated_content:
        updated_content = updated_content.replace(replace_on_file_select, updated_on_file_select)

    with open(file_path, 'w') as file:
        file.write(updated_content)

# Paths for the files
data_table_ts_path = r"C:\projects\portfoliomanager\workspace\csv-report-viewer\src\app\components\data-table\data-table.component.ts"
csv_selector_ts_path = r"C:\projects\portfoliomanager\workspace\csv-report-viewer\src\app\components\csv-selector\csv-selector.component.ts"

update_data_table_ts(data_table_ts_path)
update_csv_selector_ts(csv_selector_ts_path)

print("TypeScript files successfully updated! Please verify the changes in the Angular application.")