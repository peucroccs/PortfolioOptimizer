<div align="center">

# Portfolio Optimization using Markowitz Theory

Construção e otimização de portfólios utilizando a Teoria Moderna do Portfólio (MPT) de Harry Markowitz para maximizar retorno ajustado ao risco.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-orange)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-red)

</div>

---

## 📋 Table of Contents

* [About The Project](#about-the-project)
* [Methodology](#methodology)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Installation](#installation)
* [Usage](#usage)
* [Results](#results)
* [Future Improvements](#future-improvements)
* [References](#references)

---

## About The Project

The goal of this project is to determine the optimal allocation of assets in a portfolio using the Modern Portfolio Theory (MPT) proposed by Harry Markowitz in 1952.

The optimization process is based on key portfolio metrics, including:

- Expected Return
- Risk (Volatility)
- Sharpe Ratio

By combining these metrics, the model identifies the portfolio with the highest Sharpe Ratio, providing the best risk-adjusted return among the available asset allocations.

---

## Theory Behind

According to Modern Portfolio Theory (MPT), a portfolio is defined by its expected return and risk.

### Expected Return

$$
E(R_p) = \sum_{i=1}^{n} w_i R_i
$$

Where:
- $w_i$ = weight of asset $i$
- $R_i$ = expected return of asset $i$

---

### Portfolio Volatility

$$
\sigma_p = \sqrt{w^T \Sigma w}
$$

Where:
- $w$ = vector of weights
- $\Sigma$ = covariance matrix

---

### Sharpe Ratio

$$
SR = \frac{E(R_p) - R_f}{\sigma_p}
$$

Where:
- $R_f$ = risk-free rate

---

### Optimization Objective

$$
\max_w \frac{E(R_p) - R_f}{\sigma_p}
$$

Subject to:

$$
\sum_{i=1}^{n} w_i = 1
$$

$$
w_i \geq 0
$$

---

## Project Structure

```text
portfolio-optimization/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── results/
│   ├── plots/
│   ├── weights/
│
│
├── notebooks/
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── metrics_calc.py
│   ├── optimization.py
│   └── visualization.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies

* Python
* Pandas
* NumPy
* SciPy
* Matplotlib
* Seaborn
* yFinance

---

## Installation


---

## Usage


---

## Results

### Efficient Frontier


### Optimal Portfolio Allocation


### Portfolio Metrics


---

## Future Improvements


---

## References


---

## Author

