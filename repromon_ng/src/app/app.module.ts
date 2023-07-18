import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
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
    MatButtonModule,
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