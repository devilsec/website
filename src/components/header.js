import { html, css } from 'lit';
import { BaseElement } from './bootstrap';

export class Header extends BaseElement{
  static styles = [
    css`
      .header-container {
        margin: 0;
        padding: 0;
        height: 75px;
        margin-bottom: 50px;
        background-color: #262626;
        width: 100%;
        height: 100%;
      }
      .top-nav {
        margin-left: 75px;
        flex-wrap: wrap;
        display: flex;
        font-size: 1.5em;
      }
      .navbar {
        flex-basis: 100%;
        margin-top: 10px;
        padding-top: 20px;
        flex-wrap: wrap;
        display: flex;
        margin-bottom: 10px;
        padding-bottom: 30px;
      }
      .navbar-item {
        font-size: 1.5em;
        margin-left: 75px;
        margin-right: 75px;
      }
      .navbar-link {
        color: #fff !important;
        text-decoration: none;
      }
      .navbar-link:hover {
        border-bottom: 3px solid #ffc627;
      }
      .title {
        margin-bottom: 5px;
        margin-top: 20px;
      }
      .title-link {
        color: #fff !important;
        text-decoration: none;
        border-bottom: 3px solid #8c1d40;
      }
      .devilsec-logo {
      }
      `
  ];
  render(){
    return html`
            <div class="header-container container">
                <div class="row top-nav">
                    <a class="title-link" href="/"><h1 class="col title">DevilSec</h1></a>
                </div>
                <div class="row navbar">
                    <div class="col navbar-item"><a class="navbar-link" href="/schedule.html">Schedule</a></div>
                    <div class="col navbar-item"><a class="navbar-link" href="/resources.html">Resources</a></div>
                    <div class="col navbar-item"><a class="navbar-link" href="/videos.html">Videos</a></div>
                    <div class="col navbar-item"><a class="navbar-link" href="/connect.html">Connect</a></div>
                    <div class="col navbar-item"><a class="navbar-link" href="/about.html">About</a></div>
                </div>
            </div>
        `;
  }
}

customElements.define('main-header', Header);
