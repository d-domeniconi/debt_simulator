# Investment Horizon Simulation with Debt Aquisition

A Python-based quantitative finance simulator for modeling long-term wealth accumulation under investment growth, recurring contributions, and debt acquisition scenarios.

The project explores questions such as:

- Is financing economically better than paying cash?
- When does leverage outperform delayed purchases?
- How much opportunity cost is created by buying assets upfront?
- How do investment returns compare against financing interest rates over long horizons?

The simulator combines:

- compound investment growth,
- increasing monthly contributions,
- debt amortization,
- maintenance costs,
- and comparative wealth trajectory analysis.

---

## Features

- Monthly compound wealth simulation
- Annual-to-monthly rate conversion utilities
- Progressive monthly contribution growth
- Standard, fixed-payment, amortized loan model (Price/French system).
- Debt/financing modeling
- Wealth trajectory visualization
- Comparison between:
  - paying cash,
  - financing,
  - delayed acquisition,
  - and investment-first strategies

---

## Mathematical Model

The simulator models wealth evolution as:

```math
P[t]=P_0(r_m)^t+A_m(r_m^{t+1} - m_m^{t+1})
```

Where:

- $P_0$: initial wealth
- $A_m$: monthly contribution
- $r_m$: effective monthly investment return
- $m_m$: effective monthly contribution growth rate
- $t$: time horizon in months

Monthly contributions grow over time:

```math
A[t+1]=A[t](m_m)^{t+1}
```

Where:

- $A[t=0]$: initial monthly contribution

Annual rates are converted into equivalent monthly rates internally.

Debt is modeled by the core formula:

```math
V_p = (V_v-E)\frac{J_m-1}{1-J_m^{-n}},
```

which is an adaptation of the French system, where:

- $V_p$: installment payment
- $V_v$: asset's value
- $E$: loan's down payment
- $J_m$: effective monthly interest rate
- $n$: number of installments

OBS: each effective rate is defined as $(1+rate)$

## Installation

Clone the repository:

```bash
git clone https://github.com/d-domeniconi/debt_simulator.git
cd debt_simulator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run in Google Colab

The notebook can also be executed directly in Google Colab without local installation:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/d-domeniconi/debt_simulator/blob/main/debt_simulator.ipynb)

## Example Usage

### Import modules

```python
import src.equity as eq
import src.loan as loan
import src.vis as vis
```

### Convert annual rates to monthly rates

```python
r = 1.10  # annual investment return
m = 1.05  # annual contribution growth

rm = eq.anual_para_mensal(r)
mm = eq.anual_para_mensal(m)
```

### Simulate wealth accumulation

```python
patrimonio = eq.patrimonio_puro(
    patrimonio_inicial=40000,
    aporte_mensal=270,
    rendimento_mensal=rm,
    aumento_aporte_mensal=mm,
    meses=120
)
```

---

## Example Scenario

The simulator can compare:

- buying an asset in cash,
- financing the asset,
- investing available capital instead,
- and evaluating long-term net worth differences.

This allows analysis of leverage efficiency under different return and interest-rate assumptions.

---

## Future Improvements

Planned extensions include:

- Monte Carlo simulations
- Inflation-adjusted returns
- Variable interest-rate financing
- Tax modeling
- Portfolio volatility
- Probabilistic income growth
- Interactive dashboards
- Risk-adjusted performance metrics

---

## Motivation

Most personal finance tools treat debt as universally harmful (either that or as the solution to all your problems).

This project instead approaches debt quantitatively:

> Debt is neither good nor bad by itself — its value depends on opportunity cost, investment returns, financing rates, and time horizon.

The simulator was developed to study these tradeoffs rigorously.

---

## License

MIT License
