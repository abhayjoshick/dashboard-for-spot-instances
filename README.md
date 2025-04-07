
# ☁️ Spot Instance Analysis Dashboard

An interactive web-based dashboard built with **Streamlit** and **Plotly** to visualize, analyze, and derive insights from AWS Spot Instance data. The dashboard allows real-time file uploads, filtering, and advanced analytics including time series trends, regional heatmaps, predictive insights, and interruption risks.

---

## 🚀 Features

- 📊 **Real-Time Interactive Dashboard** via Streamlit  
- 📈 **Time Series Analysis**: Uptime trends, moving averages, peak interruption windows  
- 🌍 **Regional Insights**: Heatmaps, regional availability comparison  
- 💻 **Instance Type Performance**: Cluster comparison, cost efficiency (if data available)  
- 🤖 **Predictive Analytics** (optional): Forecast interruption likelihood or uptime trends  
- 🧠 **Correlation Insights**: Uptime vs Interruption frequency analysis  
- 🔍 **Interactive Filtering** by region, instance type, time range, etc.  
- 📤 **Upload Excel/CSV Data** for real-time visualization  
- 📎 **Download Reports** (Future enhancement)  

---

## 📂 Project Structure

```
dashboards-for-spot-instances/
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
└── README.md            # You're here!
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

If you're running locally and Plotly isn't installed, install it manually:

```bash
pip install plotly streamlit pandas openpyxl
```

---

### 2. ▶️ Run the App

```bash
streamlit run app.py
```

Then open the URL provided in your terminal (usually [http://localhost:8501](http://localhost:8501)).

---

### ☁️ Deployment on Streamlit Cloud

#### 1. Push Your Code to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

#### 2. Deploy

- Visit: [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Sign in with GitHub
- Click **"New App"**
- Select your GitHub repository
- Set `app.py` as the entry point
- Click **Deploy!**

---

## 📥 Upload Format

You can upload `.csv` or `.xlsx` files with the following fields:

| Column Name        | Description                                |
|--------------------|--------------------------------------------|
| `timestamp`        | Datetime of the instance event             |
| `region`           | AWS region (e.g., `us-west-1`)             |
| `instance_type`    | e.g., `t3.medium`, `m5.large`              |
| `uptime`           | Uptime in hours                            |
| `interruption_count` | Number of interruptions                  |

---

## 📊 Screenshots
![image](https://github.com/user-attachments/assets/99d4e0ac-2adb-42ba-88d4-88d9188519ba)
![image](https://github.com/user-attachments/assets/e0877bfe-e467-4335-b848-3b79efb9f677)
![image](https://github.com/user-attachments/assets/1ada2430-1044-48e4-ab8b-7d6d024be178)
![image](https://github.com/user-attachments/assets/f4d1240b-59cc-403a-9834-09f12bdbb4cc)
![image](https://github.com/user-attachments/assets/c1f1dec7-4e44-430d-98aa-de18adf19bdb)



_Add screenshots here as needed for illustration._

---

## 🛠️ To-Do / Enhancements

- Export visualizations and reports
- Add cost-based metrics (cost per uptime hour)
- Live alerts for risky instance types
- Integrate AWS pricing APIs

---

## 🧠 Contributing

Contributions welcome! Please fork the repository and create a PR with your enhancements or bugfixes.

---

## 📄 License

MIT License. Feel free to use and adapt.

> Built with ❤️ using Streamlit, Plotly, and Python.
