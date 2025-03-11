
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
    // Perform further actions based on selected file
  }
}
