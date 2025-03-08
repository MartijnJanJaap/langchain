# filename: generate_angular_app.py

import os
import subprocess

def run_command(command):
    """Run a shell command and print its output."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception(f"An error occurred: {error.decode()}")
    print(output.decode())

def create_angular_project():
    # Initialize a new Angular project using npx
    run_command('npx -p @angular/cli ng new stock-tracker --directory ./stock-tracker --defaults --skip-git')

def generate_angular_components_and_services():
    # Change the working directory to the Angular project
    os.chdir('./stock-tracker')

    # Generate Angular components and service using npx for Angular CLI
    run_command('npx ng generate component csv-selector')
    run_command('npx ng generate component data-table')
    run_command('npx ng generate component search-bar')
    run_command('npx ng generate service csv')

def create_component_files(component_name, template, ts_content):
    # Create the HTML template file
    with open(f'src/app/{component_name}/{component_name}.component.html', 'w') as f:
        f.write(template)

    # Create the TypeScript file
    with open(f'src/app/{component_name}/{component_name}.component.ts', 'w') as f:
        f.write(ts_content)

def create_service_file(ts_content):
    # Create the TypeScript file for the service
    with open('src/app/csv.service.ts', 'w') as f:
        f.write(ts_content)

def main():
    create_angular_project()
    generate_angular_components_and_services()

    # Define templates and TypeScript contents for each component
    csv_selector_template = '''
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

    data_table_template = '''
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

    search_bar_template = '''
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
        // Use a library like PapaParse to convert CSV data to JSON
        return [];
      }
    }
    '''

    # Create the component and service files
    create_component_files('csv-selector', csv_selector_template, csv_selector_ts)
    create_component_files('data-table', data_table_template, data_table_ts)
    create_component_files('search-bar', search_bar_template, search_bar_ts)
    create_service_file(csv_service_ts)

if __name__ == "__main__":
    main()