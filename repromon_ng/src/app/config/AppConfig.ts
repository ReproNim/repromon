
export class AppConfig {
  public static API_BASE_URL = 'http://127.0.0.1:9095/api/1';
  public static WS_BASE_URL = 'ws://127.0.0.1:9095/api/1';
  public static TOKEN_URL = 'http://127.0.0.1:9095/token';
  public static DEBUG_ACCESS_TOKEN: string | null = null;
  public static FEEDBACK_INTERVAL_SEC: number = 24*60*60;
}
