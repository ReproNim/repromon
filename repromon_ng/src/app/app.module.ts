import { NgModule, APP_INITIALIZER } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppHeaderComponent } from './components/app-header/app-header.component';
import { FeedbackScreenComponent } from './components/feedback-screen/feedback-screen.component';
import { StudyHeaderComponent } from './components/study-header/study-header.component';
import { MessageLogViewComponent } from './components/message-log-view/message-log-view.component';
import { MessageLogView2Component } from './components/message-log-view2/message-log-view2.component';
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { FeedbackHeaderComponent } from './components/feedback-header/feedback-header.component';
import {AuthInterceptor} from "./security/AuthInterceptor";
import { LoginDialogComponent } from './components/login-dialog/login-dialog.component';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MessageBoxComponent } from './components/message-box/message-box.component';
import {MatDialogModule} from "@angular/material/dialog";
import {MatIconModule} from "@angular/material/icon";
import {MatTooltipModule} from "@angular/material/tooltip";
import {ConfigLoader} from "./config/ConfigLoader";

export function loadConfig(configLoader: ConfigLoader) {
  return () => configLoader.load();
}

@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent,
    FeedbackHeaderComponent,
    FeedbackScreenComponent,
    StudyHeaderComponent,
    MessageLogViewComponent,
    MessageLogView2Component,
    FeedbackHeaderComponent,
    LoginDialogComponent,
    MessageBoxComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    FormsModule,
    HttpClientModule,
    MatDialogModule,
    MatInputModule,
    MatButtonModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSortModule,
    MatTableModule,
    MatTooltipModule,
    NoopAnimationsModule,
    MatIconModule,
  ],
  providers: [
    ConfigLoader,
    {
      provide: APP_INITIALIZER,
      useFactory: loadConfig,
      deps: [ConfigLoader],
      multi: true,
    },
    DatePipe,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true, // Multiple interceptors can be used in the order they are provided
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
