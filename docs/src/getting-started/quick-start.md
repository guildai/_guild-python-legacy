---
layout: docs
title: Quick start
description: A short tutorial to introduce Guild AI's basic features.
group: getting-started
---

After [installing Guild](/getting-started/setup/), follow these steps
to quickly become familiar with its features.

## Contents

* Will be replaced with the ToC
{:toc}

## Train MNIST softmax regression

{% term %}
$ guild train mnist
{% endterm %}

If you are running this command for the first time, Guild will install
the MNIST softmax regression model and train it using the MNIST
dataset of handwritten digit charaters.

The softmax regression model is very simple and will train on most
systems within a minute or two. As the model is trained Guild will
print training progress.

## View training results

Start Guild View:

{% term %}
$ guild view
{% endterm %}

Open Guild View in your browser by navigating to {% link
http://localhost:6333 %}http://localhost:6333{% endlink %}.

Guild View provides an advanced visual interface for viewing training
and evaluation results and compare runs to select the best trained
model for your application.

Note the

## Train MNIST CNN



## Next steps

{% next /features/ %}Read more about Guild features{% endnext %}
{% next /examples/ %}Browse Guild examples{% endnext %}
{% next /tutorials/integrating-guild-with-your-project/ %}Integrate Guild with your project{% endnext %}
{% next /tutorials/using-guild-to-serve-models/ %}Run the expert MNIST model as a web service{% endnext %}
