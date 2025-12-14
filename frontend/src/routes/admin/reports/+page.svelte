<script lang="ts">
	import { onMount } from 'svelte';
	import { adminStore } from '$lib/stores/dashboard';

	let reportType = $state('monthly');
	let reportPeriod = $state('last30days');
	let loading = $derived($adminStore.loading);

	let stats = $derived.by(() => {
		if (!$adminStore.data) {
			return {
				totalUsers: 0,
				serviceProviders: 0,
				completedJobs: 0,
				activeBreakdowns: 0
			};
		}

		const requests = $adminStore.data.requests || [];
		const completed = requests.filter((r: any) => r.status === 'completed').length;

		return {
			totalUsers: $adminStore.data.stats.totalUsers,
			serviceProviders: $adminStore.data.stats.totalProviders,
			completedJobs: completed,
			activeBreakdowns: $adminStore.data.stats.activeBreakdowns
		};
	});

	onMount(() => {
		adminStore.load();
	});
</script>

<svelte:head>
	<title>Reports - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">System Reports</h1>
				<p class="mt-2 text-sm text-gray-600">View analytics and generate custom reports</p>
			</div>
		</div>
	</div>

	<!-- Stats Overview -->
	<div class="grid grid-cols-1 gap-6 md:grid-cols-4">
		<div class="rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white shadow-lg">
			<i class="fas fa-users text-3xl opacity-75"></i>
			<div class="mt-4">
				<div class="text-3xl font-bold">{stats.totalUsers}</div>
				<div class="text-sm opacity-90">Total Users</div>
			</div>
		</div>
		<div
			class="rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 p-6 text-white shadow-lg"
		>
			<i class="fas fa-tools text-3xl opacity-75"></i>
			<div class="mt-4">
				<div class="text-3xl font-bold">{stats.serviceProviders}</div>
				<div class="text-sm opacity-90">Service Providers</div>
			</div>
		</div>
		<div class="rounded-xl bg-gradient-to-br from-green-500 to-green-600 p-6 text-white shadow-lg">
			<i class="fas fa-check-circle text-3xl opacity-75"></i>
			<div class="mt-4">
				<div class="text-3xl font-bold">{stats.completedJobs}</div>
				<div class="text-sm opacity-90">Completed Jobs</div>
			</div>
		</div>
		<div class="rounded-xl bg-gradient-to-br from-red-500 to-red-600 p-6 text-white shadow-lg">
			<i class="fas fa-car-crash text-3xl opacity-75"></i>
			<div class="mt-4">
				<div class="text-3xl font-bold">{stats.activeBreakdowns}</div>
				<div class="text-sm opacity-90">Active Breakdowns</div>
			</div>
		</div>
	</div>

	<!-- Report Generator -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-4 text-xl font-bold text-gray-900">Generate Custom Report</h2>
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Report Type</label>
				<select
					bind:value={reportType}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2"
				>
					<option value="monthly">Monthly Summary</option>
					<option value="users">User Analytics</option>
					<option value="providers">Provider Performance</option>
					<option value="financial">Financial Report</option>
				</select>
			</div>
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Time Period</label>
				<select
					bind:value={reportPeriod}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2"
				>
					<option value="last7days">Last 7 Days</option>
					<option value="last30days">Last 30 Days</option>
					<option value="last3months">Last 3 Months</option>
					<option value="lastyear">Last Year</option>
				</select>
			</div>
			<div class="flex items-end">
				<button
					class="w-full rounded-lg bg-gradient-to-r from-red-600 to-orange-600 px-4 py-2 text-sm font-bold text-white shadow-lg hover:from-red-700 hover:to-orange-700"
				>
					<i class="fas fa-download mr-2"></i>
					Generate Report
				</button>
			</div>
		</div>
	</div>

	<!-- Chart Placeholder -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-4 text-xl font-bold text-gray-900">Activity Overview</h2>
		<div class="flex h-64 items-center justify-center rounded-lg bg-gray-50">
			<div class="text-center">
				<i class="fas fa-chart-line mb-4 text-6xl text-gray-300"></i>
				<p class="text-gray-500">Chart visualization will appear here</p>
			</div>
		</div>
	</div>
</div>
