import { Component, Inject, Input } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';


@Component({
  selector: 'message-box',
  templateUrl: './message-box.component.html',
  styleUrls: ['./message-box.component.css']
})
export class MessageBoxComponent {
  @Input() title: string = 'Dialog';
  @Input() text: string = '';
  @Input() defaultButton: string = 'ok';
  @Input() buttons: string[] = ['ok'];
  @Input() icon: string | null = null;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {
    if( data ) {
      if( data.title )
        this.title = data.title;
      if( data.text )
        this.text = data.text;
      if( data.buttons )
        this.buttons = data.buttons;
      if( data.icon )
        this.icon = data.icon;
    }
  }
}
