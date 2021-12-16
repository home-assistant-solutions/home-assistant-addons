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
  selectedCoordinator: string | null = null;
  frontendUrl: any;

  constructor(private dataService: DataService, private sanitizer: DomSanitizer) {
    this.dataService.getOptions().subscribe(options => {
      this.options = options;
      this.selectCoordinator(options.coordinators[0].name);
    })
  }

  selectCoordinator(coordinator: string) {
    this.frontendUrl = this.sanitizer.bypassSecurityTrustResourceUrl('zigbee2mqtt-' + coordinator);
    this.selectedCoordinator = coordinator;
  }
}
