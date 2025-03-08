
    import { Component } from '@angular/core';

    @Component({
      selector: 'app-csv-selector',
      templateUrl: './csv-selector.component.html',
    })
    export class CsvSelectorComponent {
      csvFiles = ['file1.csv', 'file2.csv']; // Example file names

      onFileSelected(fileName: string) {
        // Action on file select
      }
    }
    