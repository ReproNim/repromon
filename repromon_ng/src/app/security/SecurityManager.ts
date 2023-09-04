import { Injectable } from '@angular/core';
import {AppConfig} from "../config/AppConfig";

@Injectable({
  providedIn: 'root', // singleton
})
export class SecurityManager {

  public hasValidToken(): boolean {
    let token = this.getToken()
    return token!=null && token.length>0;
  }

  public getToken(): string | null {
    let token = localStorage.getItem('access_token')
    if( token === null ) {
      if( AppConfig.DEBUG_ACCESS_TOKEN !=null )
        token = AppConfig.DEBUG_ACCESS_TOKEN
      else
        token = null
      this.setToken(token)
    }
    return token
  }

  public removeToken():void {
    localStorage.removeItem('access_token')
  }

  public setToken(token: string | null):void {
    localStorage.setItem('access_token', token === null?'':token)
  }
}
