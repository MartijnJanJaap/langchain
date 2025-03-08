import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CsvSelectorComponent } from './csv-selector.component';

describe('CsvSelectorComponent', () => {
  let component: CsvSelectorComponent;
  let fixture: ComponentFixture<CsvSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CsvSelectorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CsvSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
