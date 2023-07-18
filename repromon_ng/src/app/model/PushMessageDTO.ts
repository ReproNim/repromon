export interface PushMessageDTO {
  topic: string;
  ts: Date;
  sender: string;
  body: any;
}
