
import { Component, OnInit } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { CsvService } from '../../services/csv.service';
import { Output, EventEmitter } from '@angular/core';
import {NgForOf} from '@angular/common';

@Component({
  selector: 'app-csv-selector',
  standalone: true,
  imports: [MatSelectModule, NgForOf],
  templateUrl: './csv-selector.component.html'
})
export class CsvSelectorComponent implements OnInit {
  csvFiles: string[] = [];

  constructor(private csvService: CsvService) {}

  ngOnInit() {
    console.log("Fetching CSV files...");
    console.log("sadsadad")
    this.csvService.fetchCsvFiles().subscribe(files => {
      console.log('Fetched files:', files);
      this.csvFiles = files;
    });
  }

  @Output() csvFileSelected: EventEmitter<string> = new EventEmitter<string>();

  onCsvFileSelect(fileName: string) {
    this.csvFileSelected.emit(fileName);
  }

}
