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
  getMessageLog(studyId: number | null, categoryId: number | null,
                intervalSec: number | null): Observable<MessageLogInfoDTO[]> {
    let url = `${this.apiUrl}/get_message_log?`;
    let q: string = "";
    if( studyId!==null ) {
      if( q.length>0 )
        q += "&";
      q += `study_id=${studyId}`;
    }
    if( categoryId!==null ) {
      if( q.length>0 )
        q += "&";
      q += `category_id=${categoryId}`;
    }
    if( intervalSec!==null ) {
      if( q.length>0 )
        q += "&";
      q += `interval_sec=${intervalSec}`;
    }
    return this.http.get<MessageLogInfoDTO[]>(url+q);
  }

  getStudyHeader(studyId: number): Observable<StudyInfoDTO> {
    const url = `${this.apiUrl}/get_study_header?study_id=${studyId}`;
    return this.http.get<StudyInfoDTO>(url);
  }

  setMessageLogVisibility(categoryId: number, visible_: boolean, level_: string,
                          intervalSec: number | null): Observable<number>  {
    let url = `${this.apiUrl}/set_message_log_visibility?category_id=${categoryId}&visible=${visible_}&level=${level_}`;
    if( intervalSec!==null )
      url += `&interval_sec=${intervalSec}`;
    return this.http.get<number>(url);
  }
}
