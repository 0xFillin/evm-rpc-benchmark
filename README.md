# EVM RPC Benchmark Tool

![](https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=Ethereum&logoColor=white)
![](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)

A tool to benchmark Ethereum Virtual Machine (EVM) compatible RPC endpoints, with optional proxy support. This script provides insights into the performance of RPC nodes by measuring response times and success rates.



## 👉 Features
- **Benchmarking:** Measure response times, success rates, and requests per second (RPS) for EVM RPC endpoints.
- **Proxy Support:** Option to benchmark RPC endpoints through proxies.
- **Asynchronous:** Uses `asyncio` for concurrent requests to ensure efficient benchmarking.
- **Simple CLI Interface:** Choose between benchmarking with or without proxies.
- **Output:** Results are stored in JSON format and displayed in a tabulated form in the console.

## 👉 Prerequisites
- Python 3.7+
- `aiohttp` for asynchronous HTTP requests
- `tabulate` for pretty printing the results
- `termcolor` for colored console output
- `colorama` for cross-platform colored terminal text

Install the required packages using:

```bash
pip install aiohttp tabulate termcolor colorama
```

# 👨‍💻 Usage

## 🟣 Prepare Input Files:
- `rpc.txt`: Contains URLs of RPC endpoints, one per line.
- `proxy.txt` (optional): Contains proxy servers, one per line.

## 💻 Run the Script:
```bash
python3 benchmark.py
```

## 🥢 You'll be prompted to choose an option:

- For RPC Benchmark without proxy
- For RPC Benchmark with proxy

## 📍 View Results:
Results are saved in `results.json`. A summary table appears in the console with color-coded data for easy reading.

## 📁 Example Files

### > rpc.txt
```arduino
https://mainnet.infura.io/v3/YOUR_PROJECT_ID
https://eth-mainnet.alchemyapi.io/v2/YOUR_API_KEY
```

### > proxy.txt
```
login:password@ip:port
```

## 🐍 Understanding the Output
- **RPC URL**: The endpoint being tested.
- **Proxy**: Indicates if a proxy was used (yellow if yes, black if no).
- **Avg Response Time**: Average response time in milliseconds. Green if below 100ms, red otherwise.
- **Min/Max Response Time**: Best and worst-case response times.
- **Successful Responses**: Number of successful requests.
- **Error Responses**: Number of failed requests.
- **RPS**: Requests per second within a defined response time threshold (`MAX_RESPONSE_TIME = 1000ms`).

## 🗒 Notes
- Adjust `MAX_RESPONSE_TIME` in the script to define what counts towards the RPS calculation.
- The script uses a specific Ethereum call to benchmark, which can be modified for different use cases.

## 📚 Author
**0xFillin**  
- Twitter: [@0xFillin](https://twitter.com/0xFillin)  
- GitHub: [0xFillin/evm-rpc-benchmark](https://github.com/0xFillin/evm-rpc-benchmark)

## 💻 License
This project is licensed under the MIT License. See the ```LICENSE``` file for more details.

Happy benchmarking!