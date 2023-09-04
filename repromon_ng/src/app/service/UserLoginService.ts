import { Injectable, EventEmitter } from '@angular/core';
import {SecurityManager} from "../security/SecurityManager";
import {LoginInfoDTO} from "../model/LoginInfoDTO";
import {PushListenerService} from "./PushListenerService";
import {LoginService} from "./LoginService";
import {AppConfig} from "../config/AppConfig";
import {MessageBoxComponent} from "../components/message-box/message-box.component";
import {MatDialog} from "@angular/material/dialog";
import {LoginDialogComponent} from "../components/login-dialog/login-dialog.component";

@Injectable({
  providedIn: 'root'
})
export class UserLoginService {
  public onCurrentUserChange: EventEmitter<LoginInfoDTO | null> = new EventEmitter<LoginInfoDTO | null>();
  public onLoggedInChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  public currentUser: LoginInfoDTO | null = null;
  public isLoggedIn: boolean = false;

  constructor(
    private dialog: MatDialog,
    private loginService: LoginService,
    private securityManager: SecurityManager,
    private pushListenerService: PushListenerService,
  ) {
    this.updateCurrentUser();
    this.pushListenerService.onConnectedChange.subscribe(isConnected => {
      if (isConnected)
        this.updateCurrentUser();
    });
  }

  public login(username: string, password: string): void {
    this.securityManager.removeToken();

    this.loginService.getAccessToken(username, password).subscribe(
      (data:any) => {
        const token = data["access_token"];
        console.log("login success: "+token);
        this.securityManager.setToken(token);
        location.reload(); // force reload
      },
      (error) => {
        console.log("login error: "+error.error.detail)
        const dialogRef = this.dialog.open(MessageBoxComponent, {
          width: '240pt',
          height: '134pt',
          data: {
            title: 'Login Error Dialog',
            text: error.error.detail,
            buttons: ['ok'],
            icons: ['error']
          },
        });
      }
    );
  }

  loginDialog(): void {
    console.log("loginDialog()")

    const dialogRef = this.dialog.open(LoginDialogComponent, {
      width: '260pt',
      height: '230pt',
    });
    dialogRef.afterClosed().subscribe((res: any) => {
      if (res) {
        console.log("do login: "+res.username)
        this.login(res.username, res.password)
      }
    });
  }


  public logout(): void {
    this.pushListenerService.disconnect()
    this.securityManager.setToken(null)
    this.securityManager.removeToken()
    AppConfig.DEBUG_ACCESS_TOKEN = '';
    this.currentUser = null;
    this.isLoggedIn = false;
    this.onCurrentUserChange.emit(null)
    this.onLoggedInChange.emit(false)
    location.reload(); // force reload
  }

  logoutDialog(): void {
    console.log("logoutDialog()")
    const dialogRef = this.dialog.open(MessageBoxComponent, {
      width: '240pt',
      height: '134pt',
      data: {
        title: 'Logout Dialog',
        text: 'Are you sure you want to log out?',
        buttons: ['yes', 'cancel']
      },
    });

    dialogRef.afterClosed().subscribe((res: string) => {
      if (res && res=='yes') {
        console.log("do logout")
        this.logout()
      }
    });
  }


  private updateCurrentUser(): void {
    this.loginService.getCurrentUser().subscribe(
      (user) => {
        this.currentUser = user;
        this.isLoggedIn = (user && user.is_logged_in);
        console.log('set currentUser=' + JSON.stringify(this.currentUser));
        this.onCurrentUserChange.emit(user)
        this.onLoggedInChange.emit(this.isLoggedIn)
      },
      (error) => {
        console.error('Failed to get current user:', error);
        this.currentUser = null;
        this.isLoggedIn = false;
        this.onCurrentUserChange.emit(null)
        this.onLoggedInChange.emit(false)
      }
    );
  }


}
