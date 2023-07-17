import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { DatePipe } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppHeaderComponent } from './components/app-header/app-header.component';
import { FeedbackScreenComponent } from './components/feedback-screen/feedback-screen.component';
import { StudyHeaderComponent } from './components/study-header/study-header.component';
import { MessageLogViewComponent } from './components/message-log-view/message-log-view.component';

@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent,
    FeedbackScreenComponent,
    StudyHeaderComponent,
    MessageLogViewComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
