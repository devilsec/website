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
      }
      .navbar-container {
        margin-left: 25px;
        margin-top: 25px;
        border: 2px solid #ffc267;
        width: 50%;
        background: #000;
        display: flex;
        flex-wrap: wrap;
        text-align: center;
        justify-content: center;
        align-items: center;
      }
      .navbar-heading {
        display: flex;
        flex-wrap: wrap;
      }
      .navbar-pages {
        display: flex;
        flex: 1 1 0;
        height: 75px;
      }
      .navbar-item {
        border: 1px solid #ffc267;
        margin-left: 10px;
      }
      .navbar-page {
        flex: 1 1 0;
        border: 2px solid #5b5b5b;
        text-decoration: none;
        &:hover {
            border: 2px solid #ffc267;
        }
      }
      .navbar-page-link {
        text-decoration: none;
        color: #fff;
      }
      .navbar-logo {
        border: none;
        width: 75px;
      }
      .navbar-title {
        width: 200px;
      }
      `
  ];
  render(){
    return html`
            <div class="header-container">
                <div class="navbar-container">
                    <div class="navbar-heading">
                        <div class="navbar-item navbar-logo">
                            <img src="src/assets/img/DevilSecLogo.png"/>
                        </div>
                        <div class="navbar-item navbar-title">
                            <h2>DevilSec</h2>
                        </div>
                    </div>
                    <div class="navbar-pages">
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                        <div class="navbar-page">
                            <a class="navbar-page-link" href="/schedule">
                                <h3 class="navbar-page-title">Schedule<h3/>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
  }
}

customElements.define('main-header', Header);
