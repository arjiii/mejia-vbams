<script lang="ts">
	interface Job {
		id: number;
		customer: string;
		type: string;
		status: string;
		location: string;
		scheduledAt: string;
		payment: number;
	}

	import { onMount } from 'svelte';
	import { providerStore } from '$lib/stores/dashboard';

	let jobs = $derived(
		($providerStore.data?.allJobs || []).map((j: any) => ({
			id: j.id,
			customer: `Customer #${j.requester_id}`,
			type: j.service_type?.replace(/_/g, ' ').toUpperCase(),
			status: j.status,
			location: j.address || 'Unknown Location',
			scheduledAt: new Date(j.created_at).toLocaleString(),
			payment: j.actual_cost || j.estimated_cost || 0
		}))
	);

	onMount(() => {
		providerStore.load();
	});

	function refreshData() {
		providerStore.load(true);
	}

	function getStatusColor(status: string) {
		const colors: Record<string, string> = {
			completed: 'bg-green-100 text-green-800',
			in_progress: 'bg-blue-100 text-blue-800',
			scheduled: 'bg-yellow-100 text-yellow-800',
			cancelled: 'bg-red-100 text-red-800'
		};
		return colors[status] || 'bg-gray-100 text-gray-800';
	}
</script>

<svelte:head>
	<title>My Jobs - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">My Jobs</h1>
			<p class="mt-2 text-sm text-gray-600">Manage your assigned and completed jobs</p>
		</div>
		<button
			onclick={refreshData}
			class="rounded-lg bg-gray-100 px-3 py-2 text-xs font-bold text-gray-600 hover:bg-gray-200"
		>
			<i class="fas fa-sync-alt mr-2"></i>Refresh
		</button>
	</div>

	<!-- Jobs List -->
	<div class="space-y-4">
		{#each jobs as job}
			<div
				class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg transition-all hover:shadow-xl"
			>
				<div class="flex items-start justify-between">
					<div class="flex-1">
						<div class="mb-2 flex items-center gap-3">
							<h3 class="text-lg font-bold text-gray-900">{job.type}</h3>
							<span
								class={`rounded-full px-3 py-1 text-xs font-medium ${getStatusColor(job.status)}`}
							>
								{job.status.replace('_', ' ').toUpperCase()}
							</span>
						</div>
						<div class="grid grid-cols-1 gap-2 md:grid-cols-2">
							<div class="flex items-center text-sm text-gray-600">
								<i class="fas fa-user w-5 text-gray-400"></i>
								<span class="ml-2">{job.customer}</span>
							</div>
							<div class="flex items-center text-sm text-gray-600">
								<i class="fas fa-map-marker-alt w-5 text-gray-400"></i>
								<span class="ml-2">{job.location}</span>
							</div>
							<div class="flex items-center text-sm text-gray-600">
								<i class="fas fa-clock w-5 text-gray-400"></i>
								<span class="ml-2">{job.scheduledAt}</span>
							</div>
							<div class="flex items-center text-sm font-medium text-green-600">
								<i class="fas fa-dollar-sign w-5"></i>
								<span class="ml-2">₱{job.payment}</span>
							</div>
						</div>
					</div>
					<button
						class="ml-4 rounded-lg border-2 border-purple-500 px-4 py-2 text-sm font-medium text-purple-600 transition-all hover:bg-purple-50"
					>
						<i class="fas fa-eye mr-1"></i>
						View Details
					</button>
				</div>
			</div>
		{/each}
	</div>
</div>
