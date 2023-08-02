export interface MessageLogInfoDTO {
  _index?: number; // <-- added in runtime
  id: number;
  study_id: number;
  study: string
  time: string;
  ts: string;
  event_ts: string;
  processing_ts: string;
  category: string;
  status: string;
  level: string;
  device_id: number;
  device: string;
  provider: string;
  description: string;
}
