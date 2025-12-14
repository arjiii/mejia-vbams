<script lang="ts">
	import api from '$lib/utils/api';
	import { fade, scale } from 'svelte/transition';

	let { isOpen = $bindable(false), onSuccess } = $props();

	let formData = $state({
		make: '',
		model: '',
		year: new Date().getFullYear(),
		license_plate: '',
		vin: '',
		color: '',
		vehicle_type: 'car',
		fuel_type: 'gasoline',
		mileage: 0
	});

	let isSubmitting = $state(false);
	let error = $state('');

	async function handleSubmit(e: Event) {
		e.preventDefault();
		isSubmitting = true;
		error = '';

		try {
			await api.post('/vehicles/', formData);
			isOpen = false;
			if (onSuccess) onSuccess();
			// Reset form
			formData = {
				make: '',
				model: '',
				year: new Date().getFullYear(),
				license_plate: '',
				vin: '',
				color: '',
				vehicle_type: 'car',
				fuel_type: 'gasoline',
				mileage: 0
			};
		} catch (err: any) {
			console.error(err);
			error = err.response?.data?.detail || 'Failed to add vehicle. Please check inputs.';
		} finally {
			isSubmitting = false;
		}
	}

	function close() {
		isOpen = false;
	}
</script>

{#if isOpen}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4"
		transition:fade={{ duration: 200 }}
	>
		<!-- Backdrop -->
		<div
			class="absolute inset-0 bg-black/50 backdrop-blur-sm"
			onclick={close}
			role="button"
			tabindex="0"
			onkeydown={(e) => e.key === 'Escape' && close()}
			aria-label="Close modal"
		></div>

		<!-- Modal -->
		<div
			class="relative w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl"
			transition:scale={{ start: 0.95, duration: 200 }}
		>
			<!-- Header -->
			<div class="border-b border-gray-100 bg-gray-50 px-6 py-4">
				<div class="flex items-center justify-between">
					<h2 class="text-xl font-bold text-gray-900">Add New Vehicle</h2>
					<button
						onclick={close}
						class="rounded-full p-2 text-gray-400 hover:bg-gray-200 hover:text-gray-600"
						aria-label="Close"
					>
						<i class="fas fa-times"></i>
					</button>
				</div>
			</div>

			<!-- Body -->
			<div class="max-h-[80vh] overflow-y-auto p-6">
				{#if error}
					<div class="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-600">
						<i class="fas fa-exclamation-circle mr-2"></i>{error}
					</div>
				{/if}

				<form id="add-vehicle-form" onsubmit={handleSubmit} class="space-y-4">
					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-1">
							<label for="make" class="text-sm font-semibold text-gray-700">Make *</label>
							<input
								id="make"
								type="text"
								bind:value={formData.make}
								placeholder="e.g. Toyota"
								required
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							/>
						</div>
						<div class="space-y-1">
							<label for="model" class="text-sm font-semibold text-gray-700">Model *</label>
							<input
								id="model"
								type="text"
								bind:value={formData.model}
								placeholder="e.g. Camry"
								required
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							/>
						</div>
					</div>

					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-1">
							<label for="year" class="text-sm font-semibold text-gray-700">Year *</label>
							<input
								id="year"
								type="number"
								bind:value={formData.year}
								min="1900"
								max={new Date().getFullYear() + 1}
								required
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							/>
						</div>
						<div class="space-y-1">
							<label for="color" class="text-sm font-semibold text-gray-700">Color *</label>
							<input
								id="color"
								type="text"
								bind:value={formData.color}
								placeholder="e.g. Silver"
								required
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							/>
						</div>
					</div>

					<div class="space-y-1">
						<label for="license_plate" class="text-sm font-semibold text-gray-700"
							>License Plate *</label
						>
						<input
							id="license_plate"
							type="text"
							bind:value={formData.license_plate}
							placeholder="abc-1234"
							required
							class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
						/>
					</div>

					<div class="space-y-1">
						<label for="vin" class="text-sm font-semibold text-gray-700"
							>VIN (Vehicle Identification Number) *</label
						>
						<input
							id="vin"
							type="text"
							bind:value={formData.vin}
							placeholder="17-character VIN"
							required
							minlength="1"
							class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
						/>
						<p class="text-xs text-gray-400">Can be found on dashboard or driver side door.</p>
					</div>

					<div class="grid grid-cols-2 gap-4">
						<div class="space-y-1">
							<label for="vehicle_type" class="text-sm font-semibold text-gray-700">Type</label>
							<select
								id="vehicle_type"
								bind:value={formData.vehicle_type}
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							>
								<option value="car">Car</option>
								<option value="motorcycle">Motorcycle</option>
								<option value="truck">Truck</option>
								<option value="van">Van</option>
								<option value="bus">Bus</option>
							</select>
						</div>
						<div class="space-y-1">
							<label for="fuel_type" class="text-sm font-semibold text-gray-700">Fuel</label>
							<select
								id="fuel_type"
								bind:value={formData.fuel_type}
								class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
							>
								<option value="gasoline">Gasoline</option>
								<option value="diesel">Diesel</option>
								<option value="electric">Electric</option>
								<option value="hybrid">Hybrid</option>
								<option value="lpg">LPG</option>
							</select>
						</div>
					</div>

					<div class="space-y-1">
						<label for="mileage" class="text-sm font-semibold text-gray-700"
							>Current Mileage (km) *</label
						>
						<input
							id="mileage"
							type="number"
							bind:value={formData.mileage}
							min="0"
							required
							class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
						/>
					</div>
				</form>
			</div>

			<!-- Footer -->
			<div class="flex justify-end gap-3 border-t border-gray-100 bg-gray-50 px-6 py-4">
				<button
					onclick={close}
					type="button"
					class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
				>
					Cancel
				</button>
				<button
					type="submit"
					form="add-vehicle-form"
					disabled={isSubmitting}
					class="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-70"
				>
					{#if isSubmitting}
						<i class="fas fa-spinner fa-spin mr-2"></i> Saving...
					{:else}
						Save Vehicle
					{/if}
				</button>
			</div>
		</div>
	</div>
{/if}
