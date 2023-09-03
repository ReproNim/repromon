import { Injectable } from '@angular/core';
import {AppConfig} from "../config/AppConfig";

@Injectable({
  providedIn: 'root', // singleton
})
export class SecurityManager {

  getToken(): string | null {
    // TODO: use localStorage in addition to DEBUG_ACCESS_TOKEN
    //  localStorage.getItem('access_token');
    return AppConfig.DEBUG_ACCESS_TOKEN
  }
}
