import { Component, Input, OnInit } from '@angular/core';
import { FeedbackService } from '../../service/FeedbackService';

@Component({
  selector: 'study-header',
  templateUrl: './study-header.component.html',
  styleUrls: ['./study-header.component.css']
})
export class StudyHeaderComponent implements OnInit {
  @Input() studyId: number = 0;
  studyHeader: any;

  constructor(private feedbackService: FeedbackService) {
    this.studyHeader = {};
  }

  ngOnInit(): void {
    this.getStudyHeader();
  }

  async getStudyHeader(): Promise<void> {
    try {
      this.studyHeader = await this.feedbackService.getStudyHeader(this.studyId).toPromise();
    } catch (error) {
      console.error('Failed to get study header:', error);
    }
  }
}
