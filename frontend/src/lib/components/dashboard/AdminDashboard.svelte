<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';
	import StatsCard from '$lib/components/common/StatsCard.svelte';
	import UsersTable from '$lib/components/dashboard/admin/UsersTable.svelte';
	import ProvidersTable from '$lib/components/dashboard/admin/ProvidersTable.svelte';
	import { adminStore } from '$lib/stores/dashboard';

	// Derived state from store
	let stats = $derived(
		$adminStore.data?.stats || { totalUsers: 0, totalProviders: 0, activeBreakdowns: 0 }
	);
	let users = $derived($adminStore.data?.users || []);
	let providers = $derived($adminStore.data?.providers || []);
	let activeTab = $state('users');

	onMount(() => {
		adminStore.load();
	});
</script>

<div class="space-y-6">
	<!-- Welcome Header -->
	<div class="rounded-2xl bg-gradient-to-r from-red-600 to-orange-600 p-6 text-white shadow-lg">
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-3xl font-bold">Welcome Admin, {$user?.first_name || 'User'}</h1>
				<p class="mt-2 text-red-100">Manage users and service providers across the system</p>
			</div>
			<div class="hidden md:block">
				<p class="mt-1 text-red-100">Overview of system performance and user statistics</p>
			</div>
		</div>
	</div>

	<!-- Stats -->
	<div class="grid grid-cols-1 gap-5 sm:grid-cols-3">
		<StatsCard title="Total Users" value={stats.totalUsers} icon="fa-users" color="blue" />
		<StatsCard
			title="Service Providers"
			value={stats.totalProviders}
			icon="fa-tools"
			color="purple"
		/>
		<StatsCard
			title="Active Breakdowns"
			value={stats.activeBreakdowns}
			icon="fa-car-crash"
			color="red"
		/>
	</div>

	<!-- Tabs -->
	<div class="border-b border-gray-200">
		<nav class="-mb-px flex space-x-8">
			<button
				class={`whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors duration-200 ${activeTab === 'users' ? 'border-red-500 text-red-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
				onclick={() => (activeTab = 'users')}
			>
				<i class="fas fa-users mr-2"></i> Users
			</button>
			<button
				class={`whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors duration-200 ${activeTab === 'providers' ? 'border-red-500 text-red-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
				onclick={() => (activeTab = 'providers')}
			>
				<i class="fas fa-tools mr-2"></i> Service Providers
			</button>
		</nav>
	</div>

	<!-- Content -->
	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		{#if activeTab === 'users'}
			<UsersTable {users} />
		{:else}
			<ProvidersTable {providers} />
		{/if}
	</div>
</div>
