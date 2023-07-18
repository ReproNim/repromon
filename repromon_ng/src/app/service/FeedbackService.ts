import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AppConfig } from '../config/AppConfig';
import { MessageLogInfoDTO } from '../model/MessageLogInfoDTO';
import { StudyInfoDTO } from '../model/StudyInfoDTO';

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {

  private apiUrl = `${AppConfig.API_BASE_URL}/feedback`;

  constructor(private http: HttpClient) { }

  getMessage(messageId: number): Observable<MessageLogInfoDTO | null> {
    const url = `${this.apiUrl}/get_message?message_id=${messageId}`;
    return this.http.get<MessageLogInfoDTO | null>(url);
  }
  getMessageLog(studyId: number): Observable<MessageLogInfoDTO[]> {
    const url = `${this.apiUrl}/get_message_log?study_id=${studyId}`;
    return this.http.get<MessageLogInfoDTO[]>(url);
  }

  getStudyHeader(studyId: number): Observable<StudyInfoDTO> {
    const url = `${this.apiUrl}/get_study_header?study_id=${studyId}`;
    return this.http.get<StudyInfoDTO>(url);
  }

  setMessageLogVisibility(studyId: number, visible_: boolean, level_: string): Observable<number>  {
    const url = `${this.apiUrl}/set_message_log_visibility?study_id=${studyId}&visible=${visible_}&level=${level_}`;
    return this.http.get<number>(url);
  }
}
