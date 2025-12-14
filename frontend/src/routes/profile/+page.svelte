<script lang="ts">
	import { user, logout } from '$lib/stores/auth';
	import StatsCard from '$lib/components/common/StatsCard.svelte';
	import { goto } from '$app/navigation';

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<svelte:head>
	<title>Profile - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-3xl space-y-6">
	<!-- Header -->
	<div
		class="rounded-2xl bg-gradient-to-r p-8 text-white shadow-lg"
		class:from-orange-600={$user?.role === 'admin'}
		class:to-red-700={$user?.role === 'admin'}
		class:from-green-600={$user?.role === 'service_provider'}
		class:to-emerald-700={$user?.role === 'service_provider'}
		class:from-cyan-600={$user?.role === 'driver'}
		class:to-blue-700={$user?.role === 'driver'}
		class:from-blue-600={!$user?.role}
		class:to-indigo-700={!$user?.role}
	>
		<div class="flex flex-col items-center md:flex-row md:items-start md:space-x-6">
			<div
				class="flex h-24 w-24 items-center justify-center rounded-full bg-white/20 text-4xl font-bold backdrop-blur-sm"
			>
				{$user?.first_name?.charAt(0)}
			</div>
			<div class="mt-4 text-center md:mt-0 md:text-left">
				<h1 class="text-3xl font-bold">{$user?.first_name} {$user?.last_name}</h1>
				<p class="mt-1 text-blue-100">{$user?.email}</p>
				<div class="mt-4 flex flex-wrap justify-center gap-2 md:justify-start">
					<span class="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold backdrop-blur-sm">
						{($user?.role || 'User').replace('_', ' ').toUpperCase()}
					</span>
					<span
						class={`rounded-full px-3 py-1 text-xs font-semibold backdrop-blur-sm ${$user?.is_verified ? 'bg-green-400/30 text-green-50' : 'bg-yellow-400/30 text-yellow-50'}`}
					>
						{$user?.is_verified ? 'VERIFIED' : 'PENDING VERIFICATION'}
					</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Details -->
	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		<div class="border-b border-gray-100 px-6 py-5">
			<h3 class="text-lg font-bold leading-6 text-gray-900">Account Details</h3>
		</div>
		<div class="px-6 py-5">
			<dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
				<div>
					<dt class="text-sm font-medium text-gray-500">Phone Number</dt>
					<dd class="mt-1 text-sm text-gray-900">{$user?.phone || 'Not provided'}</dd>
				</div>
				<div>
					<dt class="text-sm font-medium text-gray-500">Member Since</dt>
					<dd class="mt-1 text-sm text-gray-900">
						{new Date($user?.created_at || Date.now()).toLocaleDateString()}
					</dd>
				</div>
				<div class="sm:col-span-2">
					<dt class="text-sm font-medium text-gray-500">Account ID</dt>
					<dd class="mt-1 font-mono text-sm text-gray-900">{$user?.id}</dd>
				</div>
			</dl>
		</div>
	</div>

	<!-- Actions -->
	<div class="flex justify-end space-x-4">
		<button
			onclick={handleLogout}
			class="rounded-lg border border-red-200 bg-red-50 px-6 py-3 text-sm font-bold text-red-600 transition-colors hover:bg-red-100"
		>
			<i class="fas fa-sign-out-alt mr-2"></i>
			Sign Out
		</button>
	</div>
</div>
