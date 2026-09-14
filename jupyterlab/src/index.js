// https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#theme-plugins
import { IThemeManager } from '@jupyterlab/apputils';

export default {
  id: 'jupyterlab-fmind:plugin',
  description: 'Fmind light theme for JupyterLab and Notebook 7.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (_app, manager) => {
    manager.register({
      name: 'Fmind',
      isLight: true,
      themeScrollbars: false,
      load: () => manager.loadCSS('jupyterlab-fmind/index.css'),
      unload: () => Promise.resolve()
    });
  }
};
