# 🛠️ Bill of Materials (Hardware)

To replicate the Smart BMS monitoring node, the following components are required:

| Component | Specification | Quantity | Purpose |
| :--- | :--- | :--- | :--- |
| **Microcontroller** | ESP32 DevKit V1 (30 or 38 pins) | 1 | Main processing and WiFi transmission |
| **Voltage Sensor** | Resistor Divider (10kΩ & 20kΩ) | 1 | Scaling battery voltage to ESP32 ADC range |
| **Temp Sensor** | LM35 or DHT11 | 1 | Measuring battery surface temperature |
| **Power Source** | 18650 Li-ion Battery (or 3.7V/7.4V source) | 1 | The unit under test/monitoring |
| **Connecting Wires** | Jumper Wires (M-to-M / M-to-F) | 10+ | Circuit interconnects |
| **Breadboard** | 400 or 800 Point | 1 | For prototyping the circuit |

> **Note:** For the Resistor Divider, ensure you use 1% tolerance resistors for better accuracy in voltage readings.
