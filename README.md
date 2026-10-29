# 💻 Laptop Price AI Predictor

A browser-based machine learning application that estimates laptop prices using **Ridge Regression** trained on 1,303 historical laptop records. The application uses HTML, CSS, and JavaScript to generate predictions directly in the browser without requiring an external prediction API.

> **Note:** Predictions are estimates based on historical data, not guaranteed current market prices.

## ✨ Features

- 🤖 Machine learning-based laptop price estimation.
- 💻 Browser-based interface built with HTML, CSS, and JavaScript.
- 📊 Model trained on 1,303 laptop records.
- 🧮 Ridge Regression with engineered hardware features.
- 📱 Responsive interface for different screen sizes.
- ⚡ Predictions calculated locally in the browser.
- 📈 Model evaluation using R² and Mean Absolute Percentage Error (MAPE).

## 📂 Dataset

| Property | Details |
|---|---|
| Dataset | Laptop Price Dataset |
| Source | Kaggle |
| Original data source | idealo.de |
| Original scrape year | 2019 |
| Number of records | 1,303 |
| Currency | Indian Rupees (INR) |
| Missing values | 0 |
| Target variable | Laptop price |

The dataset includes laptop specifications such as company, product type, screen size, processor, RAM, storage, graphics card, operating system, weight, and price.

### ⚠️ Dataset limitation

The dataset originates from 2019. Therefore, the model may not accurately reflect current laptop prices because of inflation, new hardware generations, and changes in the laptop market.

## 🧠 Machine Learning Model

The application uses Ridge Regression on the logarithm of laptop prices.

| Property | Value |
|---|---|
| Algorithm | Ridge Regression |
| Target transformation | Natural logarithm of price |
| Regularization parameter | λ = 0.01 |
| Train/test split | 80/20 |
| Random seed | 42 |
| Reported test R² | 0.826 |
| Reported test MAPE | 20.8% |

*The reported metrics should be reproducible using the training script and the same dataset.*

### Engineered features

The model uses features representing:

- RAM capacity.
- Storage capacity and storage type.
- Screen resolution.
- Processor tier and base clock speed.
- Graphics processing capability.
- Screen size.
- Laptop weight.
- Laptop manufacturer, product type, and operating system.

The feature extraction and encoding used by the training script must match the calculations performed by the browser application.

## 🛠️ Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Machine Learning:** Ridge Regression
- **Training:** Python
- **Model integration:** JSON coefficients
- **Dataset:** CSV
- **Optional local server:** Node.js

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AyushBaluni/Laptop-price-ai-predictor.git
cd Laptop-price-ai-predictor
```

### 2. Run the application

If `index.html` is in the repository root, open it directly in your browser.

Alternatively, start a local HTTP server:

```bash
python -m http.server 8080
```

Then visit:

http://localhost:8080/

### 3. Retrain the model

If Python is installed, run:

```bash
python train_model.py
```

The script should generate or update the model coefficient file according to its implementation.

### 4. Verify the model

Run:

```bash
python verify_model.py
```

This runs the checks implemented in the verification script.

## 📁 Project Structure

The structure below is illustrative. Keep only filenames that actually exist in the repository.

```text
Laptop-price-ai-predictor/
├── index.html
├── laptop_price.csv
├── train_model.py
├── verify_model.py
├── inspect_data.py
├── model_coeffs.json
├── server.js
├── requirements.txt
├── qa_full.mjs
├── screenshot_result.png
└── README.md
```

## 📊 Model Evaluation

The current implementation reports the following results:

| Metric | Reported result |
|---|---:|
| Test R² | 0.826 |
| Test MAPE | 20.8% |

R² measures how much of the variation in the test-set prices is explained by the model. MAPE measures average absolute prediction error relative to actual prices.

These metrics describe performance on the historical test dataset and do not guarantee equivalent accuracy on today's laptop market.

## 🔮 Future Improvements

- Train and evaluate the model using a more recent laptop price dataset.
- Compare Ridge Regression against Random Forest and Gradient Boosting.
- Improve validation across different price ranges.
- Add laptop configuration comparison.
- Improve the user interface and accessibility.
- Add model performance visualizations.
- Introduce a statistically justified prediction interval.

## ⚠️ Disclaimer

This application provides machine learning-based estimates using historical laptop pricing data. Actual prices may vary depending on the model, configuration, seller, location, availability, and date of purchase.

Always check current retailer prices before making a purchasing decision.

## 👨‍💻 Author

**Ayush Baluni**

GitHub: https://github.com/AyushBaluni

---

⭐ If you find this project useful, consider starring the repository.
