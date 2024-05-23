import { defaultConfig } from '@formkit/vue';
import { rootClasses } from './formkit.theme';
import { createMultiStepPlugin, createAutoAnimatePlugin } from '@formkit/addons';
import '@formkit/addons/css/multistep';

const config = defaultConfig({
  plugins: [createMultiStepPlugin(), createAutoAnimatePlugin()],
  config: {
    rootClasses,
  },
});

export default config;
