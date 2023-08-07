export interface MessageLogInfoDTO {
  _index?: number; // <-- added in runtime
  id: number;
  study_id: number;
  study: string
  event_on: string;
  registered_on: string;
  recorded_on: string;
  recorded_by: string;
  category: string;
  level: string;
  device_id: number;
  device: string;
  provider: string;
  description: string;
}
