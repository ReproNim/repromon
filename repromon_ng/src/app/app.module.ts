import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppHeaderComponent } from './components/app-header/app-header.component';
import { FeedbackScreenComponent } from './components/feedback-screen/feedback-screen.component';
import { StudyHeaderComponent } from './components/study-header/study-header.component';
import { MessageLogViewComponent } from './components/message-log-view/message-log-view.component';
import { MessageLogView2Component } from './components/message-log-view2/message-log-view2.component';
import {NoopAnimationsModule} from "@angular/platform-browser/animations";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";

@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent,
    FeedbackScreenComponent,
    StudyHeaderComponent,
    MessageLogViewComponent,
    MessageLogView2Component
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    HttpClientModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSortModule,
    MatTableModule,
    NoopAnimationsModule
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
