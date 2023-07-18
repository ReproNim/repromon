import { Injectable, EventEmitter } from '@angular/core';
import { AppConfig } from "../config/AppConfig";
import {PushMessageDTO} from "../model/PushMessageDTO";

@Injectable({
  providedIn: 'root'
})
export class PushListenerService {
  private socket?: WebSocket;
  public onMessage: EventEmitter<PushMessageDTO> = new EventEmitter<PushMessageDTO>();

  constructor() {
    this.connect();
  }

  private connect(): void {
    console.log(`"connect() ${AppConfig.WS_BASE_URL}/ws`)
    this.socket = new WebSocket(`${AppConfig.WS_BASE_URL}/ws`);

    this.socket.onmessage = (event) => {
      const msg = JSON.parse(event.data) as PushMessageDTO;
      console.log("msg.topic="+msg.topic)
      this.broadcastMessage(msg);
    };

    this.socket.onopen = (event) => {
      console.log('onopen: ' + event);
    };
  }

  private broadcastMessage(message: PushMessageDTO): void {
    this.onMessage.emit(message);
  }
}
