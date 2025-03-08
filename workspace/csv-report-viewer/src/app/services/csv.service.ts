
    import { Injectable } from '@angular/core';
    import { HttpClient } from '@angular/common/http';
    import { Observable } from 'rxjs';

    @Injectable({
      providedIn: 'root'
    })
    export class CsvService {
      constructor(private http: HttpClient) { }

      fetchCsv(fileName: string): Observable<any> {
        return this.http.get(fileName, { responseType: 'text' });
      }

      parseCsv(data: string): any[] {
        // Implement CSV parsing logic
        return [];
      }
    }
    