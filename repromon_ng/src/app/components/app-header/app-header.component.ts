import { Component, Input, OnInit} from '@angular/core';
import { DatePipe } from '@angular/common';
import {UserLoginService} from "../../service/UserLoginService";
import {PushListenerService} from "../../service/PushListenerService";
import {MessageBoxComponent} from "../message-box/message-box.component";
import {MatDialog} from "@angular/material/dialog";
import {LoginDialogComponent} from "../login-dialog/login-dialog.component";

@Component({
  selector: 'app-header',
  templateUrl: './app-header.component.html',
  styleUrls: ['./app-header.component.css']
})
export class AppHeaderComponent {
  @Input() screenName: string = '';
  @Input() firstName: string = '';
  @Input() lastName: string = '';
  currentTime: string | null;

  constructor(private datePipe: DatePipe,
              private dialog: MatDialog,
              public pushListenerService: PushListenerService,
              public userLoginService: UserLoginService) {
    this.screenName = '';
    this.currentTime = '';
  }

  ngOnInit(): void {
    console.log("ngOnInit()")
    this.updateTime();
    setInterval(() => this.updateTime(), 1000);
  }

  updateTime(): void {
    const now = new Date();
    this.currentTime = this.datePipe.transform(now, 'yyyy/MM/dd HH:mm:ss');
  }

}
