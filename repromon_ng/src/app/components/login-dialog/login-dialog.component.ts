import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.css']
})
export class LoginDialogComponent {
  username: string = '';
  password: string = '';

  constructor(public dialogRef: MatDialogRef<LoginDialogComponent>) {}
  login() {
    // TODO:
    this.dialogRef.close();
  }
}
