import { Component } from '@angular/core';
import { DataTableComponent } from './components/data-table/data-table.component';

@Component({
  selector: 'app-root',
  imports: [DataTableComponent],
  template: '<app-data-table [data]="data"></app-data-table>',
  standalone: true
})
export class AppComponent {
  data = [
    // Sample data to display in the data table
    { Name: 'Alice', Age: 30, Department: 'Sales' },
    { Name: 'Bob', Age: 25, Department: 'HR' },
    { Name: 'Charlie', Age: 35, Department: 'IT' }
  ];
}
