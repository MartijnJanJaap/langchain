# filename: generate_angular_app_from_csv.py

import subprocess
import os

def run_command(command):
    """Run a shell command and print its output."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception(f"An error occurred: {error.decode()}")
    print(output.decode())

def setup_angular_environment():
    try:
        # Using shell=True to simulate the same environment as command prompt
        run_command("ng version")
        print("Angular CLI is already installed.")
    except Exception as e:
        print(e)
        raise Exception("Angular CLI is not installed or not found in PATH. Please install it globally with 'npm install -g @angular/cli'.")

def create_angular_project():
    # Initialize a new Angular project
    if not os.path.exists("csv-report-viewer"):
        run_command('npx -p @angular/cli ng new csv-report-viewer --directory ./csv-report-viewer --defaults --skip-git')
    else:
        print("Angular project 'csv-report-viewer' already exists.")

def generate_components():
    os.chdir('./csv-report-viewer')
    run_command('ng generate component components/csv-selector')
    run_command('ng generate component components/data-table')
    run_command('ng generate component components/search-bar')
    run_command('ng generate service services/csv')

def main():
    setup_angular_environment()
    create_angular_project()
    generate_components()

    # Define HTML templates and TypeScript contents for each component
    csv_selector_html = '''
    <label for="fileSelect">Select CSV File:</label>
    <select id="fileSelect" (change)="onFileSelected($event.target.value)">
      <option *ngFor="let file of csvFiles" [value]="file">{{ file }}</option>
    </select>
    '''

    csv_selector_ts = '''
    import { Component } from \'@angular/core\';

    @Component({
      selector: \'app-csv-selector\',
      templateUrl: \'./csv-selector.component.html\',
    })
    export class CsvSelectorComponent {
      csvFiles = [\'file1.csv\', \'file2.csv\']; // Example file names

      onFileSelected(fileName: string) {
        // Action on file select
      }
    }
    '''

    data_table_html = '''
    <table>
      <thead>
        <tr>
          <th *ngFor="let header of headers" (click)="sortTable(header)">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let row of data">
          <td *ngFor="let cell of row">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
    '''

    data_table_ts = '''
    import { Component, Input } from \'@angular/core\';

    @Component({
      selector: \'app-data-table\',
      templateUrl: \'./data-table.component.html\',
    })
    export class DataTableComponent {
      @Input() data: any[] = [];
      headers: string[] = [];

      sortTable(header: string) {
        // Implement sorting logic
      }
    }
    '''

    search_bar_html = '''
    <input type="text" (input)="onSearch($event.target.value)" placeholder="Search...">
    '''

    search_bar_ts = '''
    import { Component, Output, EventEmitter } from \'@angular/core\';

    @Component({
      selector: \'app-search-bar\',
      templateUrl: \'./search-bar.component.html\',
    })
    export class SearchBarComponent {
      @Output() search = new EventEmitter<string>();

      onSearch(value: string) {
        this.search.emit(value);
      }
    }
    '''

    csv_service_ts = '''
    import { Injectable } from \'@angular/core\';
    import { HttpClient } from \'@angular/common/http\';
    import { Observable } from \'rxjs\';

    @Injectable({
      providedIn: \'root\'
    })
    export class CsvService {
      constructor(private http: HttpClient) { }

      fetchCsv(fileName: string): Observable<any> {
        return this.http.get(fileName, { responseType: \'text\' });
      }

      parseCsv(data: string): any[] {
        // Implement CSV parsing logic
        return [];
      }
    }
    '''

    # Create component HTML and TS files
    with open('src/app/components/csv-selector/csv-selector.component.html', 'w') as f:
        f.write(csv_selector_html)
    with open('src/app/components/csv-selector/csv-selector.component.ts', 'w') as f:
        f.write(csv_selector_ts)

    with open('src/app/components/data-table/data-table.component.html', 'w') as f:
        f.write(data_table_html)
    with open('src/app/components/data-table/data-table.component.ts', 'w') as f:
        f.write(data_table_ts)

    with open('src/app/components/search-bar/search-bar.component.html', 'w') as f:
        f.write(search_bar_html)
    with open('src/app/components/search-bar/search-bar.component.ts', 'w') as f:
        f.write(search_bar_ts)

    with open('src/app/services/csv.service.ts', 'w') as f:
        f.write(csv_service_ts)

if __name__ == "__main__":
    main()