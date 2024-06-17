# Kogai

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900?logo=bitcoin)](https://twentyone.world)
[![Docker](https://img.shields.io/badge/docker-2496ED?&logo=docker&logoColor=white)](https://hub.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/krutt/kogai/blob/master/LICENSE)
[![Top](https://img.shields.io/github/languages/top/krutt/kogai)](https://github.com/krutt/kogai)
[![Languages](https://img.shields.io/github/languages/count/krutt/kogai)](https://github.com/krutt/kogai)
[![Size](https://img.shields.io/github/repo-size/krutt/kogai)](https://github.com/krutt/kogai)
[![Last commit](https://img.shields.io/github/last-commit/krutt/kogai/master)](https://github.com/krutt/kogai)

[![Kogai banner](static/kogai-banner.svg)](https://github.com/krutt/kogai/blob/master/static/kogai-banner.svg)

## Prerequisites

* python (3.8+) - High-level general-purpose programming language largely available on POSIX systems
* [pip](https://pypi.org/project/pip) - package installer for Python
* [poetry](https://python-poetry.org) - Python packaging and dependency management made easy
* [node](https://nodejs.org) - Run JavaScript Everywhere
* [pnpm](https://pnpm.io) - Fast, disk space efficient package manager
* [docker](https://docs.docker.com/get-docker) - Accelerated container application development
* [![Valknut](static/valknut.svg) aesir](https://github.com/aekasitt/aesir) - CLI used for setting up local Bitcoin &amp; Lightning regtest
* Web browser of choice (Chrome or Firefox)
  * [![Chrome Logo](static/chrome.svg) Chrome](https://www.google.com/chrome)
  * [![Firefox Logo](static/firefox.svg) Firefox](https://www.mozilla.org/en-US/firefox/new)
* Alby - Bitcoin Lightning Wallet & Nostr <sup>[*]</sup> 
  * [![Chrome Logo](static/chrome.svg) Add extension to Chrome](https://chromewebstore.google.com/detail/alby-bitcoin-wallet-for-l/iokeahhehimjnekafflcihljlcjccdbe)
  * [![Firefox Logo](static/firefox.svg) Add extension to Firefox](https://addons.mozilla.org/en-US/firefox/addon/alby/s)

<sup>*</sup>See why Alby and not Leather, Unisat or Xverse [here](#why-alby)

## Getting started

[![Kogai walkthru](static/kogai.gif)](https://github.com/krutt/kogai/blob/master/static/kogai.gif)

## Why Alby

The original intention for this project was to make scripting approachable to degens and plebs
alike. All the popular wallet extensions were tried but Alby for two main reasons. Alby wallet
extension can be switched to `regtest` network with ease and does not prominently steer its users
toward subscribing to blockchain data. Krutt encourages specifications for wallet extensions laid
out under the [WebBTC Specs](https://webbtc.dev)

### Anti-Patterns found in popular wallet extensions

* Prominent token promotion: While definitions for `Bitcoin L2` becomes more and more profitable to
  obscure, tokens like `STX` are not recognized largely as one. This prominent promotion in extension
  storefront and homepage incur choice-conundrum for users with lesser alternatives and is not
  encouraged by Krutt and team. Lightning with its long-standing history with Bitcoin does not incur
  the same cost as it is always encouraged for node-runners to attach their own sources of truths
  for blockchain data.
* API-reliance: All ordinals-focused wallet extensions rely on making API calls to individual API 
  servers preventing pure JSON-RPC calls to Bitcoin Nodes.
* Regtest not supported: This is a continuation for the previous fault. Due to heavy-reliance on API
  access, there can never be a singular `regtest` network.

## What Alby lacks (circa Jun 2024)

According to the [WebBTC Specs](https://webbtc.dev), it would be nice if `window.webbtc.sendPayment`
can also be implemented by Alby Wallet Extension as well. The current state of this sandbox requires
a hand-off to the server sending `0.1 BTC` to the lock contract and can be improved if `sendPayment`
is implemented according to the WebBTC specs.

## Contributions

## Disclosures

## License

This project is licensed under the terms of the MIT license.