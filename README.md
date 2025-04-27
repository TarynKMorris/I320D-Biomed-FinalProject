# Modeling Discontent: An Agent-Based Approach to Social Contagion

---

**Contributors:** Taryn Morris, Shamiya Lin Naomi Ichiriu
School of Information, The University of Texas at Austin
I 320D: Data Science for Biomedical Informatics

---

## Overview
This project simulates the spread of visible discontent within a population using an agent-based model (ABM) based on social contagion theory.

The simulation addresses:
- Why individuals engage in collective action despite personal risks.
- How protest dynamics vary across political and social environments.
- How external factors such as media signals, peer influence, and perceived cost shape the success or suppression of movements.

Developed for **I320D: Data Science for Biomedical Informatics** at the University of Texas at Austin.

---

## Background
Social movements emerge when dissatisfaction among individuals exceeds personal thresholds, fueled by peer influence, media signals, and perceptions of efficacy and risk.  
Drawing on sociology, psychology, and network science, this project models the underlying mechanisms of protest diffusion, with inspirations from events such as the Black Lives Matter movement and the Candlelight Revolution.

---

## Key Variables

| Variable                  | Definition                                                  |
|----------------------------|-------------------------------------------------------------|
| `discontent`               | Core dissatisfaction level (0–1 scale)                      |
| `_freedom_threshold_`      | *How much discontent is needed to act*                      |
| `burnout`                  | Reduces likelihood to protest after repeated effort         |
| `homophily_score`          | How similar neighbors are (affects influence)               |
| `media_signal`             | External signal from -1 (discourage) to +1 (mobilize)        |
| `perceived_cost`           | Risk or social cost of participating                        |
| `efficacy`                 | Belief that protest leads to change                         |
| `confirmation_bias`        | How much opposing views are ignored                         |
| `influence_from_network`   | Average protest level among visible peers                   |

Sources:  
Landgeist (2021) — Global Freedom Index Map  
Özçetin (2024) — World Press Freedom Report

---

## Project Workflow

1. **Network Initialization**
   - Generate a random or scale-free network.
   - Assign behavioral parameters to each individual node.

2. **Simulation Propagation**
   - Agents update their visible discontent based on peer influence, media signals, perceived costs, and personal thresholds.
   - Dynamic feedback loops capture burnout and confirmation bias over time.

3. **Visualization and Analysis**
   - Plot network structure and protest diffusion across time steps.
   - Track participation rates, cluster sizes, and tipping points.

---

## Features

- **Agent-Based Modeling**
  - Models dynamic decision-making based on neighbor behavior and external signals.
  - Captures individual heterogeneity across political freedoms, efficacy beliefs, and media environments.

- **Streamlit Interactive Application**
  - Adjustable parameters such as number of nodes, average node degree, media intensity, and homophily levels.
  - Real-time visualization of protest spread across networks.
  - Publicly available at: [https://network-sim.streamlit.app/](https://network-sim.streamlit.app/)

- **Modular Codebase**
  - `network_sim.py` handles network generation and simulation logic.
  - `simulations.py` presents the Streamlit-based interactive interface.

---

## Research Questions
- Under what network and individual conditions do protests succeed in reaching critical mass?
- How does social homophily influence mobilization speed and scale?
- What role does media encouragement or suppression play in sustaining movements?
- Can protest outcomes be predicted early based on network dynamics?

---

## Future Work
Future extensions of this project could involve incorporating real-world demographic, political, and socioeconomic attributes into the agent profiles, allowing simulations to more closely mirror actual societies. Geographic clustering could be added to simulate the localized diffusion of protests across cities or regions rather than in abstract networks alone. Another avenue for improvement is integrating real-time sentiment analysis from social media platforms, dynamically updating media signals in the model to better reflect evolving public moods. Finally, to validate and refine the simulation’s predictive accuracy, the model could be benchmarked against historical case studies of protest movements such as the Arab Spring, Occupy Wall Street, or the South Korean Candlelight Revolution. These enhancements would enable a richer and more nuanced understanding of how collective action emerges and sustains itself across different contexts.

---

## References

- Apollonio, N., Blankenberg, D., Cumbo, F., Franciosa, P. G., & Santoni, D. (2023). *Evaluating homophily in networks via HONTO*. Bioinformatics, 39(1), btac763. [https://doi.org/10.1093/bioinformatics/btac763](https://doi.org/10.1093/bioinformatics/btac763)

- CNN. (2020, June 2). *Police protests use of force*. [https://www.cnn.com/2020/06/02/us/police-protests-use-of-force/index.html](https://www.cnn.com/2020/06/02/us/police-protests-use-of-force/index.html)

- Granovetter, M. (1978). *Threshold Models of Collective Behavior*. American Journal of Sociology, 83(6), 1420–1443. [http://www.jstor.org/stable/2778111](http://www.jstor.org/stable/2778111)

- Kim, E., & Choo, C. (Directors). (2022). *Candlelight Revolution* [Film]. STUDIO JUGIZA. [https://mubi.com/en/us/films/candlelight-revolution](https://mubi.com/en/us/films/candlelight-revolution)

- Landgeist. (2021). *Global Freedom Index 2021*. [https://landgeist.com/2021/03/08/global-freedom-index-2021/](https://landgeist.com/2021/03/08/global-freedom-index-2021/)

- Life Matters. (n.d.). *Crowd of protesters holding signs* [Photograph]. Pexels. [https://www.pexels.com/photo/crowd-of-protesters-holding-signs-4614165/](https://www.pexels.com/photo/crowd-of-protesters-holding-signs-4614165/)

- Masferrer, A. (2023). *The decline of freedom of expression and social vulnerability in Western democracy*. International Journal for the Semiotics of Law, 1–33. [https://doi.org/10.1007/s11196-023-09990-1](https://doi.org/10.1007/s11196-023-09990-1)

- Nout. (n.d.). *Crowd of people black and white photo* [Photograph]. Pexels. [https://www.pexels.com/photo/crowd-of-people-black-and-white-photo-2246258/](https://www.pexels.com/photo/crowd-of-people-black-and-white-photo-2246258/)

- Özçetin, B. (2024). *Digital dissent and online counterpublics in Turkey: A discursive analysis of the #MeToo movement*. Journal of Ethnic and Migration Studies. [https://doi.org/10.1177/13634615241296292](https://doi.org/10.1177/13634615241296292)

- ResearchGate. (n.d.). *Infection patterns in simple and complex contagion processes on networks*. [https://www.researchgate.net/figure/Simple-contagion-Toy-network-illustrating-the-asymmetry-of-the-infection-pattern-and-its_fig2_381309142](https://www.researchgate.net/figure/Simple-contagion-Toy-network-illustrating-the-asymmetry-of-the-infection-pattern-and-its_fig2_381309142)

- Spiske, M. (n.d.). *Crowd of protesters under gray overcast sky* [Photograph]. Pexels. [https://www.pexels.com/photo/crowd-of-protesters-under-gray-overcast-sky-4977014/](https://www.pexels.com/photo/crowd-of-protesters-under-gray-overcast-sky-4977014/)

- Zhan, C., Zheng, Y., Lai, Z., et al. (2021). *Identifying epidemic spreading dynamics of COVID-19 by pseudocoevolutionary simulated annealing optimizers*. Neural Computing and Applications, 33, 4915–4928. [https://doi.org/10.1007/s00521-020-05285-9](https://doi.org/10.1007/s00521-020-05285-9)
