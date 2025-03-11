# filename: create_angular_code.py

import os

# Define the content for the Angular service
service_content = """
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsvService {
  constructor(private http: HttpClient) { }

  fetchCsv(fileName: string): Observable<any> {
    return this.http.get(fileName, { responseType: 'text' });
  }

  parseCsv(data: string): any[] {
    // Implement CSV parsing logic
    return [];
  }
  
  // New method to fetch available CSV files
  fetchCsvFiles(): Observable<string[]> {
    return this.http.get<string[]>('/api/csv-files');
  }
}
"""

# Define the content for the Angular component
component_ts_content = """
import { Component, OnInit } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { CsvService } from '../../services/csv.service';

@Component({
  selector: 'app-csv-selector',
  standalone: true,
  imports: [MatSelectModule],
  templateUrl: './csv-selector.component.html'
})
export class CsvSelectorComponent implements OnInit {
  csvFiles: string[] = [];

  constructor(private csvService: CsvService) {}

  ngOnInit() {
    this.csvService.fetchCsvFiles().subscribe(files => {
      this.csvFiles = files;
    });
  }

  onCsvFileSelect(fileName: string) {
    console.log(\`Selected file: \${fileName}\`);
    // Perform further actions based on selected file
  }
}
"""

# Define the content for the component's HTML template
component_html_content = """
<mat-form-field appearance="fill">
  <mat-label>Select CSV File</mat-label>
  <mat-select (selectionChange)="onCsvFileSelect($event.value)">
    <mat-option *ngFor="let file of csvFiles" [value]="file">
      {{ file }}
    </mat-option>
  </mat-select>
</mat-form-field>
"""

# Define the filenames and paths
service_file_path = os.path.join('C:\\projects\\portfoliomanager\\workspace\\csv-report-viewer\\src\\app\\services', 'csv.service.ts')
component_ts_file_path = os.path.join('C:\\projects\\portfoliomanager\\workspace\\csv-report-viewer\\src\\app\\components\\csv-selector', 'csv-selector.component.ts')
component_html_file_path = os.path.join('C:\\projects\\portfoliomanager\\workspace\\csv-report-viewer\\src\\app\\components\\csv-selector', 'csv-selector.component.html')

# Ensure the components directory exists
os.makedirs(os.path.dirname(component_ts_file_path), exist_ok=True)

# Write the service content to the file
with open(service_file_path, 'w', encoding='utf-8') as service_file:
    service_file.write(service_content)

# Write the component TypeScript content to the file
with open(component_ts_file_path, 'w', encoding='utf-8') as component_ts_file:
    component_ts_file.write(component_ts_content)

# Write the component HTML content to the file
with open(component_html_file_path, 'w', encoding='utf-8') as component_html_file:
    component_html_file.write(component_html_content)

print("Angular code has been successfully created/updated.")