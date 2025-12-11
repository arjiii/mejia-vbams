<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';

	let activeRequests = $state([]);
	let isOnline = $state(false);
	let recentJobs = $state([]);
	let stats = $state({
		completedJobs: 47,
		pendingRequests: 3,
		earnings: 3250.5,
		rating: 4.8,
		responseTime: '8 min'
	});

	onMount(() => {
		// Mock data for service provider
		activeRequests = [
			{
				id: 1,
				customer: 'John Doe',
				type: 'Flat Tire Replacement',
				distance: '2.5 km',
				location: 'M. dela Cruz St., Pasay City',
				status: 'pending',
				urgency: 'high',
				estimatedPay: 450
			},
			{
				id: 2,
				customer: 'Jane Smith',
				type: 'Battery Jump Start',
				distance: '4.1 km',
				location: 'LRT-1 Station, Manila',
				status: 'pending',
				urgency: 'medium',
				estimatedPay: 350
			},
			{
				id: 3,
				customer: 'Mike Johnson',
				type: 'Towing Service',
				distance: '7.3 km',
				location: 'EDSA Ayala, Makati',
				status: 'pending',
				urgency: 'high',
				estimatedPay: 1200
			}
		];

		recentJobs = [
			{
				id: 101,
				customer: 'Sarah Williams',
				type: 'Tire Change',
				completedAt: '2 hours ago',
				earnings: 500,
				rating: 5
			},
			{
				id: 102,
				customer: 'Robert Brown',
				type: 'Battery Service',
				completedAt: '5 hours ago',
				earnings: 400,
				rating: 4
			}
		];
	});

	function toggleStatus() {
		isOnline = !isOnline;
	}

	function acceptJob(requestId: number) {
		console.log('Accepted job:', requestId);
		// In real app, this would call an API
	}
</script>

<div class="space-y-6">
	<!-- Welcome Header -->
	<div class="rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 p-6 text-white shadow-lg">
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-3xl font-bold">Welcome back, {$user?.first_name}!</h1>
				<p class="mt-2 text-purple-100">You have {stats.pendingRequests} pending requests nearby</p>
			</div>
			<div class="hidden md:block">
				<i class="fas fa-tools text-6xl opacity-30"></i>
			</div>
		</div>
	</div>

	<!-- Status Toggle -->
	<div
		class="flex flex-col items-center justify-between rounded-xl border-2 border-purple-100 bg-white p-6 shadow-lg sm:flex-row"
	>
		<div class="mb-4 sm:mb-0">
			<h2 class="text-xl font-bold text-gray-900">Service Status</h2>
			<p class="mt-1 text-sm text-gray-500">Toggle your availability to accept new requests</p>
		</div>
		<div class="flex items-center rounded-lg border border-gray-200 bg-gray-50 px-4 py-3">
			<span class="mr-3 text-sm font-medium text-gray-700">
				Status: <span class={isOnline ? 'font-bold text-green-600' : 'font-bold text-gray-500'}>
					{isOnline ? 'Online & Available' : 'Offline'}
				</span>
			</span>
			<button
				onclick={toggleStatus}
				class={`relative inline-flex h-7 w-14 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 ${isOnline ? 'bg-green-500' : 'bg-gray-300'}`}
			>
				<span
					class={`pointer-events-none inline-block h-6 w-6 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${isOnline ? 'translate-x-7' : 'translate-x-0'}`}
				></span>
			</button>
		</div>
	</div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
		<!-- Completed Jobs -->
		<div
			class="overflow-hidden rounded-xl border border-purple-100 bg-gradient-to-br from-purple-50 to-white shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-xl bg-purple-100 p-3">
						<i class="fas fa-check-circle text-2xl text-purple-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-600">Completed Jobs</dt>
							<dd class="text-3xl font-bold text-gray-900">{stats.completedJobs}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>

		<!-- Total Earnings -->
		<div
			class="overflow-hidden rounded-xl border border-green-100 bg-gradient-to-br from-green-50 to-white shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-xl bg-green-100 p-3">
						<i class="fas fa-dollar-sign text-2xl text-green-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-600">Total Earnings</dt>
							<dd class="text-3xl font-bold text-gray-900">₱{stats.earnings.toFixed(2)}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>

		<!-- Rating -->
		<div
			class="overflow-hidden rounded-xl border border-yellow-100 bg-gradient-to-br from-yellow-50 to-white shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-xl bg-yellow-100 p-3">
						<i class="fas fa-star text-2xl text-yellow-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-600">Rating</dt>
							<dd class="text-3xl font-bold text-gray-900">{stats.rating}/5.0</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>

		<!-- Response Time -->
		<div
			class="overflow-hidden rounded-xl border border-blue-100 bg-gradient-to-br from-blue-50 to-white shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-xl bg-blue-100 p-3">
						<i class="fas fa-clock text-2xl text-blue-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-600">Avg Response</dt>
							<dd class="text-3xl font-bold text-gray-900">{stats.responseTime}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Nearby Requests -->
	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		<div class="border-b border-gray-100 bg-gradient-to-r from-purple-50 to-pink-50 px-6 py-5">
			<div class="flex items-center justify-between">
				<h3 class="text-lg font-bold leading-6 text-gray-900">
					<i class="fas fa-location-arrow mr-2 text-purple-600"></i>
					Nearby Service Requests
				</h3>
				<span
					class="inline-flex items-center rounded-full bg-purple-100 px-3 py-1 text-xs font-medium text-purple-800"
				>
					{activeRequests.length} Available
				</span>
			</div>
		</div>
		<ul class="divide-y divide-gray-200">
			{#each activeRequests as request}
				<li class="p-6 transition-colors duration-150 hover:bg-purple-50">
					<div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
						<div class="min-w-0 flex-1">
							<div class="mb-3 flex items-center justify-between">
								<p class="truncate text-lg font-bold text-purple-600">
									<i class="fas fa-wrench mr-2"></i>
									{request.type}
								</p>
								{#if request.urgency === 'high'}
									<span
										class="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-800"
									>
										<i class="fas fa-exclamation-circle mr-1"></i>
										URGENT
									</span>
								{/if}
							</div>
							<div class="mt-2 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
								<div class="flex items-center text-sm text-gray-600">
									<i class="fas fa-user mr-2 w-5 text-purple-400"></i>
									{request.customer}
								</div>
								<div class="flex items-center text-sm text-gray-600">
									<i class="fas fa-map-marker-alt mr-2 w-5 text-purple-400"></i>
									{request.location}
								</div>
								<div class="flex items-center text-sm font-medium text-purple-600">
									<i class="fas fa-location-arrow mr-2 w-5"></i>
									{request.distance} away
								</div>
							</div>
							<div class="mt-3 flex items-center">
								<span class="mr-2 text-sm text-gray-500">Estimated Pay:</span>
								<span class="text-lg font-bold text-green-600">₱{request.estimatedPay}</span>
							</div>
						</div>
						<div class="flex flex-col gap-2 sm:flex-row lg:ml-6 lg:flex-shrink-0">
							<button
								onclick={() => acceptJob(request.id)}
								class="transform rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:-translate-y-0.5 hover:from-purple-700 hover:to-pink-700 hover:shadow-lg"
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
				</li>
			{/each}
			{#if activeRequests.length === 0}
				<li class="p-12 text-center">
					<div class="mx-auto h-16 w-16 text-gray-300">
						<i class="fas fa-inbox text-6xl"></i>
					</div>
					<h3 class="mt-4 text-lg font-medium text-gray-900">No active requests</h3>
					<p class="mt-2 text-sm text-gray-500">
						Make sure you're online to receive new service requests.
					</p>
				</li>
			{/if}
		</ul>
	</div>

	<!-- Recent Completed Jobs -->
	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		<div class="border-b border-gray-100 bg-gray-50 px-6 py-5">
			<h3 class="text-lg font-bold leading-6 text-gray-900">
				<i class="fas fa-history mr-2 text-gray-600"></i>
				Recent Completed Jobs
			</h3>
		</div>
		<ul class="divide-y divide-gray-200">
			{#each recentJobs as job}
				<li class="p-6">
					<div class="flex items-center justify-between">
						<div>
							<p class="font-bold text-gray-900">{job.type}</p>
							<p class="mt-1 text-sm text-gray-600">Customer: {job.customer}</p>
							<p class="mt-1 text-xs text-gray-500">{job.completedAt}</p>
						</div>
						<div class="text-right">
							<p class="text-lg font-bold text-green-600">₱{job.earnings}</p>
							<div class="mt-1 flex items-center justify-end">
								{#each Array(job.rating) as _, i}
									<i class="fas fa-star text-xs text-yellow-400"></i>
								{/each}
							</div>
						</div>
					</div>
				</li>
			{/each}
		</ul>
	</div>
</div>
