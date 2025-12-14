<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';

	interface Breakdown {
		id: number;
		vehicle: string;
		issue: string;
		location: string;
		date: string;
		status: string;
		provider: string;
		cost: number;
	}

	import { driverStore } from '$lib/stores/dashboard';

	// Derived Stores
	let storeBreakdowns = $derived($driverStore.data?.breakdowns || []);
	let storeVehicles = $derived($driverStore.data?.vehicles || []);
	let loading = $derived($driverStore.loading);
	let filterStatus = $state('all');

	// Join logic - derived automatically when store updates
	let breakdowns = $derived(
		storeBreakdowns.map((b: any) => {
			const vehicle = storeVehicles.find((v: any) => v.id === b.vehicle_id);
			const vehicleName = vehicle
				? `${vehicle.year} ${vehicle.make} ${vehicle.model} (${vehicle.license_plate})`
				: 'Unknown Vehicle';

			return {
				id: b.id,
				vehicle: vehicleName,
				issue: b.category,
				location: b.address || 'Unknown Location',
				date: b.created_at,
				status: b.status || 'reported',
				provider: 'Pending Assignment', // Breakdown model doesn't link provider directly unless joined
				cost: 0 // Breakdown doesn't have cost, AssistanceRequest does.
			};
		})
	);

	onMount(() => {
		driverStore.load();
	});

	function getStatusColor(status: string) {
		const colors: Record<string, string> = {
			completed: 'bg-green-100 text-green-800',
			in_progress: 'bg-blue-100 text-blue-800',
			pending: 'bg-yellow-100 text-yellow-800',
			cancelled: 'bg-red-100 text-red-800'
		};
		return colors[status] || 'bg-gray-100 text-gray-800';
	}

	let filteredBreakdowns = $derived(
		filterStatus === 'all' ? breakdowns : breakdowns.filter((b) => b.status === filterStatus)
	);
</script>

<svelte:head>
	<title>Breakdown History - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">Breakdown History</h1>
			<p class="mt-2 text-sm text-gray-600">View your past assistance requests</p>
		</div>
		<a
			href="/assistance"
			class="rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-blue-700 hover:to-cyan-700"
		>
			<i class="fas fa-exclamation-triangle mr-2"></i>
			Request Assistance
		</a>
	</div>

	<!-- Filter -->
	<div class="rounded-xl border border-gray-200 bg-white p-4 shadow-lg">
		<div class="flex items-center gap-4">
			<label class="text-sm font-medium text-gray-700">Filter by Status:</label>
			<select
				bind:value={filterStatus}
				class="rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
			>
				<option value="all">All Status</option>
				<option value="completed">Completed</option>
				<option value="in_progress">In Progress</option>
				<option value="pending">Pending</option>
				<option value="cancelled">Cancelled</option>
			</select>
		</div>
	</div>

	<!-- Breakdown List -->
	<div class="space-y-4">
		{#each filteredBreakdowns as breakdown}
			<div
				class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg transition-all hover:shadow-xl"
			>
				<div class="mb-4 flex items-start justify-between">
					<div class="flex-1">
						<div class="mb-2 flex items-center gap-3">
							<h3 class="text-lg font-bold text-gray-900">{breakdown.issue}</h3>
							<span
								class={`rounded-full px-3 py-1 text-xs font-medium ${getStatusColor(breakdown.status)}`}
							>
								{breakdown.status.replace('_', ' ').toUpperCase()}
							</span>
						</div>
						<p class="mb-1 text-sm text-gray-600">
							<i class="fas fa-car mr-2 text-gray-400"></i>
							{breakdown.vehicle}
						</p>
					</div>
					<div class="text-right">
						<p class="text-sm text-gray-500">{new Date(breakdown.date).toLocaleDateString()}</p>
						<p class="text-xs text-gray-400">{new Date(breakdown.date).toLocaleTimeString()}</p>
					</div>
				</div>

				<div class="mb-4 grid grid-cols-1 gap-4 md:grid-cols-3">
					<div>
						<p class="mb-1 text-xs text-gray-500">Location</p>
						<p class="text-sm font-medium text-gray-900">
							<i class="fas fa-map-marker-alt mr-1 text-red-500"></i>
							{breakdown.location}
						</p>
					</div>
					<div>
						<p class="mb-1 text-xs text-gray-500">Service Provider</p>
						<p class="text-sm font-medium text-gray-900">
							<i class="fas fa-tools mr-1 text-blue-500"></i>
							{breakdown.provider}
						</p>
					</div>
					<div>
						<p class="mb-1 text-xs text-gray-500">Cost</p>
						<p class="text-sm font-bold text-green-600">
							<i class="fas fa-peso-sign mr-1"></i>
							₱{breakdown.cost}
						</p>
					</div>
				</div>

				<div class="flex gap-2">
					<button
						class="rounded-lg border-2 border-blue-500 px-4 py-2 text-sm font-medium text-blue-600 transition-all hover:bg-blue-50"
					>
						<i class="fas fa-eye mr-1"></i>
						View Details
					</button>
					{#if breakdown.status === 'completed'}
						<button
							class="rounded-lg border-2 border-yellow-500 px-4 py-2 text-sm font-medium text-yellow-600 transition-all hover:bg-yellow-50"
						>
							<i class="fas fa-star mr-1"></i>
							Rate Service
						</button>
					{/if}
				</div>
			</div>
		{/each}

		{#if filteredBreakdowns.length === 0}
			<div class="flex flex-col items-center rounded-xl border border-gray-200 bg-white py-12">
				<i class="fas fa-history mb-4 text-6xl text-gray-300"></i>
				<p class="mb-4 text-gray-500">No breakdown records found</p>
				{#if filterStatus !== 'all'}
					<button
						onclick={() => (filterStatus = 'all')}
						class="font-medium text-blue-600 hover:text-blue-700"
					>
						Clear Filter
					</button>
				{/if}
			</div>
		{/if}
	</div>
</div>
