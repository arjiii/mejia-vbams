<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import api from '$lib/utils/api';

	let vehicleId = $derived($page.params.id);
	let vehicle: any = $state(null);
	let isLoading = $state(true);
	let error = $state('');
	let isEditing = $state(false);
	let isDeleting = $state(false);

	let editForm = $state({
		make: '',
		model: '',
		year: 0,
		license_plate: '',
		vin: '',
		color: '',
		vehicle_type: '',
		fuel_type: '',
		mileage: 0,
		insurance_provider: '',
		insurance_policy_number: '',
		insurance_expiry_date: '',
		iot_device_id: ''
	});

	onMount(async () => {
		await loadVehicle();
	});

	async function loadVehicle() {
		isLoading = true;
		try {
			const res = await api.get(`/vehicles/${vehicleId}`);
			vehicle = res.data;
			editForm = { ...vehicle };
		} catch (e: any) {
			error = e.response?.data?.detail || 'Failed to load vehicle';
		} finally {
			isLoading = false;
		}
	}

	async function handleUpdate() {
		try {
			await api.put(`/vehicles/${vehicleId}`, editForm);
			alert('Vehicle updated successfully!');
			isEditing = false;
			await loadVehicle();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to update vehicle');
		}
	}

	async function handleDelete() {
		if (!confirm('Are you sure you want to delete this vehicle? This action cannot be undone.'))
			return;

		isDeleting = true;
		try {
			await api.delete(`/vehicles/${vehicleId}`);
			alert('Vehicle deleted successfully!');
			goto('/vehicles');
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to delete vehicle');
			isDeleting = false;
		}
	}
</script>

<svelte:head>
	<title>Vehicle Details - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8">
	<div class="mb-6 flex items-center justify-between">
		<div>
			<button
				onclick={() => goto('/vehicles')}
				class="mb-2 flex items-center text-sm text-gray-600 hover:text-gray-900"
			>
				<i class="fas fa-arrow-left mr-2"></i> Back to My Vehicles
			</button>
			<h1 class="text-3xl font-bold text-gray-900">Vehicle Details</h1>
		</div>

		{#if vehicle && !isEditing}
			<div class="flex gap-2">
				<button
					onclick={() => (isEditing = true)}
					class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
				>
					<i class="fas fa-edit mr-2"></i>Edit
				</button>
				<button
					onclick={handleDelete}
					disabled={isDeleting}
					class="rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700 disabled:opacity-50"
				>
					<i class="fas fa-trash mr-2"></i>
					{isDeleting ? 'Deleting...' : 'Delete'}
				</button>
			</div>
		{/if}
	</div>

	{#if isLoading}
		<div class="text-center">
			<i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
			<p class="mt-4 text-gray-600">Loading vehicle details...</p>
		</div>
	{:else if error}
		<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
			<i class="fas fa-exclamation-circle mr-2"></i>{error}
		</div>
	{:else if vehicle}
		{#if isEditing}
			<!-- Edit Form -->
			<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-bold">Edit Vehicle</h2>

				<div class="grid gap-4 md:grid-cols-2">
					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Make</label>
						<input
							type="text"
							bind:value={editForm.make}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Model</label>
						<input
							type="text"
							bind:value={editForm.model}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Year</label>
						<input
							type="number"
							bind:value={editForm.year}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">License Plate</label>
						<input
							type="text"
							bind:value={editForm.license_plate}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">VIN</label>
						<input
							type="text"
							bind:value={editForm.vin}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Color</label>
						<input
							type="text"
							bind:value={editForm.color}
							class="w-full rounded-lg border border-gray-300 p-2.5"
							required
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Vehicle Type</label>
						<select
							bind:value={editForm.vehicle_type}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						>
							<option value="car">Car</option>
							<option value="truck">Truck</option>
							<option value="motorcycle">Motorcycle</option>
							<option value="bus">Bus</option>
							<option value="van">Van</option>
						</select>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Fuel Type</label>
						<select
							bind:value={editForm.fuel_type}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						>
							<option value="gasoline">Gasoline</option>
							<option value="diesel">Diesel</option>
							<option value="electric">Electric</option>
							<option value="hybrid">Hybrid</option>
							<option value="lpg">LPG</option>
						</select>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Mileage (km)</label>
						<input
							type="number"
							bind:value={editForm.mileage}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Insurance Provider</label>
						<input
							type="text"
							bind:value={editForm.insurance_provider}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700"
							>Insurance Policy Number</label
						>
						<input
							type="text"
							bind:value={editForm.insurance_policy_number}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						/>
					</div>

					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700"
							>Insurance Expiry Date</label
						>
						<input
							type="date"
							bind:value={editForm.insurance_expiry_date}
							class="w-full rounded-lg border border-gray-300 p-2.5"
						/>
					</div>
				</div>

				<div class="mt-6 flex gap-2">
					<button
						onclick={handleUpdate}
						class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
					>
						Save Changes
					</button>
					<button
						onclick={() => (isEditing = false)}
						class="rounded-lg border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50"
					>
						Cancel
					</button>
				</div>
			</div>
		{:else}
			<!-- View Mode -->
			<div class="grid gap-6 lg:grid-cols-3">
				<div class="space-y-6 lg:col-span-2">
					<!-- Main Info Card -->
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<div class="mb-4 flex items-start justify-between">
							<div>
								<h2 class="text-2xl font-bold text-gray-900">
									{vehicle.year}
									{vehicle.make}
									{vehicle.model}
								</h2>
								<p class="mt-1 text-lg font-medium text-gray-600">{vehicle.license_plate}</p>
							</div>
							<div
								class={`rounded-full px-4 py-2 text-sm font-medium ${vehicle.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}
							>
								{vehicle.is_active ? 'Active' : 'Inactive'}
							</div>
						</div>

						<div class="grid gap-4 md:grid-cols-2">
							<div>
								<p class="text-sm text-gray-600">VIN</p>
								<p class="font-medium text-gray-900">{vehicle.vin}</p>
							</div>
							<div>
								<p class="text-sm text-gray-600">Color</p>
								<p class="font-medium text-gray-900">{vehicle.color}</p>
							</div>
							<div>
								<p class="text-sm text-gray-600">Vehicle Type</p>
								<p class="font-medium text-gray-900">{vehicle.vehicle_type.toUpperCase()}</p>
							</div>
							<div>
								<p class="text-sm text-gray-600">Fuel Type</p>
								<p class="font-medium text-gray-900">{vehicle.fuel_type.toUpperCase()}</p>
							</div>
							<div>
								<p class="text-sm text-gray-600">Mileage</p>
								<p class="font-medium text-gray-900">{vehicle.mileage.toLocaleString()} km</p>
							</div>
						</div>
					</div>

					<!-- Insurance Info -->
					{#if vehicle.insurance_provider}
						<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
							<h3 class="mb-4 text-lg font-bold text-gray-900">Insurance Information</h3>
							<div class="space-y-3">
								<div>
									<p class="text-sm text-gray-600">Provider</p>
									<p class="font-medium text-gray-900">{vehicle.insurance_provider}</p>
								</div>
								{#if vehicle.insurance_policy_number}
									<div>
										<p class="text-sm text-gray-600">Policy Number</p>
										<p class="font-medium text-gray-900">{vehicle.insurance_policy_number}</p>
									</div>
								{/if}
								{#if vehicle.insurance_expiry_date}
									<div>
										<p class="text-sm text-gray-600">Expiry Date</p>
										<p class="font-medium text-gray-900">
											{new Date(vehicle.insurance_expiry_date).toLocaleDateString()}
										</p>
									</div>
								{/if}
							</div>
						</div>
					{/if}
				</div>

				<!-- Sidebar -->
				<div class="space-y-6">
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<h3 class="mb-4 text-lg font-bold text-gray-900">Quick Info</h3>
						<div class="space-y-3 text-sm">
							<div>
								<p class="text-gray-600">Vehicle ID</p>
								<p class="font-medium text-gray-900">#{vehicle.id}</p>
							</div>
							<div>
								<p class="text-gray-600">Owner ID</p>
								<p class="font-medium text-gray-900">#{vehicle.owner_id}</p>
							</div>
							{#if vehicle.iot_device_id}
								<div>
									<p class="text-gray-600">IoT Device</p>
									<p class="font-medium text-gray-900">{vehicle.iot_device_id}</p>
								</div>
							{/if}
						</div>
					</div>

					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<h3 class="mb-4 text-lg font-bold text-gray-900">Service History</h3>
						<div class="space-y-3 text-sm">
							<div>
								<p class="text-gray-600">Last Service</p>
								<p class="font-medium text-gray-900">
									{new Date(vehicle.last_service_date).toLocaleDateString()}
								</p>
							</div>
							{#if vehicle.next_service_due}
								<div>
									<p class="text-gray-600">Next Service Due</p>
									<p class="font-medium text-orange-600">
										{new Date(vehicle.next_service_due).toLocaleDateString()}
									</p>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</div>
		{/if}
	{/if}
</div>
