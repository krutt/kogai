<script setup lang='ts'>
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
</script>

<template>
  <div class="flex flex-col">
    <div class="flex-1 space-y-4 p-8 pt-6">
      <div class="flex items-center justify-between space-y-2">
        <h2 class="text-3xl font-bold tracking-tight">
          Kogai
        </h2>
      </div>
    </div>
    <div class="grid gap-4 py-4 md:grid-cols-2 lg:grid-cols-4">
      <card>
        <card-header class="flex flex-row items-center justify-between space-y-0 pb-2">
          <card-title class="text-sm font-medium">
            Script
          </card-title>
        </card-header>
        <card-content>
          BUIDL
        </card-content>
      </card>
      <card>
        <card-header class="flex flex-row items-center justify-between space-y-0 pb-2">
          <card-title class="text-sm font-medium">
            Bitcoin Tx
          </card-title>
        </card-header>
        <card-content>
          Transaction
        </card-content>
      </card>
    </div>
  </div>
</template>
