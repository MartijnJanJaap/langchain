# filename: update_data_table_component.py

def update_data_table_component():
    # File path of the Angular component to be updated
    file_path = r"C:\projects\portfoliomanager\workspace\csv-report-viewer\src\app\components\data-table\data-table.component.ts"
    
    # Reading the existing content of the data-table component
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # New content for data-table component with sortTable method
    new_content = [
        "import { Component, Input, OnInit } from '@angular/core';\n",
        "import { CommonModule } from '@angular/common';\n",
        "import { CsvService } from '../../services/csv.service';\n\n",
        "@Component({\n",
        "  selector: 'app-data-table',\n",
        "  standalone: true,\n",
        "  imports: [CommonModule],\n",
        "  templateUrl: './data-table.component.html'\n",
        "})\n",
        "export class DataTableComponent implements OnInit {\n",
        "  @Input() data: any[] = [];\n",
        "  headers: string[] = [];\n",
        "  sortOrder: number = 1; // 1 for ascending, -1 for descending\n\n",
        "  constructor(private csvService: CsvService) {}\n\n",
        "  ngOnInit() {\n",
        "    this.fetchDataFromCsv();\n",
        "  }\n\n",
        "  fetchDataFromCsv() {\n",
        "    this.csvService.fetchCsv('path/to/your/csvfile.csv').subscribe(data => {\n",
        "      this.data = this.csvService.parseCsv(data);\n",
        "      if (this.data.length > 0) {\n",
        "        this.headers = Object.keys(this.data[0]);\n",
        "      }\n",
        "    });\n",
        "  }\n\n",
        "  sortTable(header: string) {\n",
        "    const headerIndex = this.headers.indexOf(header);\n",
        "    if (headerIndex === -1) return;\n\n",
        "    this.data.sort((a, b) => {\n",
        "      const aValue = a[header];\n",
        "      const bValue = b[header];\n\n",
        "      if (aValue < bValue) {\n",
        "        return -1 * this.sortOrder;\n",
        "      }\n",
        "      if (aValue > bValue) {\n",
        "        return 1 * this.sortOrder;\n",
        "      }\n",
        "      return 0;\n",
        "    });\n\n",
        "    this.sortOrder = -this.sortOrder; // Toggle sort order\n",
        "  }\n",
        "}\n"
    ]
    
    # Write back the modified content
    with open(file_path, 'w') as file:
        file.writelines(new_content)

if __name__ == "__main__":
    update_data_table_component()