# filename: update_data_table_component.py

import os

def update_data_table_component():
    component_ts_file = r'C:\projects\portfoliomanager\workspace\csv-report-viewer\src\app\components\data-table\data-table.component.ts'
    
    new_content = '''
import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
})
export class DataTableComponent implements OnInit {
  @Input() data: any[] = [];
  headers: string[] = [];
  sortOrder: number = 1; // 1 for ascending, -1 for descending
  
  ngOnInit() {
    if (this.data.length > 0) {
      // Initialize headers if data is available
      this.headers = Object.keys(this.data[0]);
    }
  }

  sortTable(header: string) {
    const headerIndex = this.headers.indexOf(header);
    if(headerIndex === -1) return;

    this.data.sort((a, b) => {
      const aValue = a[headerIndex];
      const bValue = b[headerIndex];

      if (aValue < bValue) {
        return -1 * this.sortOrder;
      }
      if (aValue > bValue) {
        return 1 * this.sortOrder;
      }
      
      return 0;
    });

    this.sortOrder = -this.sortOrder; // Toggle sort order
  }
}
'''
    # Writing the new content to the component.ts file
    with open(component_ts_file, 'w') as file:
        file.write(new_content)
    
    print(f"{component_ts_file} has been updated successfully.")

update_data_table_component()