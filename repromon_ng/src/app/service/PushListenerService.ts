import { Injectable, EventEmitter } from '@angular/core';
import { AppConfig } from "../config/AppConfig";
import {PushMessageDTO} from "../model/PushMessageDTO";
import {SecurityManager} from "../security/SecurityManager";

@Injectable({
  providedIn: 'root'
})
export class PushListenerService {
  private socket?: WebSocket;
  public onMessage: EventEmitter<PushMessageDTO> = new EventEmitter<PushMessageDTO>();
  public onConnectedChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  public isConnected: boolean = false;

  constructor(
      private securityManager: SecurityManager,
    ) {
    this.connect();
    // try to reconnect each 1 minute in case of problems
    setInterval(() => {
      if (!this.isConnected)
        this.autoReconnect();
    }, 1*60*1000);
  }

  private autoReconnect(): void {
    console.log("autoReconnect() attempt")
    if( this.securityManager.hasValidToken() )
      this.connect()
    else
      console.log("skip autoReconnect as valid token not found")
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
      if( this.socket ) {
        const token = this.securityManager.getToken()
        if( token ) {
          this.socket.send(token);
          this.isConnected = true;
          this.onConnectedChange.emit(true);
        } else {
          console.log("access token not found, disconnect/close websocket")
          this.socket.close()
        }
      }
    };

    this.socket.onclose = (event) => {
      console.log('onclose: ' + event);
      this.isConnected = false;
      this.onConnectedChange.emit(false);
    };
  }

  public disconnect(): void {
    if( this.isConnected && this.socket )
      this.socket.close()
  }

  private broadcastMessage(message: PushMessageDTO): void {
    this.onMessage.emit(message);
  }
}
