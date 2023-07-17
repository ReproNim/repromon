import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
}
