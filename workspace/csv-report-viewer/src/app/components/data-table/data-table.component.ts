import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './data-table.component.html'
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
      const aValue = a[header];
      const bValue = b[header];

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
