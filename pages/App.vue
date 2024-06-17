<script setup lang="ts">
/* imports */
import { Ref, onMounted, ref } from 'vue'

/* components */
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

/* vectors */
import AlbyLogo from '@/assets/alby.svg'
import BitcoinDocs from '@/assets/bitcoindocs.svg'
import GithubBadge from '@/assets/github.svg'

let albyAddress: Ref<string> = ref('')
let albyDerivationPath: Ref<string> = ref('')
let albyPublicKey: Ref<string> = ref('')
let balance: Ref<number> = ref(0)
let blockHashes: Ref<Array<string>> = ref([])
let lockAddress: Ref<string> = ref('')
let lockTxid: Ref<string> = ref('')
let unlockTxid: Ref<string> = ref('')

let connectWallet = async () => {
  const _window = window as typeof window & { webbtc?: any }
  if (typeof _window.webbtc !== 'undefined') {
    await _window.webbtc.enable()
    let { address, derivationPath, publicKey } = await _window.webbtc.getAddress()
    albyAddress.value = address
    albyDerivationPath.value = derivationPath
    albyPublicKey.value = publicKey
  }
}

let openBitcoinDocs = () => {
  window.open(
    'https://bitcoindocs.org/notes/taproot-lock-and-spend-taproot-script-path-with-python',
    '_blank',
    'noreferrer, noopener'
  )
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

let fetchBalance = async () => {
  await fetch(`/balance/${albyAddress.value}`)
    .catch(console.error)
    .then(async resp => {
      if (!!resp) {
        let data = await resp.json()
        balance.value = data.balance
      }
    })
}

let sendToLock = async () => {
  // Switch to unisat for payment
  await fetch('/send', {
    body: JSON.stringify({ address: lockAddress.value, amount: 1.0 }),
    headers: { 'Content-Type': 'application/json;' },
    method: 'POST',
  })
    .catch(console.error)
    .then(async resp => {
      if (!!resp) {
        let { txid } = await resp.json()
        lockTxid.value = txid
      }
    })
}

let tapFaucet = async () => {
  await fetch('/faucet', {
    body: JSON.stringify({ address: albyAddress.value }),
    headers: { 'Content-Type': 'application/json;' },
    method: 'POST',
  })
    .catch(console.error)
    .then(console.log)
}

let unlock = async () => {
  await fetch('/unlock', {
    body: JSON.stringify({
      address: albyAddress.value,
      pubkey: albyPublicKey.value,
      txid: lockTxid.value,
    }),
    headers: { 'Content-Type': 'application/json;' },
    method: 'POST',
  })
    .catch(console.error)
    .then(async resp => {
      let { txid } = await resp.json()
      unlockTxid.value = txid
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
        <Button @click="connectWallet" class="cursor-pointer float-right md:w-1/4 w-1/2" v-if="!albyAddress">
          Connect Wallet
          <alby-logo class="h-6 inline ml-2 w-auto" />
        </Button>
        <span class="float-right" v-if="albyAddress">
          Balance:&nbsp;
          {{ balance }}
          &nbsp;₿
        </span>
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
          <Button
            @click="openGithubRepository"
            class="cursor-pointer md:w-1/3 w-full"
            variant="outline"
          >
            Repository
            <github-badge class="h-6 inline ml-2 w-auto" />
          </Button>
          <Button @click="openBitcoinDocs" class="cursor-pointer md:w-1/3 w-full" variant="outline">
            Note by Katsu
            <bitcoin-docs class="h-6 inline ml-2 w-auto" />
          </Button>
        </div>
      </div>
      <div class="grid gap-4 py-4 grid-cols-1">
        <Card v-if="albyAddress">
          <CardHeader>
            <CardTitle> Address </CardTitle>
            <CardDescription>
              This is your Bitcoin Address currently selected and provided by Alby Wallet Extension.
            </CardDescription>
          </CardHeader>
          <CardContent class="break-all text-sm font-medium">
            {{ albyAddress }}
          </CardContent>
          <CardFooter class="justify-between space-x-2">
            <Button
              @click="tapFaucet"
              class="cursor-pointer"
              variant="secondary"
            >
              Tap Faucet
            </Button>
            <Button
              @click="fetchBalance"
              class="cursor-pointer"
              variant="outline"
            >
              Fetch Balance
            </Button>
          </CardFooter>
        </Card>
        <Card v-if="albyAddress && !lockAddress">
          <CardHeader>
            <CardTitle> Create Taproot Lock </CardTitle>
            <CardDescription>
              Here we will construct an address that locks its funds that will only be spendable if
              any of the 3 mathematical equations get solved.
            </CardDescription>
          </CardHeader>
          <CardFooter class="flex flex-col items-end">
            <Button @click="createTaprootAddress" class="cursor-pointer">
              Create Taproot Address
            </Button>
          </CardFooter>
        </Card>
        <Card v-if="lockAddress">
          <CardHeader>
            <CardTitle> Lock Address </CardTitle>
            <CardDescription>
              After getting an address, send 0.01 BTC to it. In the next step, we'll solve one of
              the equations and spend those funds.
            </CardDescription>
          </CardHeader>
          <CardContent class="break-all text-sm font-medium">
            {{ lockAddress }}
          </CardContent>
          <CardFooter class="flex flex-col items-end">
            <Button
              @click="sendToLock"
              :variant="!lockTxid ? '' : 'outline'"
              class="cursor-pointer"
            >
              Send 0.1 BTC to Lock Address
            </Button>
          </CardFooter>
        </Card>
        <Card v-if="lockTxid">
          <CardHeader>
            <CardTitle> Locking Transaction Hash </CardTitle>
            <CardDescription>
              In this example, we will unlock the funds by solving the 2nd mathematical equation
              (x + 2 = 4). In order to unlock the funds we must provide a value X.
            </CardDescription>
          </CardHeader>
          <CardContent class="break-all font-medium text-sm">
            {{ lockTxid }}
          </CardContent>
          <CardFooter class="flex flex-col items-end">
            <Button @click="unlock" class="cursor-pointer float-right mb-4 mt-4" :variant="!unlockTxid ? '' : 'outline'">
              Unlock
            </Button>
          </CardFooter>
        </Card>
        <Card v-if="unlockTxid">
          <CardHeader>
            <CardTitle> Unlocking Transaction Hash </CardTitle>
          </CardHeader>
          <CardContent class="break-all text-sm font-medium">
            {{ unlockTxid }}
          </CardContent>
          <CardFooter class="flex flex-col items-end">
            <Button
              @click="fetchBalance"
              class="cursor-pointer float-right mb-4 mt-4"
              variant="secondary"
            >
              Fetch unlocked balance
            </Button>
          </CardFooter>
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