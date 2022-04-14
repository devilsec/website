import BaseElement from './bootstrap.js';
import html from 'lit';

export class Footer extends BaseElement{
    render(){
        return html`
            <footer>
                <div>&copy; DevilSec 2022</div>
            </footer>
        `;
    }
}

customElements.define('footer', Footer);
