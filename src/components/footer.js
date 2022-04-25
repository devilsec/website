import { html } from 'lit';
import { BaseElement } from './bootstrap';

export class Footer extends BaseElement{
  render(){
    return html`
            <footer>
                <div>&copy; DevilSec 2022</div>
            </footer>
        `;
  }
}

customElements.define('main-footer', Footer);
