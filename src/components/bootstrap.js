import {LitElement} from 'lit';
import bootstrap from '../../node_modules/bootstrap/dist/css/bootstrap.css';

/**
 * Base web component class which provides the Bootstrap styles.
 * Imported and used within all web components.
 */
export class BaseElement extends LitElement{
    static styles=bootstrap;
}
