<script lang="ts">
	interface ServiceRequest {
		id: number;
		customer: string;
		type: string;
		location: string;
		distance: string;
		urgency: string;
		estimatedPay: number;
		requestedAt: string;
	}

	import { onMount } from 'svelte';
	import { providerStore } from '$lib/stores/dashboard';
	import api from '$lib/utils/api';

	let requests = $derived($providerStore.data?.activeRequests || []);
	let loading = $derived($providerStore.loading);

	onMount(() => {
		providerStore.load();
	});

	function refreshData() {
		providerStore.load(true);
	}

	async function acceptRequest(id: number) {
		if (!confirm('Accept this job?')) return;
		try {
			await api.put(`/assistance/${id}/accept`);
			alert('Job accepted!');
			providerStore.load(true);
		} catch (e) {
			console.error('Failed to accept request:', e);
			alert('Failed to accept job. It may have been taken.');
		}
	}
</script>

<svelte:head>
	<title>Service Requests - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">Nearby Service Requests</h1>
				<p class="mt-2 text-sm text-gray-600">Accept requests from drivers in your area</p>
			</div>
			<button
				onclick={refreshData}
				class="rounded-lg bg-gray-100 px-3 py-2 text-xs font-bold text-gray-600 hover:bg-gray-200"
			>
				<i class="fas fa-sync-alt mr-2"></i>Refresh
			</button>
		</div>
	</div>

	<div class="space-y-4">
		{#each requests as request}
			<div
				class="rounded-xl border-2 border-purple-200 bg-white p-6 shadow-lg transition-all hover:border-purple-400 hover:shadow-xl"
			>
				<div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
					<div class="flex-1">
						<div class="mb-3 flex items-center gap-3">
							<h3 class="text-lg font-bold text-purple-600">
								<i class="fas fa-wrench mr-2"></i>
								{request.type}
							</h3>
							{#if request.urgency === 'high'}
								<span
									class="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-800"
								>
									<i class="fas fa-exclamation-circle mr-1"></i>
									URGENT
								</span>
							{/if}
						</div>
						<div class="grid grid-cols-1 gap-2 md:grid-cols-2">
							<div class="flex items-center text-sm text-gray-600">
								<i class="fas fa-user w-5 text-purple-400"></i>
								<span class="ml-2">{request.customer}</span>
							</div>
							<div class="flex items-center text-sm text-gray-600">
								<i class="fas fa-map-marker-alt w-5 text-purple-400"></i>
								<span class="ml-2">{request.location}</span>
							</div>
							<div class="flex items-center text-sm font-medium text-purple-600">
								<i class="fas fa-location-arrow w-5"></i>
								<span class="ml-2">{request.distance} away</span>
							</div>
							<div class="flex items-center text-sm text-gray-500">
								<i class="fas fa-clock w-5 text-gray-400"></i>
								<span class="ml-2">{request.requestedAt}</span>
							</div>
						</div>
						<div class="mt-3 flex items-center">
							<span class="mr-2 text-sm text-gray-500">Estimated Pay:</span>
							<span class="text-lg font-bold text-green-600">₱{request.estimatedPay}</span>
						</div>
					</div>
					<div class="flex flex-col gap-2 sm:flex-row lg:ml-6">
						<button
							onclick={() => acceptRequest(request.id)}
							class="transform rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:-translate-y-0.5 hover:from-purple-700 hover:to-pink-700"
						>
							<i class="fas fa-check mr-2"></i>
							Accept Job
						</button>
						<button
							class="rounded-lg border-2 border-gray-200 px-6 py-3 text-sm font-medium text-gray-700 transition-all hover:border-purple-500 hover:text-purple-600"
						>
							<i class="fas fa-info-circle mr-2"></i>
							Details
						</button>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
