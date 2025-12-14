<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import 'leaflet/dist/leaflet.css';
	// Dynamic import type
	import type * as Leaflet from 'leaflet';

	// Props
	interface Props {
		center?: [number, number];
		zoom?: number;
		markers?: Array<{
			lat: number;
			lng: number;
			title?: string;
			type?: 'user' | 'provider' | 'breakdown';
		}>;
		interactive?: boolean;
		onLocationSelect?: (lat: number, lng: number) => void;
	}

	let {
		center = [14.5995, 120.9842],
		zoom = 13,
		markers = [],
		interactive = true,
		onLocationSelect
	}: Props = $props();

	let mapElement: HTMLElement;
	let map: Leaflet.Map;
	let markerLayers: Leaflet.Marker[] = [];
	let L: typeof Leaflet; // Module reference

	onMount(async () => {
		if (browser) {
			// Dynamic import
			const module = await import('leaflet');
			L = module.default || module;

			map = L.map(mapElement).setView(center, zoom);

			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; OpenStreetMap contributors'
			}).addTo(map);

			// Handle markers
			updateMarkers();

			// Handle clicks
			if (interactive) {
				map.on('click', (e) => {
					if (onLocationSelect) {
						onLocationSelect(e.latlng.lat, e.latlng.lng);
					}
				});
			}
		}
	});

	// Reactivity
	$effect(() => {
		if (map && center) {
			map.setView(center, zoom);
		}
	});

	$effect(() => {
		if (map && markers) {
			updateMarkers();
		}
	});

	function updateMarkers() {
		if (!map) return;

		markerLayers.forEach((m) => m.remove());
		markerLayers = [];

		markers.forEach((m) => {
			// Customize icon based on type (TODO)
			const marker = L.marker([m.lat, m.lng]).addTo(map);
			if (m.title) marker.bindPopup(m.title);
			markerLayers.push(marker);
		});
	}

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<div
	bind:this={mapElement}
	class="z-0 h-full w-full rounded-lg shadow-inner"
	style="min-height: 300px;"
></div>

<style>
	/* Leaflet needs explicit height sometimes, but handled by min-height above */
</style>
