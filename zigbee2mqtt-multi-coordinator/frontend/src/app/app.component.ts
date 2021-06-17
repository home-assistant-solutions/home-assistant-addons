import { Component } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { DataService } from './services/data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  options: any = {};
  selectedCoordinator = null;
  frontendUrl: any;

  constructor(private dataService: DataService, private sanitizer: DomSanitizer) {
    this.dataService.getOptions().subscribe(options => {
      this.options = options;
    })
  }

  onCoordinatorSelected(coordinator: any) {
    this.frontendUrl = this.sanitizer.bypassSecurityTrustResourceUrl('http://192.168.157.2:8080/zigbee2mqtt-' + coordinator);
    this.selectedCoordinator = coordinator;
  }
}
