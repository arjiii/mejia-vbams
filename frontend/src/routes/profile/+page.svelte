<script lang="ts">
	import { user } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	let currentUser: any = null;

	onMount(() => {
		const unsubscribe = user.subscribe((value) => {
			currentUser = value;
		});
		return () => unsubscribe();
	});
</script>

<svelte:head>
	<title>Profile - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-4xl space-y-6 p-6">
	<h1 class="text-3xl font-bold text-gray-900">My Profile</h1>
	{#if currentUser}
		<div class="mt-4 rounded-xl bg-white p-6 shadow-lg">
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div>
					<h2 class="text-xl font-semibold text-gray-800">Personal Info</h2>
					<p class="mt-2 text-gray-600"><strong>Name:</strong> {currentUser.name}</p>
					<p class="text-gray-600"><strong>Email:</strong> {currentUser.email}</p>
					<p class="text-gray-600"><strong>Role:</strong> {currentUser.role.replace('_', ' ')}</p>
				</div>
				{#if currentUser.role === 'driver'}
					<div>
						<h2 class="text-xl font-semibold text-gray-800">Vehicle Management</h2>
						<p class="mt-2 text-gray-600">
							You can add, edit, or remove your vehicles from the <a
								href="/vehicles"
								class="text-blue-600 hover:underline">Vehicles</a
							> page.
						</p>
					</div>
				{:else if currentUser.role === 'service_provider'}
					<div>
						<h2 class="text-xl font-semibold text-gray-800">Provider Settings</h2>
						<p class="mt-2 text-gray-600">
							Manage your availability, earnings, and job preferences from the <a
								href="/availability"
								class="text-blue-600 hover:underline">Availability</a
							>
							and <a href="/earnings" class="text-blue-600 hover:underline">Earnings</a> pages.
						</p>
					</div>
				{:else if currentUser.role === 'admin'}
					<div>
						<h2 class="text-xl font-semibold text-gray-800">Admin Shortcuts</h2>
						<p class="mt-2 text-gray-600">
							Quick access to management sections: <a
								href="/admin/users"
								class="text-blue-600 hover:underline">User Management</a
							>,
							<a href="/admin/providers" class="text-blue-600 hover:underline"
								>Provider Management</a
							>, <a href="/admin/reports" class="text-blue-600 hover:underline">Reports</a>,
							<a href="/admin/settings" class="text-blue-600 hover:underline">Settings</a>.
						</p>
					</div>
				{/if}
			</div>
		</div>
	{:else}
		<p class="text-gray-500">Loading profile...</p>
	{/if}
</div>
