import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'feedback-screen',
  templateUrl: './feedback-screen.component.html',
  styleUrls: ['./feedback-screen.component.css']
})
export class FeedbackScreenComponent implements OnInit {
  @Input() categoryId: number;
  @Input() studyId: number;


  constructor() {
    this.categoryId = 0;
    this.studyId = 0;
  }

  ngOnInit(): void {
    console.log('ngOnInit');
    this.reload();
  }

  async reload(): Promise<void> {
    console.log('reload, categoryId='+this.categoryId);
  }
}
