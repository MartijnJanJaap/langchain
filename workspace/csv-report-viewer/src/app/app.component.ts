import { Component } from '@angular/core';
import { DataTableComponent } from './components/data-table/data-table.component';

@Component({
  selector: 'app-root',
  imports: [DataTableComponent],
  templateUrl: './app.component.html',
  standalone: true
})
export class AppComponent {
}
