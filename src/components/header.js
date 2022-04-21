import { html } from 'lit';
import { BaseElement } from './bootstrap.js';

export class Header extends BaseElement {
  render() {
    return html`
            <div class="sticky">
                <nav class="navbar navbar-inverse">
                    <div class="container-fluid">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        </button>
                        <a href="HomePage.html"></a>
                    </div>
                    <div class="collapse navbar-collapse" id="myNavbar">
                        <ul class="nav navbar-nav">
                            <li class="active"><a href="HomePage.html">Home</a></li>
                            <li><a href="GetConnected.html">Get Connected</a></li>
                            <li><a href="ClubRecordings.html">Club Recordings</a></li>
                            <li><a href="Resources.html">Resources</a></li>
                            <li><a href="DSSchedule.html">Schedule/Calendar</a></li>
                        </ul>
                    </div>
                    </div>
                </nav>
            </div>
        `;
  }
}

customElements.define('main-header', Header);
