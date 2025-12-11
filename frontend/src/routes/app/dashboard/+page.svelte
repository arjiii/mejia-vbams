<script lang="ts">
  export let title = 'Dashboard';
</script>

<svelte:head>
  <title>App - Dashboard</title>
</svelte:head>

<div class="p-6 bg-white rounded shadow">
  <h2 class="text-2xl font-semibold mb-4">Dashboard</h2>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div class="p-4 bg-gray-50 rounded">
      <h3 class="text-sm text-gray-500">Total Vehicles</h3>
      <div class="text-3xl font-bold text-gray-900 mt-2">12</div>
      <p class="text-xs text-gray-500 mt-1">Registered vehicles in the system</p>
    </div>
    <div class="p-4 bg-gray-50 rounded">
      <h3 class="text-sm text-gray-500">Open Breakdowns</h3>
      <div class="text-3xl font-bold text-gray-900 mt-2">3</div>
      <p class="text-xs text-gray-500 mt-1">Breakdowns awaiting assignment</p>
    </div>
    <div class="p-4 bg-gray-50 rounded">
      <h3 class="text-sm text-gray-500">Active Assistance</h3>
      <div class="text-3xl font-bold text-gray-900 mt-2">2</div>
      <p class="text-xs text-gray-500 mt-1">Ongoing assistance requests</p>
    </div>
  </div>

  <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4">
    <section class="bg-white border rounded p-4">
      <h4 class="font-medium mb-2">Recent Breakdowns</h4>
      <ul class="space-y-2 text-sm text-gray-700">
        <li class="flex justify-between"><span>Flat tire — M. dela Cruz St.</span><span class="text-xs text-gray-500">10:12 AM</span></li>
        <li class="flex justify-between"><span>Battery issue — LRT-1 Station</span><span class="text-xs text-gray-500">09:05 AM</span></li>
        <li class="flex justify-between"><span>Overheating — EDSA</span><span class="text-xs text-gray-500">Yesterday</span></li>
      </ul>
    </section>

    <section class="bg-white border rounded p-4">
      <h4 class="font-medium mb-2">Upcoming Tasks</h4>
      <ul class="space-y-2 text-sm text-gray-700">
        <li>Service provider visit scheduled — 2:30 PM</li>
        <li>Vehicle inspection due — 3 vehicles</li>
        <li>Update vehicle insurance information</li>
      </ul>
    </section>
  </div>
</div>
