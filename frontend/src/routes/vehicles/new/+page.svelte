<script lang="ts">
	import { goto } from '$app/navigation';
	import { isAuthenticated } from '$lib/stores/auth';
	import { vehicleAPI } from '$lib/utils/api';

	let make = $state('');
	let model = $state('');
	let year = $state(new Date().getFullYear());
	let licensePlate = $state('');
	let vin = $state('');
	let color = $state('');
	let vehicleType = $state('car');
	let fuelType = $state('gasoline');
	let mileage = $state(0);
	let insuranceProvider = $state('');
	let insurancePolicyNumber = $state('');
	let insuranceExpiryDate = $state('');
	let loading = $state(false);
	let error = $state('');

	// Redirect if not authenticated
	if (!$isAuthenticated) {
		goto('/login');
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		if (!make || !model || !licensePlate || !vin || !color) {
			error = 'Please fill in all required fields';
			return;
		}

		loading = true;
		error = '';

		try {
			const vehicleData = {
				make,
				model,
				year,
				license_plate: licensePlate,
				vin,
				color,
				vehicle_type: vehicleType,
				fuel_type: fuelType,
				mileage,
				insurance_provider: insuranceProvider || null,
				insurance_policy_number: insurancePolicyNumber || null,
				insurance_expiry_date: insuranceExpiryDate || null
			};

			await vehicleAPI.create(vehicleData);
			goto('/vehicles');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to add vehicle';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Add Vehicle - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-2xl">
	<div class="space-y-6">
		<!-- Header -->
		<div>
			<h1 class="text-2xl font-bold text-gray-900">Add New Vehicle</h1>
			<p class="mt-1 text-sm text-gray-600">Register a new vehicle to your account</p>
		</div>

		<!-- Form -->
		<form onsubmit={handleSubmit} class="space-y-6">
			{#if error}
				<div class="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-red-600">
					{error}
				</div>
			{/if}

			<!-- Basic Information -->
			<div class="rounded-lg bg-white p-6 shadow">
				<h3 class="mb-4 text-lg font-medium text-gray-900">Basic Information</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
					<div>
						<label for="make" class="block text-sm font-medium text-gray-700">Make *</label>
						<input
							type="text"
							id="make"
							bind:value={make}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="e.g., Toyota"
						/>
					</div>
					<div>
						<label for="model" class="block text-sm font-medium text-gray-700">Model *</label>
						<input
							type="text"
							id="model"
							bind:value={model}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="e.g., Camry"
						/>
					</div>
					<div>
						<label for="year" class="block text-sm font-medium text-gray-700">Year *</label>
						<input
							type="number"
							id="year"
							bind:value={year}
							min="1900"
							max={new Date().getFullYear() + 1}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>
					<div>
						<label for="color" class="block text-sm font-medium text-gray-700">Color *</label>
						<input
							type="text"
							id="color"
							bind:value={color}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="e.g., Silver"
						/>
					</div>
				</div>
			</div>

			<!-- Vehicle Details -->
			<div class="rounded-lg bg-white p-6 shadow">
				<h3 class="mb-4 text-lg font-medium text-gray-900">Vehicle Details</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
					<div>
						<label for="vehicleType" class="block text-sm font-medium text-gray-700"
							>Vehicle Type *</label
						>
						<select
							id="vehicleType"
							bind:value={vehicleType}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						>
							<option value="car">Car</option>
							<option value="truck">Truck</option>
							<option value="motorcycle">Motorcycle</option>
							<option value="bus">Bus</option>
							<option value="van">Van</option>
						</select>
					</div>
					<div>
						<label for="fuelType" class="block text-sm font-medium text-gray-700">Fuel Type *</label
						>
						<select
							id="fuelType"
							bind:value={fuelType}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						>
							<option value="gasoline">Gasoline</option>
							<option value="diesel">Diesel</option>
							<option value="electric">Electric</option>
							<option value="hybrid">Hybrid</option>
							<option value="lpg">LPG</option>
						</select>
					</div>
					<div>
						<label for="mileage" class="block text-sm font-medium text-gray-700">Mileage (km)</label
						>
						<input
							type="number"
							id="mileage"
							bind:value={mileage}
							min="0"
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>
				</div>
			</div>

			<!-- Registration Information -->
			<div class="rounded-lg bg-white p-6 shadow">
				<h3 class="mb-4 text-lg font-medium text-gray-900">Registration Information</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
					<div>
						<label for="licensePlate" class="block text-sm font-medium text-gray-700"
							>License Plate *</label
						>
						<input
							type="text"
							id="licensePlate"
							bind:value={licensePlate}
							required
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="e.g., ABC-123"
						/>
					</div>
					<div>
						<label for="vin" class="block text-sm font-medium text-gray-700">VIN *</label>
						<input
							type="text"
							id="vin"
							bind:value={vin}
							required
							maxlength="17"
							class="mt-1 block w-full rounded-md border-gray-300 font-mono shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="17-character VIN"
						/>
					</div>
				</div>
			</div>

			<!-- Insurance Information (Optional) -->
			<div class="rounded-lg bg-white p-6 shadow">
				<h3 class="mb-4 text-lg font-medium text-gray-900">Insurance Information (Optional)</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
					<div>
						<label for="insuranceProvider" class="block text-sm font-medium text-gray-700"
							>Insurance Provider</label
						>
						<input
							type="text"
							id="insuranceProvider"
							bind:value={insuranceProvider}
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="e.g., State Farm"
						/>
					</div>
					<div>
						<label for="insurancePolicyNumber" class="block text-sm font-medium text-gray-700"
							>Policy Number</label
						>
						<input
							type="text"
							id="insurancePolicyNumber"
							bind:value={insurancePolicyNumber}
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
							placeholder="Policy number"
						/>
					</div>
					<div class="sm:col-span-2">
						<label for="insuranceExpiryDate" class="block text-sm font-medium text-gray-700"
							>Expiry Date</label
						>
						<input
							type="date"
							id="insuranceExpiryDate"
							bind:value={insuranceExpiryDate}
							class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
						/>
					</div>
				</div>
			</div>

			<!-- Submit Button -->
			<div class="flex justify-end space-x-3">
				<a
					href="/vehicles"
					class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
				>
					Cancel
				</a>
				<button
					type="submit"
					disabled={loading}
					class="inline-flex items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
				>
					{#if loading}
						<i class="fas fa-spinner fa-spin mr-2"></i>
					{/if}
					Add Vehicle
				</button>
			</div>
		</form>
	</div>
</div>
