import { Component, Input, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { AppConfig} from "../../config/AppConfig";
import { FeedbackService } from '../../service/FeedbackService';
import { MessageLogInfoDTO } from "../../model/MessageLogInfoDTO";
import {PushMessageDTO} from "../../model/PushMessageDTO";


@Component({
  selector: 'message-log-view',
  templateUrl: './message-log-view.component.html',
  styleUrls: ['./message-log-view.component.css']
})
export class MessageLogViewComponent implements OnInit {
  @Input() studyId: number = 0;
  messageLog: MessageLogInfoDTO[] = [];
  selectedItemId: any = null;
  errorCount: number = 0;
  warnCount: number = 0;

  constructor(
    private datePipe: DatePipe,
    private feedbackService: FeedbackService
  ) {
  }

  ngOnInit(): void {
    this.fetchMessageLog();
    this.setupWebSocket();
  }

  async setupWebSocket(): Promise<void> {
    const socket = new WebSocket(`${AppConfig.WS_BASE_URL}/ws`);

    socket.onmessage = (event) => {
      console.log('onmessage: data=' + event.data);
      const msg = JSON.parse(event.data) as PushMessageDTO;
      console.log('topic=' + msg.topic);

      if (msg.topic === 'feedback-log-refresh' && msg.body.study_id === this.studyId) {
        this.reload();
      }

      if (msg.topic === 'feedback-log-add' && msg.body.study_id === this.studyId) {
        this.addMessage(msg.body.message_id);
      }
    };

    socket.onopen = function (event) {
      console.log('onopen: ' + event);
    };
  }

  async addMessage(message_id: number): Promise<void> {
    console.log('addMessage(message_id=' + message_id + ')');
    const msg = await this.feedbackService.getMessage(message_id).toPromise();
    this.messageLog.push(msg as MessageLogInfoDTO);
    this.updateCounters();
  }

  async clearMessages(mask: string): Promise<void> {
    console.log("clearMessages(mask="+mask+")")
    this.feedbackService.setMessageLogVisibility(this.studyId, false, mask).subscribe(
      res => {
        console.log("clearMessages res="+res);
        this.reload();
      }
    );
    console.log("clearMessages(...) done")
  }

  async fetchMessageLog(): Promise<void> {
    console.log('fetchMessageLog');
    try {
      this.feedbackService.getMessageLog(this.studyId).subscribe(
        lst => {
          this.messageLog = lst;
          this.updateCounters();
        }
      )
    } catch (error) {
      console.error('Failed to fetch message log:', error);
    }
  }

  formatDate(timestamp: any): string {
    return this.datePipe.transform(timestamp, 'yyyy-MM-dd') as string;
  }

  formatTime(timestamp: any): string {
    return this.datePipe.transform(timestamp, 'HH:mm:ss') as string;
  }

  reload(): void {
    console.log('reload');
    this.fetchMessageLog();
  }

  async resetMessages(): Promise<void> {
    console.log('resetMessages');
    this.feedbackService.setMessageLogVisibility(this.studyId, true, '*').subscribe(
      res => {
        console.log("setMessageLogVisibility res="+res)
        // this.reload();
      }
    );
  }

  selectRow(itemId: any): void {
    this.selectedItemId = itemId;
  }

  private updateCounters(): void {
    this.errorCount = this.messageLog.filter((message) => message.level === 'ERROR').length;
    this.warnCount = this.messageLog.filter((message) => message.level === 'WARN').length;
  }
}

