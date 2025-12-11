<script lang="ts">
  export let title = 'Breakdowns';
</script>

<svelte:head>
  <title>App - Breakdowns</title>
</svelte:head>

<div class="p-6 bg-white rounded shadow">
  <h2 class="text-2xl font-semibold mb-4">Breakdowns</h2>
  <div class="mb-4 text-sm text-gray-600">Manage and track breakdown reports.</div>
  <div class="space-y-3">
    <div class="p-3 border rounded">
      <div class="flex justify-between"><div><strong>Flat tire</strong><div class="text-xs text-gray-500">M. dela Cruz St.</div></div><div class="text-sm text-yellow-700">Reported</div></div>
    </div>
    <div class="p-3 border rounded">
      <div class="flex justify-between"><div><strong>Battery issue</strong><div class="text-xs text-gray-500">LRT-1 Station</div></div><div class="text-sm text-blue-700">Assigned</div></div>
    </div>
  </div>
</div>
