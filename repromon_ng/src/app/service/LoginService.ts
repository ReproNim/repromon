import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import { LoginInfoDTO } from '../model/LoginInfoDTO';
import { AppConfig } from '../config/AppConfig';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private apiUrl = `${AppConfig.API_BASE_URL}/login`;

  constructor(private http: HttpClient) { }

  getCurrentUser(): Observable<LoginInfoDTO> {
    const url = `${this.apiUrl}/get_current_user`;
    return this.http.get<LoginInfoDTO>(url);
  }

  getAccessToken(username: string, password: string): Observable<any> {
    const opts = {
      headers: new HttpHeaders({
        'Content-Type': 'application/x-www-form-urlencoded',
      }),
    };

    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);
    body.set('grant_type', 'password');

    return this.http.post<any>(AppConfig.TOKEN_URL, body.toString(), opts);
  }
}
