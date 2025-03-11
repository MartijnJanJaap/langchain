
import { Injectable } from '@angular/core';
import { environment } from '../config';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsvService {
  constructor(private http: HttpClient) { }

  private baseUrl: string = environment.apiUrl;

  fetchCsv(fileName: string): Observable<any> {
    return this.http.get(this.baseUrl + "/" + fileName, { responseType: 'text' });
  }

  parseCsv(data: string): any[] {
    // Implement CSV parsing logic
    return [];
  }

  // New method to fetch available CSV files
  fetchCsvFiles(): Observable<string[]> {
    return this.http.get<string[]>(this.baseUrl +'/api/csv-files');
  }
}
