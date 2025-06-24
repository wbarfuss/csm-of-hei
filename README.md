These lecture notes provide an integrated perspective on different modeling approaches (dynamics, equilibrium, and agent-based) applied to human-environment interactions and sustainability transitions. Its scope is practical, utilizing Python within Jupyter Notebooks. Prerequisites are basic mathematical skills.

This is version 0.1. To be updated and improved.

## Learning goals

After **working** through all materials, 

* students can **model** *human-environment interactions* <br>to answer relevant questions in sustainability science.
* students can **implement** *models of human-environment interactions* <br> in the
general-purpose computer language **Python**.
* students can critically **evaluate** *models of human-environment interactions* <br>to judge their
relevance to issues in sustainability science.

## Integrated writing

The following steps are entirely optional for readers who want to focus on the learning goals and are not interested in the development of these lecture notes.

These lecture notes are written in [Jupyter](https://jupyter.org) Notebooks, which are a popular format for interactive computing. Notebooks contain code, math, and text. The code is written in [Python](https://www.python.org), a general-purpose programming language widely used in scientific computing and other fields.

Scholarly writing practices, such as citations and cross-references, are facilitated by [Quarto](https://quarto.org), a powerful scientific and technical publishing system. Quarto also allows you to view these lecture notes in various formats, such as HTML and PDF. 


Assuming you have installed the [Quarto CLI](https://quarto.org/docs/get-started/), you can render these lecture notes by running the following command in the terminal:

```{python}
#| output: false
!quarto render .
```

The comment `#| output: false` is a Quarto directive that prevents the output of this cell from being displayed in the rendered documents. This is useful for keeping these readable.

These lecture notes are made open-source and hosted in a GitHub repository. To convert this `index.ipynb` file (which is required in the Quarto Book project type) into the repository's README file, one may execute the following commands:

```{python}
!quarto convert index.ipynb # convert into Quarto markdown
!tail -n +10 index.qmd > README.md  # remove some metadata+
!rm index.qmd  # remove the intermediate file
```

## Acknowledgements
I am grateful to all the students I had the pleasure of working with on this material. Their feedback has been, is, and will continue to be essential for shaping this content. I would also like to thank my teachers and mentors, who have influenced my thinking. I am thankful to all contributors and creators of the many open-source projects these notes build upon, such as the Python language and its ecosystem, Jupyter, and Quarto. Furthermore, I acknowledge many helpers who may use some form of generative AI, such as ChatGPT, Perplexity, GitHub Copilot, and Grammarly. All remaining errors remain my own.

