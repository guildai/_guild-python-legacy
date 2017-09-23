---
layout: docs
title: Installation
description: Setup for Guild AI
group: getting-started
---

Follow the steps below to install and configure Guild AI on your system.

## Contents

* Will be replaced with the ToC
{:toc}

## Requirements

### Python

Guild AI currently requires Python 2.7 or Python 3.

### TensorFlow

Guild AI requires TensorFlow version {{site.tensorflow_min}} or
later. Some projects may require later versions of TensorFlow ---
refer to the documentation for each project to confirm you have a
compatible version of TensorFlow installed.

Refer to {% link https://www.tensorflow.org/install/ %}Installing
TensorFlow{% endlink %} for instructions on installing TensorFlow on
your system. If your system does not have a GPU, or you're not sure,
select the non-GPU version of TensorFlow. You can upgrade to the GPU
version later if you need to.

### nvidia-smi

Guild uses {% link
https://developer.nvidia.com/nvidia-system-management-interface
%}NVIDIA System Management Interface{% endlink %} to collect GPU
statistics. If your system has an NVIDIA GPU, we recommend installing
this utility to extend the data Guild collects for your model.

To install `nvidia-smi` install the latest CUDA toolkit from this location:

{% link https://developer.nvidia.com/cuda-downloads
%}https://developer.nvidia.com/cuda-downloads{% endlink %}

## Installing using pip

{% term %}
$ sudo pip install guildai
{% endterm %}

## Check your installation

Once Guild AI is installed, confirm that it's installed correctly by
running:

{% term %}
$ guild check
{% endterm %}

You should see details about the Guild installation. If you get any
errors, please report them on {% ref github-issues %} to get
assistance.

{% next /getting-started/quick-start/ %}Next: Start using Guild{% endnext %}
