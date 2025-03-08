
    import { Component, Input } from '@angular/core';

    @Component({
      selector: 'app-data-table',
      templateUrl: './data-table.component.html',
    })
    export class DataTableComponent {
      @Input() data: any[] = [];
      headers: string[] = [];

      sortTable(header: string) {
        // Implement sorting logic
      }
    }
    