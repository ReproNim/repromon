import { Injectable, EventEmitter } from '@angular/core';
import { AppConfig } from "../config/AppConfig";
import {PushMessageDTO} from "../model/PushMessageDTO";

@Injectable({
  providedIn: 'root'
})
export class PushListenerService {
  private socket?: WebSocket;
  public onMessage: EventEmitter<PushMessageDTO> = new EventEmitter<PushMessageDTO>();
  public onConnectedChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  public isConnected: boolean = false;

  constructor() {
    this.connect();
    // try to reconnect each 1 minute in case of problems
    setInterval(() => {
      if (!this.isConnected)
        this.autoReconnect();
    }, 1*60*1000);
  }

  private autoReconnect(): void {
    console.log("autoReconnect() attempt")
    this.connect()
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
      this.isConnected = true;
      this.onConnectedChange.emit(true);
    };

    this.socket.onclose = (event) => {
      console.log('onclose: ' + event);
      this.isConnected = false;
      this.onConnectedChange.emit(false);
    };
  }

  private broadcastMessage(message: PushMessageDTO): void {
    this.onMessage.emit(message);
  }
}
