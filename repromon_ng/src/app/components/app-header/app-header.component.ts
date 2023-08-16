import { Component, Input, OnInit} from '@angular/core';
import { DatePipe } from '@angular/common';
import { AppConfig } from '../../config/AppConfig';
import { LoginService } from '../../service/LoginService';
import {PushListenerService} from "../../service/PushListenerService";

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
  currentUser: any;

  constructor(private datePipe: DatePipe,
              private loginService: LoginService,
              public pushListenerService: PushListenerService) {
    this.screenName = '';
    this.currentTime = '';
    this.currentUser = {};
  }

  ngOnInit(): void {
    console.log("ngOnInit()")
    this.updateTime();
    setInterval(() => this.updateTime(), 1000);
    this.getCurrentUser();
    this.pushListenerService.onConnectedChange.subscribe(isConnected => {
      if (isConnected)
        this.getCurrentUser();
    });
  }

  updateTime(): void {
    const now = new Date();
    this.currentTime = this.datePipe.transform(now, 'yyyy/MM/dd HH:mm:ss');
  }

  getCurrentUser(): void {
    this.loginService.getCurrentUser().subscribe(
      (user) => {
        this.currentUser = user;
        AppConfig.CURRENT_USER = this.currentUser;
        console.log('set AppConfig.CURRENT_USER=' + JSON.stringify(AppConfig.CURRENT_USER));
      },
      (error) => {
        console.error('Failed to get current user:', error);
      }
    );
  }

}
