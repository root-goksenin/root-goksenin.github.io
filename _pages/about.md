---
layout: about
title: about
permalink: /
subtitle: PhD candidate in machine hearing · <a href='https://www.ru.nl/donders/'>Donders Institute</a>, Radboud University · Nijmegen, the Netherlands

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Donders Institute for Brain, Cognition and Behaviour</p>
    <p>Radboud University</p>
    <p>Nijmegen, the Netherlands</p>
    <p>Dutch citizen (EU)</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
---

I'm a PhD candidate in AI at the [Donders Institute](https://www.ru.nl/donders/), Radboud University, advised by Kiki van der Heijden and Marcel van Gerven, and a member of the ELLIS Unit Nijmegen. I work on **machine hearing**: teaching machines to understand sound scenes the way people do, both what they hear and where it comes from. My research combines **representation learning** with **(spatial) audio**, building self-supervised audio foundation models that hold up in real, noisy and reverberant environments, and extends to **spatial audio large language models**.

Most audio foundation models are trained on single-channel audio and are effectively "spatially blind." My work closes this gap. **AudioSphere** (NeurIPS 2026) is the first self-supervised audio model to perform sound event localization and detection from a frozen backbone, and it works across microphone array geometries without retraining. **Bearings** learns soundfield embeddings that plug into frozen single-channel audio encoders without retraining, and **EquiSELD** makes rotation-equivariant localization networks efficient to train. **GRAM** learns spatial representations in binaural and Ambisonics formats. I also build open benchmarks (NatHEAR, RealSELD) for evaluating audio models in noisy, reverberant scenes.

My work extends to speech representation learning. **SpeechJEPA** learns speech representations entirely in latent space, without the clustering that earlier speech JEPAs relied on. Trained in 64 GPU-hours, it outperforms wav2vec 2.0, HuBERT and WavLM at every labeled-data budget for speech recognition. **WavJEPA** applies the same kind of semantic learning to general-purpose audio, straight from raw waveforms. I train these models on Snellius, the Dutch national supercomputer, with three compute grants totaling 3 million SBUs (about 15,000 H100 GPU-hours). Code and models are on the [HAMLET lab GitHub](https://github.com/labhamlet), my [personal GitHub](https://github.com/root-goksenin) and [Hugging Face](https://huggingface.co/labhamlet).

Before my PhD, I worked at [ScreenPoint Medical](https://screenpoint-medical.com/) as a software engineer on large-scale medical AI software. During a research internship there, I developed an MRI segmentation pipeline for breast density estimation, which led to a first-author paper at MIDL 2024. During my bachelor's, I interned as a data scientist at [Arcadis](https://www.arcadis.com/), building machine learning dashboards for housing price analysis and EV charging placement. I hold an MSc in AI from the University of Amsterdam and a BSc in AI from Radboud University.

**I'm looking for research internships for 2027 in machine hearing, audio and speech representation learning, or spatial audio.** Feel free to reach out by [email](mailto:goksenin.yuksel@donders.ru.nl).
