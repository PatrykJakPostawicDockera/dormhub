import './assets/main.css';
import 'vue-toastification/dist/index.css';
import 'vue-final-modal/style.css';

import { createApp } from 'vue';
import { createVfm } from 'vue-final-modal';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

import type { PluginOptions } from 'vue-toastification';
import Toast, { POSITION } from 'vue-toastification';

import { plugin } from '@formkit/vue';
import config from '../formkit.config';

import App from './App.vue';
import router from './router';

const app = createApp(App);

const toastOptions: PluginOptions = {
  transition: 'Vue-Toastification__bounce',
  maxToasts: 20,
  newestOnTop: true,
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  showCloseButtonOnHover: true,
  icon: true,
};

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const vfm = createVfm();

app.use(pinia);
app.use(router);
app.use(vfm);
app.use(Toast, toastOptions);
app.use(plugin, config);

app.mount('#app');
