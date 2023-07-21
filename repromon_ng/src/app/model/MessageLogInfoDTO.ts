export interface MessageLogInfoDTO {
  _index?: number; // <-- added in runtime
  id: number;
  study_id: number;
  time: string;
  ts: string;
  category: string;
  status: string;
  level: string;
  provider: string;
  description: string;
}
