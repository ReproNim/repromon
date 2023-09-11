import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {AppConfig} from "./AppConfig";
import {firstValueFrom} from "rxjs";

@Injectable({
  providedIn: 'root',
})
export class ConfigLoader {
  constructor(private http: HttpClient) {}

  async load(): Promise<void> {
    console.log("load config.json");
    const cfg = await firstValueFrom(this.http.get<any>('config.json'));

    const protocol: string = window.location.protocol;
    const server: string = window.location.hostname;
    const port: string = window.location.port;
    //const appPath: string = window.location.pathname;

    const baseUrlHttp: string = `${protocol}//${server}:${port}`
    console.log(`baseUrlHttp: ${baseUrlHttp}`);
    const baseUrlWs: string = 'ws'+baseUrlHttp.substring(4);
    console.log(`baseUrlWs: ${baseUrlWs}`);

    if( port !== "4200" ) {
      console.log("overload server config")
      for (const key in cfg) {
        if (cfg.hasOwnProperty(key)) {
          if (typeof cfg[key] === 'string') {
            cfg[key] = cfg[key].replace("http://127.0.0.1:9095", baseUrlHttp);
            cfg[key] = cfg[key].replace("ws://127.0.0.1:9095", baseUrlWs);
          }
        }
      }
    }

    AppConfig.initialize(cfg);
    console.log("loaded config.json: "+AppConfig.dump());
  }
}
