import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { DatePipe } from '@angular/common';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { AppConfig} from "../../config/AppConfig";
import { FeedbackService } from '../../service/FeedbackService';
import { MessageLogInfoDTO } from "../../model/MessageLogInfoDTO";
import {PushMessageDTO} from "../../model/PushMessageDTO";
import {PushListenerService} from "../../service/PushListenerService";
import {SelectionModel} from "@angular/cdk/collections";


@Component({
  selector: 'message-log-view2',
  templateUrl: './message-log-view2.component.html',
  styleUrls: ['./message-log-view2.component.css']
})
export class MessageLogView2Component implements OnInit {
  @Input() studyId: number = 0;
  messageLog: MessageLogInfoDTO[] = [];
  errorCount: number = 0;
  warnCount: number = 0;

  displayedColumns: string[] = ['index', 'date', 'time', 'level', 'provider', 'description'];
  dataSource: MatTableDataSource<MessageLogInfoDTO> | null = null;
  selection: any;

  @ViewChild(MatSort) sort: MatSort | null = null;
  @ViewChild(MatPaginator) paginator: MatPaginator | null = null;
  @ViewChild('dg', { static: true }) dg: any;


  constructor(
    private datePipe: DatePipe,
    private feedbackService: FeedbackService,
    private pushListenerService: PushListenerService
  ) {
  }

  ngOnInit(): void {
    this.selection = new SelectionModel<any>(false, []);
    this.pushListenerService.onMessage.subscribe(msg => {
      if (msg.topic === 'feedback-log-refresh' && msg.body.study_id === this.studyId) {
        this.reload();
      }

      if (msg.topic === 'feedback-log-add' && msg.body.study_id === this.studyId) {
        this.addMessage(msg.body.message_id);
      }
    });
    this.fetchMessageLog();
  }

  ngOnDestroy(): void {
    this.pushListenerService.onMessage.unsubscribe();
  }

  async addMessage(message_id: number): Promise<void> {
    console.log('addMessage(message_id=' + message_id + ')');
    this.feedbackService.getMessage(message_id).subscribe( msg => {
      this.messageLog.push(msg as MessageLogInfoDTO);
      this.selectLastItem();
      this.updateCounters();
      // force grid redraw
      this.dg.renderRows();
    })
  }

  async clearMessages(mask: string): Promise<void> {
    console.log("clearMessages(mask="+mask+")")
    this.feedbackService.setMessageLogVisibility(this.studyId, false, mask).subscribe(
      res => {
        console.log("clearMessages res="+res);
        //this.reload();
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
          this.dataSource = new MatTableDataSource<MessageLogInfoDTO>(this.messageLog);
          this.dataSource.sort = this.sort;
          this.dataSource.paginator = this.paginator;
          this.selectLastItem();
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

  selectLastItem(): void {
    if( this.messageLog.length>0 )
      this.selectItem(this.messageLog[this.messageLog.length-1])
  }

  selectItem(row: MessageLogInfoDTO): void {
    console.log("selectItem: "+row.id)
    this.selection.select(row);
  }

  private updateCounters(): void {
    this.errorCount = this.messageLog.filter((message) => message.level === 'ERROR').length;
    this.warnCount = this.messageLog.filter((message) => message.level === 'WARN').length;
  }

  protected readonly console = console;
}

