<script lang="ts">
  import { onMount } from 'svelte';
  import AppTemplate from '$lib/components/AppTemplate.svelte';

  // Mock data
  let vehicles = [
    { id: 1, plate: 'ABC-123', model: 'Toyota Vios', mileage: 45200 },
    { id: 2, plate: 'XYZ-789', model: 'Honda Civic', mileage: 128000 },
    { id: 3, plate: 'LMN-456', model: 'Nissan Almera', mileage: 200500 }
  ];

  let breakdowns = [
    { id: 1, title: 'Flat tire', location: 'M. dela Cruz St.', status: 'reported', time: '10:12 AM' },
    { id: 2, title: 'Battery issue', location: 'LRT-1 Station', status: 'assigned', time: '09:05 AM' }
  ];

  let filter = '';
  $: filteredVehicles = vehicles.filter(v => v.plate.toLowerCase().includes(filter.toLowerCase()) || v.model.toLowerCase().includes(filter.toLowerCase()));
</script>

<svelte:head>
  <title>App — VBAMS</title>
</svelte:head>

<AppTemplate title="VBAMS — App">
  <div class="max-w-7xl mx-auto">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p class="text-sm text-gray-500">Overview of vehicles, breakdowns and assistance.</p>
            </div>
            <div class="flex items-center gap-3">
              <button class="px-4 py-2 bg-white border rounded-md text-sm hover:bg-gray-50">Export</button>
              <a href="/app/vehicles" class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700">Manage Vehicles</a>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="p-4 bg-gray-50 rounded">
              <div class="text-sm text-gray-500">Total Vehicles</div>
              <div class="text-3xl font-bold text-gray-900">{vehicles.length}</div>
              <div class="text-xs text-gray-400 mt-2">Registered vehicles in the system</div>
            </div>
            <div class="p-4 bg-gray-50 rounded">
              <div class="text-sm text-gray-500">Open Breakdowns</div>
              <div class="text-3xl font-bold text-gray-900">{breakdowns.length}</div>
              <div class="text-xs text-gray-400 mt-2">Breakdowns awaiting assignment</div>
            </div>
            <div class="p-4 bg-gray-50 rounded">
              <div class="text-sm text-gray-500">Active Assistance</div>
              <div class="text-3xl font-bold text-gray-900">2</div>
              <div class="text-xs text-gray-400 mt-2">Ongoing assistance requests</div>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 bg-white border rounded">
              <h3 class="font-medium mb-2">Recent Breakdowns</h3>
              <ul class="divide-y divide-gray-100">
                {#each breakdowns as b}
                  <li class="py-3 flex justify-between items-center">
                    <div>
                      <div class="font-medium">{b.title}</div>
                      <div class="text-xs text-gray-500">{b.location} • {b.time}</div>
                    </div>
                    <div class="text-sm px-3 py-1 rounded {b.status === 'reported' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-50 text-blue-800'}">{b.status}</div>
                  </li>
                {/each}
              </ul>
            </div>

            <div class="p-4 bg-white border rounded">
              <h3 class="font-medium mb-2">Upcoming Tasks</h3>
              <ul class="space-y-2 text-sm text-gray-700">
                <li>Service provider visit scheduled — 2:30 PM</li>
                <li>Vehicle inspection due — 3 vehicles</li>
                <li>Update vehicle insurance information</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="font-medium mb-3">Map</h3>
          <div class="h-64 bg-gray-100 rounded flex items-center justify-center text-gray-500">Map area</div>
        </div>
      </div>

      <aside class="space-y-6">
        <div class="bg-white rounded-lg shadow p-4">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-medium">My Vehicles</h3>
            <div class="text-sm text-gray-500">{vehicles.length}</div>
          </div>
          <input placeholder="Filter" bind:value={filter} class="w-full p-2 mb-3 border rounded-md" />
          <div class="space-y-2">
            {#each filteredVehicles as v}
              <div class="p-2 border rounded flex justify-between items-center">
                <div>
                  <div class="font-medium">{v.plate}</div>
                  <div class="text-xs text-gray-500">{v.model}</div>
                </div>
                <div class="text-sm text-gray-600">{v.mileage} km</div>
              </div>
            {/each}
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="font-medium mb-2">Quick Actions</h3>
          <div class="flex flex-col gap-2">
            <button class="px-3 py-2 bg-blue-600 text-white rounded">Report Breakdown</button>
            <button class="px-3 py-2 bg-gray-100 rounded">Add Vehicle</button>
            <button class="px-3 py-2 bg-gray-100 rounded">Update Location</button>
          </div>
        </div>
      </aside>
    </div>
  </div>
</AppTemplate>
