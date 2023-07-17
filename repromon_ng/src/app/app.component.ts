import { Component, OnInit } from '@angular/core';
import {AppHeaderComponent} from "./components/app-header/app-header.component";
import { LoginService } from './service/LoginService';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'repromon_ng';

  constructor(private loginService: LoginService) { }

  ngOnInit(): void {
    this.loginService.getCurrentUser().subscribe(
      response => {
        // Handle the response from the getCurrentUser method
        console.log(response);
      },
      error => {
        // Handle any errors that occur during the API call
        console.error(error);
      }
    );
  }
}
