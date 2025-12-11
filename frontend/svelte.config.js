
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
// SvelteKit expects `adapter` to be an object with an `adapt` method.
// Many adapters export a function (the adapt implementation) directly
// (CommonJS style). If we get a function, wrap it into an object
// with an `adapt` property so the shape matches what SvelteKit validates.
const maybeAdapter =
	typeof adapter === 'function' ? { adapt: adapter } : adapter;

const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: { adapter: maybeAdapter }
};

export default config;
