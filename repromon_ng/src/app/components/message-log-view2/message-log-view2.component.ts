import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { DatePipe } from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
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
  @Input() categoryId: number = 0;
  messageLog: MessageLogInfoDTO[] = [];
  errorCount: number = 0;
  warnCount: number = 0;

  displayedColumns: string[] = ['_index', 'date', 'time', 'level', 'provider', 'study', 'description'];
  dataSource!: MatTableDataSource<MessageLogInfoDTO>;
  selection: any;

  @ViewChild(MatSort, { static:  true }) sort!: MatSort;
  @ViewChild(MatPaginator, { static:  true }) paginator!: MatPaginator;
  @ViewChild('div_dg', { static: true }) div_dg: any;
  @ViewChild('dg', { static: true }) dg: any;


  constructor(
    private datePipe: DatePipe,
    private feedbackService: FeedbackService,
    private pushListenerService: PushListenerService
  ) {
  }

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource<MessageLogInfoDTO>([]);
    this.selection = new SelectionModel<any>(false, []);
    this.pushListenerService.onMessage.subscribe(msg => {
      if (msg.topic === 'feedback-log-refresh' && msg.body.category_id === this.categoryId) {
        this.reload();
      }

      if (msg.topic === 'feedback-log-add' && msg.body.category_id === this.categoryId) {
        this.addMessage(msg.body.message_id);
      }
    });
  }

  ngAfterViewInit(): void {
    if( this.dataSource ) {
      this.dataSource.sort = this.sort;
      this.dataSource.paginator = this.paginator;
      this.dataSource.sortingDataAccessor = (item: any, property) => {
        if (property === 'date' ) {
          return this.formatDate(item.ts);
        } else if (property === 'time' ) {
          return this.formatTime(item.ts);
        } else
          return item[property];
      };
    }
    this.fetchMessageLog();
  }

  ngAfterContentInit(): void {
    this.adjustPageSize();
  }

  ngOnDestroy(): void {
    this.pushListenerService.onMessage.unsubscribe();
  }

  async addMessage(message_id: number): Promise<void> {
    console.log('addMessage(message_id=' + message_id + ')');
    this.feedbackService.getMessage(message_id).subscribe( msg => {
      if( msg ) {
        // find item in sorted array based on event_on timestamp
        let index = this.messageLog.findIndex(
          (item) => new Date(msg.event_on) < new Date(item.event_on)
        );
        console.log("insert index="+index)

        if (index === -1)
          index = this.messageLog.length;

        this.messageLog.splice(index, 0, msg);
        // update _index for message and all subsequent items
        for( let i=index; i<this.messageLog.length; i++)
          this.messageLog[i]._index = i+1;

        this.selectLastItem();
        this.updateCounters();
        // force grid redraw
        this.dataSource._updateChangeSubscription();
        //this.dg.renderRows();
      }
    })
  }

  adjustPageSize():void {
    const elemHeight = this.div_dg.nativeElement.offsetHeight;
    let n: number = 1;
    if( elemHeight>200 ) {
      n = Math.floor((elemHeight-142)/48);
    }
    if (this.paginator.pageSize != n) {
      // console.log("set pageSize=" + n);
      this.paginator.pageSize = n;
      this.paginator._changePageSize(this.paginator.pageSize);
      if( this.selection.hasValue() ) {
        this.selectItem(this.selection.selected[0])
      }
    }
  }

  async clearMessages(mask: string): Promise<void> {
    console.log("clearMessages(mask="+mask+")")
    this.feedbackService.setMessageLogVisibility(this.categoryId, false,
      mask, AppConfig.FEEDBACK_INTERVAL_SEC).subscribe(
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
      this.feedbackService.getMessageLog(null, this.categoryId,
          AppConfig.FEEDBACK_INTERVAL_SEC).subscribe(
        lst => {
          lst.forEach((element, index) => {
            element._index = index + 1;
          });
          this.messageLog = lst;
          this.dataSource.data = this.messageLog;
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

  onDataGridResize(event:any) {
    this.adjustPageSize();
  }

  reload(): void {
    console.log('reload');
    this.fetchMessageLog();
  }

  async resetMessages(): Promise<void> {
    console.log('resetMessages');
    this.feedbackService.setMessageLogVisibility(this.categoryId, true, '*',
      AppConfig.FEEDBACK_INTERVAL_SEC).subscribe(
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

    if( row!=null && this.paginator!=null && this.dataSource!=null ) {
      const idx = this.dataSource.data.indexOf(row);
      const pageSize = this.paginator.pageSize || 1;
      const pageIndex = Math.floor(idx / pageSize);
      this.paginator.pageIndex = pageIndex;
      this.paginator._changePageSize(this.paginator.pageSize);
    }
  }

  private updateCounters(): void {
    this.errorCount = this.messageLog.filter((message) => message.level === 'ERROR').length;
    this.warnCount = this.messageLog.filter((message) => message.level === 'WARN').length;
  }

  protected readonly console = console;
}

