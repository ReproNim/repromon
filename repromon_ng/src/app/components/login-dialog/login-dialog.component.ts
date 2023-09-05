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

  cancel() {
    this.dialogRef.close(null);
  }

  login() {
    if( this.username.trim().length==0 || this.password.trim().length==0 )
      return;
    this.dialogRef.close( {
        username: this.username,
        password: this.password,
      }
    );
  }

}
