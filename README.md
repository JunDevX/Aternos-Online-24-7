## Languages
English [Russian](https://github.com/JunDevX/Aternos-Online-24-7/blob/main/README-ru.md)
# Aternos-Online-24-7

![Node.js](https://img.shields.io/badge/Node.js-18.x-green?logo=node.js)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Made in Russia](https://img.shields.io/badge/Made%20in-Russia-red?logo=russia)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview
This repository provides a hybrid **Node.js + Python** automation tool designed to keep your **Aternos Minecraft server online 24/7**.  
The system periodically connects to the server, preventing automatic shutdown due to inactivity.

## Features
- Continuous 24/7 uptime for Aternos servers  
- Hybrid architecture: Node.js for control logic, Python for automation  
- Automatic reconnection and session handling  
- Modular structure and easy configuration  
- CLI-based control for quick setup and monitoring  

## Technologies Used
- **Node.js** — main controller, scheduler, logging  
- **Python** — automation routines, session/browser emulation  
- **Puppeteer / Selenium** (optional depending on setup)  
- **dotenv** for environment configuration  

## Installation
```bash
git clone https://github.com/JunDevX/Aternos-Online-24-7.git
cd Aternos-Online-24-7
npm install
pip install -r requirements.txt
```
