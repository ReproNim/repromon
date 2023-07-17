import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'feedback-screen',
  templateUrl: './feedback-screen.component.html',
  styleUrls: ['./feedback-screen.component.css']
})
export class FeedbackScreenComponent implements OnInit {
  @Input() studyId: number;

  constructor() {
    this.studyId = 0;
  }

  ngOnInit(): void {
    console.log('ngOnInit');
    this.reload();
  }

  async reload(): Promise<void> {
    console.log('reload, studyId='+this.studyId);
  }
}
