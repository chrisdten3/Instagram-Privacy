# 📌 Instagram Privacy Data Processor

## 🔍 Overview
Instagram allows users to **download their personal data** as a JSON archive, which contains detailed information about their **advertisers, account activity, posts, location history, and more**. This project **analyzes and summarizes** that data to provide insights into your Instagram privacy.

Instead of simply displaying raw JSON data, this tool **highlights key privacy-related insights**, including:

✅ The number of **advertisers** that have access to your information  
✅ Which advertisers **know you've visited them in person**  
✅ A **visualization** of the IP addresses from your login history  
✅ A **timeline of posts you've viewed**  
✅ A list of **recently viewed products** and **recommended topics**  

This tool helps users better understand how their data is being used and who has access to their online activity.

---

## 📂 Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/chrisdten3/instagram-privacy.git
cd instagram-privacy
```

### **2️⃣ Prepare Your Instagram Data**
- **Download** your Instagram archive from [Instagram's Data Download page](https://www.instagram.com/download/request/)  
- **Unzip the archive** and place the entire folder inside the cloned repository  
- **Rename the folder** to **`instagram`**  

### **3️⃣ Install Dependencies**
Make sure you have **Python 3.x** installed, then run:
```bash
pip install -r requirements.txt
```

### **4️⃣ Convert the Data into a Usable Format**
Run the conversion script to merge all Instagram JSON files into a single report:
```bash
python convert.py
```
This will generate **`new_merged.json`**, which will be used for analysis.

### **5️⃣ Launch the Streamlit Web Application**
```bash
streamlit run app.py
```
- Upload the **`new_merged.json`** file when prompted  
- View **interactive charts, tables, and maps** summarizing your Instagram data  

---

## 🔍 Key Information Extracted

### **📢 Advertiser Insights**
- Total **number of advertisers** that have access to your data  
- Advertisers that **use custom data audiences**  
- Advertisers that **know you've visited them in person**  

### **📊 Post & Activity Tracking**
- Total **number of posts viewed**  
- A **timeline graph** showing when you viewed posts  

### **🌍 Location & IP Tracking**
- A **map of login activity** (based on IP addresses)  
- Hover over points to see **timestamps & device information**  

### **🛍️ Shopping & Interests**
- List of **recently viewed products**  
- List of **recommended topics Instagram thinks you're interested in**  

---

## 🎨 Design & Visualization Choices
I chose **Python + Streamlit** for this project because:
✅ **Streamlit provides an easy-to-use interface** for interactive data visualization  
✅ **Pydeck's map integration** makes it easy to visualize login activity  
✅ **Pandas & Matplotlib** efficiently handle and summarize large amounts of data  

**Limitations of our choices:**  
⚠️ **Data accuracy depends on Instagram's archive** – some insights (like in-person visits) are only available if Instagram collects them  
⚠️ **Geolocation is approximate** – IP addresses may not always correspond to actual locations  
⚠️ **Requires a manual upload** – Users must download and unzip their data before running the tool  

---

## 🎯 Why This Information Matters
I focused on **advertiser tracking, login activity, and user engagement** because:
🔹 **Privacy Awareness** – Many users don’t realize how many advertisers have access to their information  
🔹 **Security** – Tracking IP login history can help users spot unauthorized logins  
🔹 **Data Profiling** – The "Recommended Topics" and "Recently Viewed Products" sections show how Instagram builds a **personalized profile** of users  

Understanding these insights empowers users to **take control of their online privacy** and adjust their **Instagram settings accordingly**.

---

## 🤝 Contributors
Made by Christopher Tengey for COSC 3720

