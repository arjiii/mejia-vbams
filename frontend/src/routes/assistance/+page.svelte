<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';
	import { goto } from '$app/navigation';

	import AddVehicleModal from '$lib/components/vehicles/AddVehicleModal.svelte';
	import Map from '$lib/components/common/Map.svelte';

	let { title = 'Assistance' } = $props();

	let vehicles: any[] = $state([]);
	let nearbyProviders: any[] = $state([]);
	let selectedVehicle = $state('');
	let issueType = $state('');
	let location = $state('');
	let description = $state('');
	let isSubmitting = $state(false);
	let isLoadingProviders = $state(false);
	let error = $state('');
	let showTips = $state(true);
	let showAddModal = $state(false);

	let mapCenter: [number, number] = $state([14.5995, 120.9842]);
	let mapMarkers: any[] = $state([]);

	// Create markers for nearby providers and user location
	$effect(() => {
		const markers = [];
		// User location
		if (location.includes(',')) {
			const parts = location.split(',');
			const lat = parseFloat(parts[0]);
			const lng = parseFloat(parts[1]);
			if (!isNaN(lat) && !isNaN(lng)) {
				markers.push({ lat, lng, title: 'Your Location' });
				mapCenter = [lat, lng];
			}
		}

		// Providers
		nearbyProviders.forEach((p) => {
			// Assuming providers have location data (not in current dummy data? wait, get_nearby_providers does return distance but maybe not exact lat/lng?)
			// ServiceProviderPublicResponse (Step 858) HAS distance but NO lat/lng exposed?
			// It has current_latitude/longitude in ServiceProviderResponse but ServiceProviderPublicResponse?
			// Let's check schemas.py Step 860.
			// ServiceProviderPublicResponse inherits ServiceProviderResponse? No, inherits ServiceProviderResponse.
			// ServiceProviderResponse has current_latitude.
			// So yes, it has lat/lng.
			if (p.current_latitude && p.current_longitude) {
				markers.push({
					lat: p.current_latitude,
					lng: p.current_longitude,
					title: p.business_name || 'Provider'
				});
			}
		});
		mapMarkers = markers;
	});

	function handleMapSelect(lat: number, lng: number) {
		location = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
		fetchNearbyProviders(lat, lng);
	}

	// Troubleshooting Tips Data
	const troubleshootingTips = [
		{
			title: 'Flat Tire',
			icon: 'fa-dharmachakra',
			tips: [
				'Move to a safe area away from traffic.',
				'Turn on your hazard lights.',
				'Apply the parking brake.',
				'If you have a spare and tools, proceed with caution.',
				'Otherwise, wait for assistance inside the vehicle if possible.'
			]
		},
		{
			title: 'Dead Battery',
			icon: 'fa-car-battery',
			tips: [
				'Turn off all lights and electronics.',
				'Check if battery terminals are loose or corroded.',
				'If you have jumper cables and another vehicle, attempt a jump start.',
				'Never smoke near the battery.'
			]
		},
		{
			title: 'Overheating',
			icon: 'fa-thermometer-full',
			tips: [
				'Pull over immediately and turn off the engine.',
				'Do NOT open the radiator cap while hot.',
				'Open the hood to let heat escape.',
				'Wait at least 15-20 minutes before checking coolant levels.'
			]
		}
	];

	const issueTypes = [
		{ label: 'Flat Tire', value: 'tire' },
		{ label: 'Dead Battery', value: 'electrical' },
		{ label: 'Engine Problem', value: 'mechanical' },
		{ label: 'Out of Fuel', value: 'fuel' },
		{ label: 'Accident', value: 'accident' },
		{ label: 'Other', value: 'other' }
	];

	async function loadVehicles() {
		try {
			const res = await api.get('/vehicles/');
			vehicles = res.data;
		} catch (e) {
			console.error('Failed to load vehicles', e);
			error = 'Could not load your vehicles. Please try again.';
		}
	}

	async function fetchNearbyProviders(lat: number, long: number) {
		isLoadingProviders = true;
		try {
			const res = await api.get(`/service-providers/nearby/${lat}/${long}`);
			nearbyProviders = res.data;
		} catch (e) {
			console.error('Failed to load providers', e);
		} finally {
			isLoadingProviders = false;
		}
	}

	onMount(() => {
		loadVehicles();
	});

	function handleVehicleAdded() {
		loadVehicles();
	}

	function getCurrentLocation() {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					const lat = position.coords.latitude;
					const long = position.coords.longitude;
					location = `${lat}, ${long}`;
					fetchNearbyProviders(lat, long);
				},
				(err) => {
					alert('Unable to get your location. Please enter manually.');
				}
			);
		} else {
			alert('Geolocation is not supported by your browser.');
		}
	}

	function handleLocationBlur() {
		if (location.includes(',')) {
			const parts = location.split(',');
			const lat = parseFloat(parts[0]);
			const long = parseFloat(parts[1]);
			if (!isNaN(lat) && !isNaN(long)) {
				fetchNearbyProviders(lat, long);
			}
		}
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		isSubmitting = true;
		error = '';

		try {
			// 1. Create Breakdown Report
			let lat = 0,
				long = 0;
			if (location.includes(',')) {
				const parts = location.split(',');
				lat = parseFloat(parts[0].trim());
				long = parseFloat(parts[1].trim());
			}

			const breakdownData = {
				vehicle_id: parseInt(selectedVehicle),
				latitude: lat,
				longitude: long,
				address: location,
				description: description || issueType,
				category: issueType,
				severity: 'medium'
			};

			const breakdownRes = await api.post('/breakdowns/', breakdownData);
			const breakdownId = breakdownRes.data.id;

			// 2. Create Assistance Request
			let serviceType = 'repair';
			if (issueType === 'tire') serviceType = 'tire_change';
			if (issueType === 'fuel') serviceType = 'fuel_delivery';
			if (issueType === 'electrical') serviceType = 'jump_start';
			if (issueType === 'accident') serviceType = 'towing';

			await api.post('/assistance/', {
				breakdown_id: breakdownId,
				service_type: serviceType,
				latitude: lat,
				longitude: long,
				address: location,
				priority: 'high'
			});

			alert('Assistance request submitted successfully!');
			goto('/dashboard');
		} catch (err: any) {
			console.error('Submission failed', err);
			error = err.response?.data?.detail || 'Failed to submit request. Please try again.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Request Assistance - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:px-8">
	<AddVehicleModal bind:isOpen={showAddModal} onSuccess={handleVehicleAdded} />

	<!-- Header -->
	<div class="mb-8 flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">Request Assistance</h1>
			<p class="mt-2 text-sm text-gray-600">
				Submit a request and we'll connect you with a service provider.
			</p>
		</div>
		<div class="hidden md:block">
			<div class="text-right">
				<p class="text-xs font-bold uppercase tracking-wide text-gray-500">Emergency Hotline</p>
				<a href="tel:911" class="text-2xl font-black text-red-600 hover:text-red-700">911</a>
			</div>
		</div>
	</div>

	<div class="grid gap-8 lg:grid-cols-3">
		<!-- Main Form Column -->
		<div class="space-y-6 lg:col-span-2">
			<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm md:p-8">
				<h2 class="mb-6 border-b pb-4 text-xl font-bold text-gray-900">Breakdown Details</h2>

				{#if error}
					<div class="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
						<i class="fas fa-exclamation-circle mr-2"></i>{error}
					</div>
				{/if}

				{#if vehicles.length === 0}
					<div
						class="flex flex-col items-center rounded-xl border border-dashed border-gray-300 bg-gray-50 p-8 text-center"
					>
						<div class="mb-4 rounded-full bg-blue-100 p-3 text-blue-600">
							<i class="fas fa-car text-2xl"></i>
						</div>
						<h3 class="text-lg font-medium text-gray-900">No Vehicles Found</h3>
						<p class="mb-4 text-sm text-gray-500">
							You need to add a vehicle before you can request assistance.
						</p>
						<button
							onclick={() => (showAddModal = true)}
							class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
						>
							<i class="fas fa-plus mr-2"></i> Add Vehicle
						</button>
					</div>
				{:else}
					<form onsubmit={handleSubmit} class="space-y-6">
						<!-- Vehicle Selection -->
						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Select Vehicle</label>
							<div class="relative">
								<i class="fas fa-car absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
								<select
									bind:value={selectedVehicle}
									required
									class="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
								>
									<option value="" disabled selected>Choose your vehicle...</option>
									{#each vehicles as vehicle}
										<option value={vehicle.id}
											>{vehicle.year}
											{vehicle.make}
											{vehicle.model} ({vehicle.license_plate})</option
										>
									{/each}
								</select>
							</div>
						</div>

						<!-- Issue Type -->
						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Type of Issue</label>
							<div class="grid grid-cols-2 gap-3 md:grid-cols-3">
								{#each issueTypes as type}
									<label
										class={`cursor-pointer rounded-lg border p-3 text-center transition-all hover:bg-gray-50 ${issueType === type.value ? 'border-blue-500 bg-blue-50 text-blue-700 ring-1 ring-blue-500' : 'border-gray-200'}`}
									>
										<input
											type="radio"
											name="issue"
											value={type.value}
											bind:group={issueType}
											class="sr-only"
											required
										/>
										<div class="text-sm font-medium">{type.label}</div>
									</label>
								{/each}
							</div>
						</div>

						<!-- Location -->
						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Location</label>
							<div class="flex gap-2">
								<div class="relative flex-1">
									<i
										class="fas fa-map-marker-alt absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
									></i>
									<input
										type="text"
										bind:value={location}
										onblur={handleLocationBlur}
										placeholder="Enter address or GPS coordinates"
										required
										class="w-full rounded-lg border border-gray-300 py-2.5 pl-10 pr-4 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
									/>
								</div>
								<button
									type="button"
									onclick={getCurrentLocation}
									class="flex items-center justify-center rounded-lg border border-gray-300 bg-white px-3 text-gray-600 hover:bg-gray-50"
									title="Use Current Location"
								>
									<i class="fas fa-crosshairs"></i>
								</button>
							</div>
							<p class="mt-1 text-xs text-gray-500">
								Use GPS icon or tap on the map to set location.
							</p>

							<div class="mt-4 h-64 w-full overflow-hidden rounded-lg border border-gray-300">
								<Map center={mapCenter} markers={mapMarkers} onLocationSelect={handleMapSelect} />
							</div>
						</div>

						<!-- Description -->
						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700"
								>Description (Optional)</label
							>
							<textarea
								bind:value={description}
								rows="3"
								class="w-full rounded-lg border border-gray-300 p-3 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
								placeholder="Any additional details..."
							></textarea>
						</div>

						<div class="pt-4">
							<button
								type="submit"
								disabled={isSubmitting}
								class="w-full rounded-lg bg-blue-600 py-3 text-base font-bold text-white shadow hover:bg-blue-700 disabled:opacity-70"
							>
								{#if isSubmitting}
									<i class="fas fa-spinner fa-spin mr-2"></i> Processing...
								{:else}
									Submit Request
								{/if}
							</button>
						</div>
					</form>
				{/if}
			</div>
		</div>

		<!-- Sidebar - Tips & Safety -->
		<div class="space-y-6">
			<!-- Nearby Providers (Sidebar) -->
			{#if isLoadingProviders}
				<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
					<div class="text-center text-sm text-gray-500">
						<i class="fas fa-spinner fa-spin mr-2"></i> Finding nearby help...
					</div>
				</div>
			{:else if nearbyProviders.length > 0}
				<div class="rounded-xl border border-green-200 bg-green-50 p-5 shadow-sm">
					<h3 class="mb-4 flex items-center text-lg font-bold text-green-900">
						<i class="fas fa-map-marked-alt mr-2"></i> Nearby Providers
					</h3>
					<div class="space-y-3">
						{#each nearbyProviders as provider}
							<div
								class="flex items-center justify-between rounded-lg border border-green-100 bg-white p-3 shadow-sm transition hover:shadow-md"
							>
								<div>
									<div class="text-sm font-bold text-gray-900">
										{provider.business_name || provider.first_name + ' ' + provider.last_name}
									</div>
									<div class="mt-1 text-xs text-gray-500">
										<i class="fas fa-location-arrow mr-1 text-green-600"></i>
										{provider.distance} km
									</div>
								</div>
								<a
									href={`tel:${provider.phone}`}
									class="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-600 transition hover:bg-green-600 hover:text-white"
									title="Call Now"
								>
									<i class="fas fa-phone-alt text-xs"></i>
								</a>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Tips Section -->
			<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
				<h3 class="mb-4 flex items-center text-lg font-bold text-gray-900">
					<i class="fas fa-lightbulb mr-2 text-yellow-500"></i> Helpful Tips
				</h3>
				<div class="space-y-4">
					{#each troubleshootingTips as tip}
						<div class="rounded-lg bg-gray-50 p-3">
							<h4 class="mb-1 flex items-center text-sm font-bold text-gray-800">
								<i class={`fas ${tip.icon} mr-2 text-gray-500`}></i>
								{tip.title}
							</h4>
							<ul class="ml-6 list-disc space-y-1 text-xs text-gray-600">
								{#each tip.tips as t}
									<li>{t}</li>
								{/each}
							</ul>
						</div>
					{/each}
				</div>
			</div>

			<!-- Safety Notice -->
			<div class="rounded-xl border border-yellow-100 bg-yellow-50 p-5">
				<div class="flex items-start">
					<i class="fas fa-shield-alt mr-3 mt-1 text-yellow-600"></i>
					<div>
						<h3 class="text-sm font-bold text-yellow-800">Your Safety Matters</h3>
						<p class="mt-1 text-xs text-yellow-700">
							Stay inside your car if you're on a busy road. Lock doors while waiting for provider.
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
