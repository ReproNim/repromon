
export class AppConfig {
  public static API_BASE_URL = 'http://127.0.0.1:9095/api/1';
  public static WS_BASE_URL = 'ws://127.0.0.1:9095/api/1';
  public static CURRENT_USER = undefined;
  //public static DEBUG_ACCESS_TOKEN = undefined;
  public static DEBUG_ACCESS_TOKEN ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." +
    "eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcyNDY1ODk1Mn0." +
    "cIFzfZYL7GHYKcX-8pCgDIPhIhgkEKfwUG3Ay9LYg1E";
  public static FEEDBACK_INTERVAL_SEC: number = 24*60*60;
}
