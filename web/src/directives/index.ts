import { App, Directive } from "vue";
import auth from "./modules/auth";
import vClickOutside from "./modules/clickOutside";

const directivesList: { [key: string]: Directive } = {
  auth,
  ["click-outside"]: vClickOutside
};

const directives = {
  install: function (app: App<Element>) {
    Object.keys(directivesList).forEach(key => {
      app.directive(key, directivesList[key]);
    });
  }
};

export default directives;
