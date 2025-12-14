<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';
	import api from '$lib/utils/api';

	import { providerStore } from '$lib/stores/dashboard';
	import StatsCard from '$lib/components/common/StatsCard.svelte';

	let activeRequests = $derived($providerStore.data?.activeRequests || []);
	let recentJobs = $derived($providerStore.data?.recentJobs || []);
	let stats = $derived(
		$providerStore.data
			? {
					completedJobs: $providerStore.data.completedJobs,
					pendingRequests: $providerStore.data.pendingRequests,
					earnings: $providerStore.data.earnings,
					rating: 0, // Mock rating or from backend if added to schema
					responseTime: 'N/A'
				}
			: {
					completedJobs: 0,
					pendingRequests: 0,
					earnings: 0,
					rating: 0,
					responseTime: 'N/A'
				}
	);

	let loading = $derived($providerStore.loading);
	let isOnline = $state(true); // Keeping online status local for now as it's toggle-able instant interaction

	let applicationData = $state({
		business_name: '',
		business_license: '',
		base_rate: 500,
		documents: [] as string[]
	});

	let uploadStatus = $state('');
	async function handleFileUpload(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files || input.files.length === 0) return;

		uploadStatus = 'Uploading...';
		const formData = new FormData();
		for (let i = 0; i < input.files.length; i++) {
			formData.append('files', input.files[i]);
		}

		try {
			// Using fetch directly as api wrapper might need update for FormData
			const token = localStorage.getItem('token');
			const res = await fetch('http://localhost:8000/api/upload/', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`
				},
				body: formData
			});

			if (!res.ok) throw new Error('Upload failed');
			const data = await res.json();

			// Append new urls
			applicationData.documents = [...applicationData.documents, ...data.urls];
			uploadStatus = 'Upload complete';
		} catch (e) {
			console.error(e);
			uploadStatus = 'Upload failed';
		}
	}

	onMount(async () => {
		if ($user?.is_verified) {
			providerStore.load();
		}
	});

	async function submitApplication() {
		try {
			await api.put('/service-providers/profile', applicationData);
			alert('Application submitted successfully! Please wait for admin verification.');
		} catch (e) {
			console.error('Failed to submit application', e);
			alert('Failed to submit application.');
		}
	}

	function toggleStatus() {
		// Toggle via API
		isOnline = !isOnline;
		api
			.put('/service-providers/online-status', { is_online: isOnline })
			.catch((e) => console.error(e));
	}

	async function acceptJob(requestId: number) {
		try {
			await api.put(`/assistance/${requestId}/accept`);
			alert('Job Accepted!');
			providerStore.load(true); // Refresh list to remove accepted job from pending
		} catch (e) {
			console.error('Failed to accept job:', e);
			alert('Could not accept job. It may have been taken.');
		}
	}
</script>

{#if $user?.is_verified}
	<div class="space-y-6">
		<!-- Welcome Header -->
		<div
			class="rounded-2xl bg-gradient-to-r from-emerald-600 to-green-600 p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<h1 class="text-3xl font-bold">Welcome back, {$user?.first_name}!</h1>
					<p class="mt-2 text-green-100">
						You have {stats.pendingRequests} pending requests nearby
					</p>
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
					aria-label="Toggle Online Status"
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
			<StatsCard
				title="Completed Jobs"
				value={stats.completedJobs}
				icon="fa-check-circle"
				color="purple"
			/>
			<StatsCard
				title="Total Earnings"
				value={`₱${stats.earnings.toFixed(2)}`}
				icon="fa-dollar-sign"
				color="green"
			/>
			<StatsCard title="Rating" value={`${stats.rating}/5.0`} icon="fa-star" color="yellow" />
			<StatsCard title="Avg Response" value={stats.responseTime} icon="fa-clock" color="blue" />
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
								<a
									href="/requests"
									class="flex items-center justify-center rounded-lg border-2 border-gray-200 px-6 py-3 text-sm font-medium text-gray-700 transition-all hover:border-purple-500 hover:text-purple-600"
								>
									<i class="fas fa-info-circle mr-2"></i>
									Details
								</a>
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
{:else}
	<!-- Application / Pending View -->
	<!-- Application / Pending View -->
	<div class="mx-auto max-w-5xl">
		<div class="mb-8 text-center">
			<h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
				Service Provider Application
			</h2>
			<p class="mt-4 text-lg text-gray-600">
				Complete your profile to start accepting jobs on the platform.
			</p>
		</div>

		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Status Sidebar -->
			<div class="lg:col-span-1">
				<div class="overflow-hidden rounded-2xl bg-white shadow-lg">
					<div class="bg-gradient-to-r from-yellow-400 to-orange-500 p-6 text-white">
						<div class="flex items-center space-x-4">
							<div
								class="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 backdrop-blur-sm"
							>
								<i class="fas fa-clock text-2xl text-white"></i>
							</div>
							<div>
								<h3 class="text-lg font-bold">Verification Pending</h3>
								<p class="text-sm text-yellow-50">Action Required</p>
							</div>
						</div>
					</div>
					<div class="p-6">
						<nav aria-label="Progress">
							<ol role="list" class="overflow-hidden">
								<li class="relative pb-10">
									<div
										class="absolute left-4 top-4 -ml-px h-full w-0.5 bg-green-500"
										aria-hidden="true"
									></div>
									<div class="group relative flex items-start">
										<span class="flex h-9 items-center">
											<span
												class="relative z-10 flex h-8 w-8 items-center justify-center rounded-full bg-green-500 group-hover:bg-green-600"
											>
												<i class="fas fa-check text-xs text-white"></i>
											</span>
										</span>
										<span class="ml-4 flex min-w-0 flex-col">
											<span class="text-sm font-medium text-green-500">Account Registered</span>
											<span class="text-sm text-gray-500">Step completed</span>
										</span>
									</div>
								</li>
								<li class="relative">
									<div class="group relative flex items-start">
										<span class="flex h-9 items-center">
											<span
												class="relative z-10 flex h-8 w-8 items-center justify-center rounded-full border-2 border-purple-600 bg-white"
											>
												<span class="h-2.5 w-2.5 rounded-full bg-purple-600"></span>
											</span>
										</span>
										<span class="ml-4 flex min-w-0 flex-col">
											<span class="text-sm font-medium text-purple-600">Profile & Documents</span>
											<span class="text-sm text-gray-500">In Progress</span>
										</span>
									</div>
								</li>
							</ol>
						</nav>
						<div class="mt-6 rounded-lg border border-yellow-100 bg-yellow-50 p-4">
							<div class="flex">
								<div class="flex-shrink-0">
									<i class="fas fa-info-circle text-yellow-400"></i>
								</div>
								<div class="ml-3">
									<h3 class="text-sm font-medium text-yellow-800">Review Process</h3>
									<div class="mt-2 text-sm text-yellow-700">
										<p>Admin review typically takes 24-48 hours. Ensure all documents are clear.</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Main Form -->
			<div class="lg:col-span-2">
				<div class="rounded-2xl border border-gray-100 bg-white p-8 shadow-xl">
					<h3 class="mb-6 flex items-center text-xl font-bold text-gray-900">
						<i class="fas fa-id-card-alt mr-3 text-purple-600"></i>
						Business Details
					</h3>
					<form
						onsubmit={(e) => {
							e.preventDefault();
							submitApplication();
						}}
						class="space-y-6"
					>
						<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
							<div>
								<label for="businessName" class="block text-sm font-medium text-gray-700"
									>Business Name</label
								>
								<div class="relative mt-1 rounded-md shadow-sm">
									<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
										<i class="fas fa-store text-gray-400"></i>
									</div>
									<input
										id="businessName"
										type="text"
										bind:value={applicationData.business_name}
										class="block w-full rounded-lg border-gray-300 py-3 pl-10 focus:border-purple-500 focus:ring-purple-500 sm:text-sm"
										required
									/>
								</div>
							</div>
							<div>
								<label for="baseRate" class="block text-sm font-medium text-gray-700"
									>Base Service Rate (₱)</label
								>
								<div class="relative mt-1 rounded-md shadow-sm">
									<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
										<span class="text-gray-500 sm:text-sm">₱</span>
									</div>
									<input
										id="baseRate"
										type="number"
										bind:value={applicationData.base_rate}
										class="block w-full rounded-lg border-gray-300 py-3 pl-8 focus:border-purple-500 focus:ring-purple-500 sm:text-sm"
										min="0"
									/>
								</div>
							</div>
							<div class="md:col-span-2">
								<label for="businessLicense" class="block text-sm font-medium text-gray-700"
									>Business License / Tax ID</label
								>
								<div class="relative mt-1 rounded-md shadow-sm">
									<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
										<i class="fas fa-certificate text-gray-400"></i>
									</div>
									<input
										id="businessLicense"
										type="text"
										bind:value={applicationData.business_license}
										class="block w-full rounded-lg border-gray-300 py-3 pl-10 focus:border-purple-500 focus:ring-purple-500 sm:text-sm"
										placeholder="Leave empty to auto-generate temporary ID"
									/>
								</div>
							</div>
						</div>

						<div class="pt-4">
							<label class="mb-2 block text-sm font-medium text-gray-700"
								>Registration Documents</label
							>
							<div
								class="relative flex justify-center rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 px-6 py-10 transition-colors hover:border-purple-400 hover:bg-purple-50"
							>
								<div class="space-y-2 text-center">
									<div
										class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-100"
									>
										<i class="fas fa-cloud-upload-alt text-2xl text-purple-600"></i>
									</div>
									<div class="flex justify-center text-sm text-gray-600">
										<label
											for="file-upload"
											class="relative cursor-pointer rounded-md font-medium text-purple-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-purple-500 focus-within:ring-offset-2 hover:text-purple-500"
										>
											<span class="px-1 text-lg">Upload files</span>
											<input
												id="file-upload"
												name="file-upload"
												type="file"
												class="sr-only"
												multiple
												onchange={handleFileUpload}
											/>
										</label>
									</div>
									<p class="text-xs text-gray-500">PNG, JPG, PDF up to 10MB</p>
								</div>
							</div>

							{#if uploadStatus}
								<div class="mt-2 flex items-center text-sm">
									{#if uploadStatus === 'Uploading...'}
										<i class="fas fa-spinner fa-spin mr-2 text-blue-500"></i>
										<span class="text-blue-500">Uploading...</span>
									{:else if uploadStatus === 'Upload failed'}
										<i class="fas fa-times-circle mr-2 text-red-500"></i>
										<span class="text-red-500">Upload failed</span>
									{:else}
										<i class="fas fa-check-circle mr-2 text-green-500"></i>
										<span class="text-green-500">Upload complete</span>
									{/if}
								</div>
							{/if}

							{#if applicationData.documents.length > 0}
								<div class="mt-4 rounded-lg border border-gray-200 bg-gray-50">
									<ul class="divide-y divide-gray-200">
										{#each applicationData.documents as doc}
											<li class="flex items-center justify-between py-3 pl-3 pr-4 text-sm">
												<div class="flex w-0 flex-1 items-center">
													<i class="fas fa-paperclip flex-shrink-0 text-gray-400"></i>
													<span class="ml-2 w-0 flex-1 truncate text-gray-600"
														>{doc.split('/').pop()}</span
													>
												</div>
												<div class="ml-4 flex-shrink-0">
													<a
														href={`http://localhost:8000${doc}`}
														target="_blank"
														class="font-medium text-purple-600 hover:text-purple-500"
													>
														View
													</a>
												</div>
											</li>
										{/each}
									</ul>
								</div>
							{/if}
						</div>

						<div class="border-t border-gray-100 pt-6">
							<button
								type="submit"
								class="w-full transform rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4 text-base font-bold text-white shadow-xl transition-all hover:-translate-y-0.5 hover:from-purple-700 hover:to-pink-700 hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
							>
								Submit Application
								<i class="fas fa-arrow-right ml-2 opacity-80"></i>
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
{/if}
