# AI.OS // Identity Terminal

```console
vrathik@aios:~$ sudo systemctl start ai.os
```

<p align="left">
  <img src="assets/boot.gif" alt="AI.OS boot sequence: POST, kernel, CUDA, neural engine, system ready" width="440" />
</p>

```console
vrathik@aios:~$ login vrathik
Authenticating... identity verified. Rendering portrait.
```

<p align="left">
  <img src="assets/portrait.gif" alt="ASCII portrait of Vrathik Shenoy resolving from edge-detection to full render" width="380" />
</p>

---

```console
vrathik@aios:~$ whoami
vrathik

vrathik@aios:~$ id
uid=1000(vrathik) gid=1000(engineer) groups=1000(engineer),27(sudo),44(computer-vision),46(generative-ai),108(diffusion),120(mlops)

vrathik@aios:~$ hostnamectl
   Static hostname: aios
         Icon name: computer-workstation
  Operating System: AI.OS 2.0 "Latent Space"
            Kernel: Linux 6.13-neural-cuda
      Architecture: x86-64 · CUDA sm_90
          Hardware: Vrathik Shenoy — AI Engineer
             Focus: Computer Vision & Generative AI
            Status: ● Building Wearify
         Last Sync: <!-- SYNC_TIME_START -->System Sync: 2026-07-15 11:39:57 UTC (Active)<!-- SYNC_TIME_END -->

vrathik@aios:~$ cat /etc/motd
  Initializing Human Intelligence... loading Artificial Intelligence...
  Welcome, Vrathik Shenoy.

  Bridging cutting-edge computer vision research and production:
  optimizing latent diffusion models, accelerating tensor
  computations, and engineering virtual try-on ecosystems.
```

---

```console
vrathik@aios:~$ tree ~ -L 1
/home/vrathik
├── about/          # whoami — background & mission
├── projects/       # systemctl status <service>
├── research/       # journalctl --unit research
├── startup/        # docker ps — shipping containers
├── experiments/    # ongoing R&D
├── github/         # htop — live system stats
└── contact/        # cat ~/.ssh/config

7 directories
```

---

```console
vrathik@aios:~$ pacman -Q | grep -E 'ml|ai|vision|gpu'
python 3.12
pytorch 2.5
cuda 12.6
opencv 4.13
transformers 4.x
diffusers 0.x
triton 3.x
nextjs 15
docker 27

vrathik@aios:~$ cat /proc/skills
[EXPERT]    Computer Vision · PyTorch · CUDA · OpenCV
[ADVANCED]  Latent Diffusion · Model Optimization · Python
[LEARNING]  VLMs · Triton Kernels · MLOps · Next.js
```

---

```console
vrathik@aios:~$ systemctl status wearify.service
● wearify.service - Virtual Try-On Synthesis Engine
     Loaded: loaded (/etc/systemd/system/wearify.service; enabled)
     Active: active (running) since 2025 — production
   Main PID: 1337 (wearify)
      Stack: Python · PyTorch · CUDA · Next.js
       Repo: https://github.com/vrathikshenoy/wearify
     CGroup: /system.slice/wearify.service
             └─ high-fidelity garment transfer onto target person models
             └─ diffusion-based drape synthesis + body landmark alignment

vrathik@aios:~$ systemctl status gemini-vton.service
○ gemini-vton.service - Multi-modal Try-On (Gemini)
     Loaded: loaded (/etc/systemd/system/gemini-vton.service; disabled)
     Active: inactive (dead) — archived
      Stack: Python · Gemini API · Bun · Tailwind
       Repo: https://github.com/vrathikshenoy/gemini-vton
     CGroup: agentic multimodal try-on pipeline powered by Gemini
```

---

```console
vrathik@aios:~$ journalctl --unit research -n 5 --no-pager
research[vton]:       drape deformation & synthesis — optimizing
research[diffusion]:  latent diffusion — inference speed & parameter efficiency
research[fashion]:    high-precision human parsing & body landmark alignment
research[vit]:        attention maps in diffusion guidance
research[multimodal]: VLM alignment for commercial usage
```

---

```console
vrathik@aios:~$ docker ps
CONTAINER ID   IMAGE              STATUS         PORTS      NAMES
a1b2c3d4e5f6   wearify/api        Up 8 months    :8000      api
f6e5d4c3b2a1   wearify/frontend   Up 8 months    :3000      frontend
9z8y7x6w5v4u   wearify/worker     Up 8 months    (gpu)      worker
1a2b3c4d5e6f   wearify/model      Up 8 months    :5000      model-server
```

---

```console
vrathik@aios:~$ htop
```

<p align="left">
  <img src="assets/ai_terminal.svg" alt="AI.OS live system monitor showing running neural processes" width="440" />
</p>

<p align="left">
  <img src="https://github-readme-stats.vercel.app/api?username=vrathikshenoy&show_icons=true&theme=dark&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&icon_color=39d0ff&border_color=30363d&hide_title=false" alt="Vrathik's GitHub statistics" width="410" />
  &nbsp;&nbsp;
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=vrathikshenoy&layout=compact&theme=dark&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&border_color=30363d" alt="Vrathik's most used languages" width="290" />
</p>

---

```console
vrathik@aios:~$ git log --graph --oneline --all
* 2026  scale ai products (HEAD -> main, active node)
* 2025  wearify & vton engine development
* 2024  deep generative research — diffusion & pytorch
* 2023  computer vision specialization
* 2022  started ai journey (root commit)
```

<p align="left">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=vrathikshenoy&theme=github-compact&bg_color=0d1117&color=58a6ff&line=39d0ff&point=a371f7&area=true&hide_border=true" alt="Vrathik's contribution activity graph" width="740" />
</p>

---

```console
vrathik@aios:~$ cat ~/.ssh/config
Host github
    User        vrathikshenoy
    HostName    github.com/vrathikshenoy

Host linkedin
    HostName    linkedin.com/in/vrathik-shenoy

Host email
    HostName    shenoyvrathik@gmail.com
```

---

```console
vrathik@aios:~$ sudo rm -rf /
rm: it is dangerous to operate recursively on '/'
Permission denied. Nice try :)

vrathik@aios:~$ make startup
Building MVP...       [####------] 40%
Still debugging...    ▓▓▓▒▒▒
make: shipping anyway.

vrathik@aios:~$ ai --future
generating................
> Building AI products that solve real-world problems.
```

---

```console
vrathik@aios:~$ fortune -ai
```

<!-- QUOTE_START -->
```
"The question is not whether machines think but whether men do." — B.F. Skinner
```
<!-- QUOTE_END -->

```console
vrathik@aios:~$ sudo poweroff
[  OK  ] Stopping Neural Engine...
[  OK  ] Saving Session State...
[  OK  ] Unmounting /dev/vton...
[  OK  ] Flushing tensor cache...

Goodbye, traveler.
```

<p align="left">
  <b>█</b>
</p>
