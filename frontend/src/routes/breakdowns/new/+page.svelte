<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { breakdownAPI, vehicleAPI } from '$lib/utils/api';

	let vehicles = $state([]);
	let loading = $state(false);
	let error = $state('');

	let selectedVehicleId = $state('');
	let category = $state('mechanical');
	let description = $state('');
	let address = $state('');
	let latitude = $state(0);
	let longitude = $state(0);

	onMount(async () => {
		try {
			// Mock vehicles for now
			vehicles = [
				{ id: 1, make: 'Toyota', model: 'Camry', license_plate: 'ABC-123' },
				{ id: 2, make: 'Honda', model: 'Civic', license_plate: 'XYZ-789' }
			];

			// Try to get location
			if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(
					(pos) => {
						latitude = pos.coords.latitude;
						longitude = pos.coords.longitude;
						address = 'Detected Location'; // In real app, reverse geocode here
					},
					(err) => {
						console.error('Location error', err);
					}
				);
			}
		} catch (e) {
			console.error(e);
		}
	});

	async function handleSubmit(event: Event) {
		event.preventDefault();
		if (!selectedVehicleId || !description || !address) {
			error = 'Please fill in all required fields';
			return;
		}

		loading = true;
		error = '';

		try {
			// Mock submission
			// await breakdownAPI.create({ ... });

			// Simulate delay
			await new Promise((r) => setTimeout(r, 1000));

			goto('/breakdowns');
		} catch (e) {
			error = 'Failed to submit breakdown report';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Report Breakdown - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Report a Breakdown</h1>
		<p class="mt-2 text-gray-600">
			Please provide details about your situation so we can send the right help.
		</p>
	</div>

	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		<div class="px-6 py-8 sm:p-10">
			<form class="space-y-8" onsubmit={handleSubmit}>
				{#if error}
					<div
						class="flex items-center rounded-lg border border-red-200 bg-red-50 p-4 text-red-600"
					>
						<i class="fas fa-exclamation-circle mr-3 text-lg"></i>
						{error}
					</div>
				{/if}

				<div class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-6">
					<div class="sm:col-span-6">
						<label for="vehicle" class="mb-1 block text-sm font-medium text-gray-700"
							>Select Vehicle</label
						>
						<div class="relative rounded-md shadow-sm">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<i class="fas fa-car text-gray-400"></i>
							</div>
							<select
								id="vehicle"
								bind:value={selectedVehicleId}
								class="block w-full rounded-lg border-gray-300 py-3 pl-10 text-base focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							>
								<option value="">Select a vehicle</option>
								{#each vehicles as vehicle}
									<option value={vehicle.id}
										>{vehicle.make} {vehicle.model} ({vehicle.license_plate})</option
									>
								{/each}
							</select>
						</div>
					</div>

					<div class="sm:col-span-6">
						<label for="category" class="mb-1 block text-sm font-medium text-gray-700"
							>Problem Category</label
						>
						<div class="relative rounded-md shadow-sm">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<i class="fas fa-tools text-gray-400"></i>
							</div>
							<select
								id="category"
								bind:value={category}
								class="block w-full rounded-lg border-gray-300 py-3 pl-10 text-base focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							>
								<option value="mechanical">Mechanical Issue</option>
								<option value="electrical">Electrical Issue</option>
								<option value="tire">Flat Tire</option>
								<option value="fuel">Out of Fuel</option>
								<option value="accident">Accident</option>
								<option value="other">Other</option>
							</select>
						</div>
					</div>

					<div class="sm:col-span-6">
						<label for="location" class="mb-1 block text-sm font-medium text-gray-700"
							>Location</label
						>
						<div class="mt-1 flex rounded-md shadow-sm">
							<div class="relative flex-grow focus-within:z-10">
								<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
									<i class="fas fa-map-marker-alt text-gray-400"></i>
								</div>
								<input
									type="text"
									id="location"
									bind:value={address}
									class="block w-full rounded-none rounded-l-lg border-gray-300 py-3 pl-10 focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
									placeholder="Enter address or use current location"
								/>
							</div>
							<button
								type="button"
								class="relative -ml-px inline-flex items-center space-x-2 rounded-r-lg border border-gray-300 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							>
								<i class="fas fa-crosshairs text-blue-600"></i>
								<span>Locate Me</span>
							</button>
						</div>
					</div>

					<div class="sm:col-span-6">
						<label for="description" class="mb-1 block text-sm font-medium text-gray-700"
							>Description</label
						>
						<div class="mt-1">
							<textarea
								id="description"
								rows="4"
								bind:value={description}
								class="block w-full rounded-lg border border-gray-300 p-3 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
								placeholder="Describe the issue in detail (e.g., strange noise, smoke, flat tire location)..."
							></textarea>
						</div>
					</div>
				</div>

				<div class="flex justify-end border-t border-gray-100 pt-4">
					<a
						href="/dashboard"
						class="rounded-lg border border-gray-300 bg-white px-6 py-3 text-sm font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
					>
						Cancel
					</a>
					<button
						type="submit"
						disabled={loading}
						class="ml-3 inline-flex justify-center rounded-lg border border-transparent bg-blue-600 px-6 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
					>
						{#if loading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
						{/if}
						Submit Request
					</button>
				</div>
			</form>
		</div>
	</div>
</div>
