<script setup lang="ts">
/* imports */
import { onMounted, ref } from 'vue'

/* components */
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import GithubBadge from '@/assets/github.svg'

let albyAddress = ref('')
let albyPublicKey = ref('')
let blockHashes = ref([])
let lockAddress = ref('')

let connectWallet = async () => {
  const _window = window as typeof window & { webbtc?: any }
  if (typeof _window.webbtc !== 'undefined') {
    await _window.webbtc.enable()
    let { address, publicKey } = await _window.webbtc.getAddress()
    albyAddress.value = address
    albyPublicKey.value = publicKey
  }
}

let openGithubRepository = () => {
  window.open('https://github.com/krutt/kogai.git', '_blank', 'noreferrer, noopener')
}

let createTaprootAddress = async () => {
  await fetch('/lock', {
    method: 'POST',
    body: JSON.stringify({ pubkey: albyPublicKey.value }),
    headers: { 'Content-Type': 'application/json;' },
  })
    .catch(console.error)
    .then(async resp => {
      if (!!resp) {
        let { address } = await resp.json()
        lockAddress.value = address
      }
    })
}

onMounted(async () => {
  const eventSource = new EventSource('/blocks')
  eventSource.addEventListener('message', event => {
    let { blockHash } = JSON.parse(event.data)
    if (blockHashes.value.includes(blockHash)) return
    blockHashes.value.push(blockHash)
  })
  eventSource.addEventListener('end', () => {
    eventSource.close()
  })
})
</script>

<template>
  <div class="flex flex-col">
    <div class="flex-1 space-y-4 p-8 pt-6">
      <div class="flex items-center justify-between space-y-2">
        <h2 class="text-3xl font-bold tracking-tight">Kogai</h2>
      </div>
    </div>
    <section class="container grid lg:grid-cols-2 place-items-center py-20 md:py-32 gap-10">
      <div class="text-center lg:text-start space-y-6">
        <main class="text-5xl md:text-6xl font-bold">
          <h1 class="inline">
            <span
              class="inline bg-gradient-to-r from-[#FF146E] via-[#FFADCD] to-[#FF146E] text-transparent bg-clip-text"
            >
              Kogai
            </span>
            create simple locks
          </h1>
          <h2 class="inline">
            with
            <span
              class="inline bg-gradient-to-r from-[#ff9999] via-[#ff9900] to-[#ff9999] text-transparent bg-clip-text"
            >
              Taproot
            </span>
            address
          </h2>
        </main>
        <div class="space-y-4 md:space-y-0 md:space-x-4">
          <Button @click="connectWallet" class="w-full md:w-1/3" v-if="!albyAddress">
            Connect Wallet
          </Button>
          <Button @click="openGithubRepository" class="md:w-1/3 w-full" variant="outline">
            Repository
            <github-badge class="h-6 inline ml-2 w-auto" />
          </Button>
        </div>
      </div>
      <div class="grid gap-4 py-4 grid-cols-1">
        <Card v-if="albyAddress">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium"> Address </CardTitle>
          </CardHeader>
          <CardContent>
            <span>
              {{ albyAddress }}
            </span>
            <Button @click="createTaprootAddress" class="float-right mb-4 mt-4">
              Create Taproot Address
            </Button>
          </CardContent>
        </Card>
        <Card v-if="lockAddress">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium"> Lock Address </CardTitle>
          </CardHeader>
          <CardContent>
            {{ lockAddress }}
          </CardContent>
        </Card>
      </div>
      <div class="grid gap-4 py-4 grid-cols-1 hidden">
        <h2 class="inline">Blocks since Pageload</h2>
        <Card v-for="blockHash in blockHashes">
          <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle class="text-sm font-medium">{{ blockHash }} </CardTitle>
          </CardHeader>
        </Card>
      </div>
    </section>
  </div>
</template>
