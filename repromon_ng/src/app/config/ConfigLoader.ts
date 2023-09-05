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
    AppConfig.initialize(cfg);
    console.log("loaded config.json: "+AppConfig.dump());
  }
}
