import { Component } from '@angular/core';
import {DeviceEntity} from "../../model/DeviceEntity";
import {FeedbackService} from "../../service/FeedbackService";

@Component({
  selector: 'feedback-header',
  templateUrl: './feedback-header.component.html',
  styleUrls: ['./feedback-header.component.css']
})
export class FeedbackHeaderComponent {
  devices: DeviceEntity[];

  constructor(private feedbackService: FeedbackService) {
    this.devices = []
  }

  ngOnInit(): void {
    this.init();
  }

  async init(): Promise<void> {
    try {
      this.feedbackService.getDevices().subscribe(
        lst => {
          this.devices = lst;
        }
      )
    } catch (error) {
      console.error('Failed to get devices:', error);
    }
  }

  getDevDesc(): string {
    return this.devices.map(device => device.description).join(', ');
  }
}
