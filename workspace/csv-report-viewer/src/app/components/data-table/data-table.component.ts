import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CsvService } from '../../services/csv.service';
import { CsvSelectorComponent } from '../csv-selector/csv-selector.component';
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [CommonModule, CsvSelectorComponent],
  templateUrl: './data-table.component.html'
})
export class DataTableComponent implements OnInit {
  @Input() data: any[] = [];
  headers: string[] = [];
  sortOrder: number = 1; // 1 for ascending, -1 for descending

  constructor(private csvService: CsvService) {}

  csvFileSelected: string = '';

  ngOnInit() {
    this.csvFileSelected = '';
    this.fetchDataFromCsv();
  }

  fetchDataFromCsv() {
    this.csvService.fetchCsv('assets/reports/csv/2025-03-08.csv').subscribe(data => {
      this.data = this.csvService.parseCsv(data);
      if (this.data.length > 0) {
        this.headers = Object.keys(this.data[0]);
      }
    });
  }

  sortTable(header: string) {
    const headerIndex = this.headers.indexOf(header);
    if (headerIndex === -1) return;

    this.data.sort((a, b) => {
      const aValue = a[header];
      const bValue = b[header];

      if (aValue < bValue) {
        return -1 * this.sortOrder;
      }
      if (aValue > bValue) {
        return this.sortOrder;
      }
      return 0;
    });

    this.sortOrder = -this.sortOrder; // Toggle sort order
  }
}

//   updateCsvData(fileName: string) {
//     this.csvService.fetchCsv(\`assets/reports/csv/\${fileName}.csv\`).subscribe(data => {
//       this.data = this.csvService.parseCsv(data);
//       if (this.data.length > 0) {
//         this.headers = Object.keys(this.data[0]);
//       }
//     });
//   }
