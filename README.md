## 📉 Problem Statement
Electric Vehicle (EV) battery packs are highly sensitive to thermal runaway and voltage imbalances. Standard BMS systems often lack a user-friendly interface for remote monitoring. This project bridges that gap by providing a real-time, AI-ready dashboard that allows engineers to monitor pack health from anywhere, preventing catastrophic failures through predictive alerts.

## 🔌 Circuit Logic & Pin Mapping
To ensure accurate data acquisition, the following hardware configuration is utilized:

| Component | ESP32 Pin | Logic |
| :--- | :--- | :--- |
| **Voltage Divider** | GPIO 34 (ADC1) | Scales 0-8.4V (2S battery) to 0-3.3V range for ESP32. |
| **LM35 Sensor** | GPIO 35 (ADC1) | Linear output of 10mV/°C for precise thermal tracking. |
| **Status LED** | GPIO 2 | Blinks during WiFi data transmission sync. |



## 🧠 Software Logic Flow
1. **Data Ingestion:** ESP32 samples analog signals at 12-bit resolution.
2. **Transmission:** Data is serialized into a JSON object and sent via HTTP POST.
3. **Processing:** The Python backend calculates State of Charge (SoC) using a linear interpolation of the discharge curve:
   $$SoC = \frac{V_{curr} - V_{min}}{V_{max} - V_{min}} \times 100$$
4. **Visualization:** Streamlit renders the data using Plotly for high-frequency updates.

## 🛠️ Challenges & Solutions
- **Challenge:** WiFi connection drops in industrial environments.
- **Solution:** Implemented a non-blocking reconnection loop in C++ that restores the session without interrupting sensor sampling.
- **Challenge:** High-frequency data causing dashboard lag.
- **Solution:** Integrated `st.session_state` to buffer and display only the most recent 15 telemetry points, optimizing browser performance.

## 🚀 Future Roadmap
- [ ] **Integration with LoRaWAN:** For long-range battery monitoring in remote areas.
- [ ] **Machine Learning Implementation:** Using an LSTM (Long Short-Term Memory) model to predict Remaining Useful Life (RUL).
- [ ] **Mobile Notifications:** Integration with Telegram API for instant emergency alerts.
