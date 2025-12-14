<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';

	import { providerStore } from '$lib/stores/dashboard';

	let allJobs = $derived($providerStore.data?.allJobs || []);
	let loading = $derived($providerStore.loading);
	let today = new Date();

	// Computed Earnings
	let earnings = $derived.by(() => {
		const jobs = allJobs.filter((j: any) => j.status === 'completed');

		const isToday = (date: Date) => date.toDateString() === today.toDateString();
		const isThisWeek = (date: Date) => {
			const d = new Date(date);
			const day = today.getDay();
			const diff = today.getDate() - day + (day === 0 ? -6 : 1);
			const monday = new Date(today.setDate(diff));
			return d >= monday;
		};
		const isThisMonth = (date: Date) =>
			date.getMonth() === today.getMonth() && date.getFullYear() === today.getFullYear();

		return {
			today: jobs
				.filter((j) => isToday(new Date(j.created_at)))
				.reduce((acc, j) => acc + (j.actual_cost || 0), 0),
			thisWeek: jobs
				.filter((j) => isThisWeek(new Date(j.created_at)))
				.reduce((acc, j) => acc + (j.actual_cost || 0), 0),
			thisMonth: jobs
				.filter((j) => isThisMonth(new Date(j.created_at)))
				.reduce((acc, j) => acc + (j.actual_cost || 0), 0),
			total: jobs.reduce((acc, j) => acc + (j.actual_cost || 0), 0)
		};
	});

	let transactions = $derived(
		allJobs
			.filter((j: any) => j.status === 'completed')
			.map((j: any) => ({
				job: j.service_type?.replace(/_/g, ' ').toUpperCase() || 'SERVICE',
				customer: `Customer #${j.requester_id}`,
				date: new Date(j.created_at).toLocaleDateString(),
				amount: j.actual_cost || 0,
				status: 'paid' // Assuming completed means paid for now
			}))
	);

	onMount(() => {
		providerStore.load();
	});
</script>

<svelte:head>
	<title>Earnings - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold text-gray-900">My Earnings</h1>
		<div class="flex items-center gap-4">
			<p class="mt-2 text-sm text-gray-600">Track your income and payment history</p>
		</div>
	</div>

	<!-- Earnings Cards -->
	<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
		<div class="rounded-xl bg-gradient-to-br from-green-500 to-green-600 p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Today</p>
					<p class="mt-2 text-3xl font-bold">₱{earnings.today}</p>
				</div>
				<i class="fas fa-calendar-day text-3xl opacity-75"></i>
			</div>
		</div>
		<div class="rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">This Week</p>
					<p class="mt-2 text-3xl font-bold">₱{earnings.thisWeek}</p>
				</div>
				<i class="fas fa-calendar-week text-3xl opacity-75"></i>
			</div>
		</div>
		<div
			class="rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">This Month</p>
					<p class="mt-2 text-3xl font-bold">₱{earnings.thisMonth}</p>
				</div>
				<i class="fas fa-calendar-alt text-3xl opacity-75"></i>
			</div>
		</div>
		<div
			class="rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Total Earnings</p>
					<p class="mt-2 text-3xl font-bold">₱{earnings.total}</p>
				</div>
				<i class="fas fa-chart-line text-3xl opacity-75"></i>
			</div>
		</div>
	</div>

	<!-- Transaction History -->
	<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg">
		<div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
			<h2 class="text-xl font-bold text-gray-900">Recent Transactions</h2>
		</div>
		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Job</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Customer</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Date</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Amount</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Status</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 bg-white">
					{#each transactions as transaction}
						<tr class="hover:bg-gray-50">
							<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900"
								>{transaction.job}</td
							>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-600"
								>{transaction.customer}</td
							>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-600">{transaction.date}</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm font-bold text-green-600"
								>₱{transaction.amount}</td
							>
							<td class="whitespace-nowrap px-6 py-4">
								<span
									class={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${transaction.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}
								>
									{transaction.status.toUpperCase()}
								</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
