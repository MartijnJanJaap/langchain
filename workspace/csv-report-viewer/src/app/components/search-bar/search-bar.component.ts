
    import { Component, Output, EventEmitter } from '@angular/core';

    @Component({
      selector: 'app-search-bar',
      templateUrl: './search-bar.component.html',
    })
    export class SearchBarComponent {
      @Output() search = new EventEmitter<string>();

      onSearch(value: string) {
        this.search.emit(value);
      }
    }
    