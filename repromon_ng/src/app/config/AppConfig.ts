

export class AppConfig {
  public static ENV = 'local'
  public static API_BASE_URL: string = 'http://127.0.0.1:9095/api/1';
  public static WS_BASE_URL: string = 'ws://127.0.0.1:9095/api/1';
  public static TOKEN_URL: string = 'http://127.0.0.1:9095/token';
  public static DEBUG_ACCESS_TOKEN: string | null = null;
  public static FEEDBACK_INTERVAL_SEC: number = 24 * 60 * 60;

  public static initialize(data: any) {
    if (data) {
      if (data.hasOwnProperty("ENV"))
        AppConfig.ENV = data["ENV"];
      if (data.hasOwnProperty("API_BASE_URL"))
        AppConfig.API_BASE_URL = data["API_BASE_URL"];
      if (data.hasOwnProperty("WS_BASE_URL"))
        AppConfig.WS_BASE_URL = data["WS_BASE_URL"];
      if (data.hasOwnProperty("TOKEN_URL"))
        AppConfig.TOKEN_URL = data["TOKEN_URL"];
      if (data.hasOwnProperty("DEBUG_ACCESS_TOKEN"))
        AppConfig.DEBUG_ACCESS_TOKEN = data["DEBUG_ACCESS_TOKEN"];
      if (data.hasOwnProperty("FEEDBACK_INTERVAL_SEC"))
        AppConfig.FEEDBACK_INTERVAL_SEC = data["FEEDBACK_INTERVAL_SEC"];
    }
  }

  public static dump(): string {
    return JSON.stringify({
      'ENV': AppConfig.ENV,
      'API_BASE_URL': AppConfig.API_BASE_URL,
      'WS_BASE_URL': AppConfig.WS_BASE_URL,
      'TOKEN_URL': AppConfig.TOKEN_URL,
      'DEBUG_ACCESS_TOKEN': AppConfig.DEBUG_ACCESS_TOKEN,
      'FEEDBACK_INTERVAL_SEC': AppConfig.FEEDBACK_INTERVAL_SEC,
    });
  }
}
