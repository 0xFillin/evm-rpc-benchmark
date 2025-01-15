import time
import json
import asyncio
import aiohttp
from tabulate import tabulate
from termcolor import colored
from colorama import init, Fore

init(autoreset=True)

RPC_FILE = 'rpc.txt'
PROXY_FILE = 'proxy.txt'
OUTPUT_JSON = 'results.json'

MAX_RESPONSE_TIME = 1000


async def send_request(session, rpc_url, proxy=None):
    start_time = time.perf_counter() * 1000
    try:
        data = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [
                {
                    "from": None,
                    "to": "0x6b175474e89094c44da98b954eedeac495271d0f",
                    "data": "0x70a082310000000000000000000000006E0d01A76C3Cf4288372a29124A26D4353EE51BE"
                },
                "latest",
                {
                    "0x1111111111111111111111111111111111111111": {
                        "balance": "0xFFFFFFFFFFFFFFFFFFFF"
                    }
                }
            ],
            "id": 1
        }

        if proxy:
            proxy_url = f"http://{proxy}"
            async with session.post(rpc_url, json=data, proxy=proxy_url) as response:
                response_text = await response.text()
        else:
            async with session.post(rpc_url, json=data) as response:
                response_text = await response.text()

        response_time = time.perf_counter() * 1000 - start_time

        if "Too Many Requests" in response_text:
            return {"success": False, "error": "Too Many Requests", "response_time": response_time, "proxy": proxy}

        if 'result":"0x' in response_text:
            return {"success": True, "response_time": response_time, "proxy": proxy}
        else:
            return {"success": False, "response_time": response_time, "error": "Invalid result", "proxy": proxy}

    except Exception as e:
        return {"success": False, "response_time": time.perf_counter() * 1000 - start_time, "error": str(e), "proxy": proxy}


async def benchmark_rpc(rpc_url, proxies=None):
    print(Fore.MAGENTA + f"BENCHMARK | Sending requests to RPC: {rpc_url}")

    results = []
    if proxies:
        for proxy in proxies:
            async with aiohttp.ClientSession() as session:
                tasks = [send_request(session, rpc_url, proxy) for _ in range(100)]
                responses = await asyncio.gather(*tasks, return_exceptions=True)
    else:
        async with aiohttp.ClientSession() as session:
            tasks = [send_request(session, rpc_url) for _ in range(100)]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

    successful_responses = [res for res in responses if isinstance(res, dict) and res['success']]
    failed_responses = [res for res in responses if not isinstance(res, dict) or not res['success']]

    total_requests = len(responses)
    successful_requests = len(successful_responses)
    failed_requests = len(failed_responses)

    if successful_responses:
        response_times = [res['response_time'] for res in successful_responses]
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        rps = sum(1 for res in successful_responses if res['response_time'] <= MAX_RESPONSE_TIME)
    else:
        avg_response_time = min_response_time = max_response_time = rps = None

    return {
        "rpc_url": rpc_url,
        "proxy": proxies[0] if proxies else None,
        "avg_response_time": round(avg_response_time, 2) if avg_response_time else "N/A",
        "min_response_time": round(min_response_time, 2) if min_response_time else "N/A",
        "max_response_time": round(max_response_time, 2) if max_response_time else "N/A",
        "successful_responses": successful_requests,
        "error_responses": failed_requests,
        "rps": rps
    }


async def main():
    print(Fore.MAGENTA + """
██████╗ ██████╗  ██████╗    ████████╗███████╗███████╗████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║            ██║   █████╗  ███████╗   ██║   █████╗  ██████╔╝
██╔══██╗██╔═══╝ ██║            ██║   ██╔══╝  ╚════██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║██║     ╚██████╗       ██║   ███████╗███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚═╝      ╚═════╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

> Author: 0xFillin https://x.com/0xFillin
> Github: https://github.com/0xFillin/evm-rpc-benchmark
""")
    print("Select an option:")
    print("1. RPC Benchmark")
    print("2. RPC Benchmark with Proxy")

    choice = input("Enter choice: ").strip()

    print("\n")

    if choice == "1":
        with open(RPC_FILE, 'r') as file:
            rpc_list = [line.strip() for line in file if line.strip()]

        results = []

        for rpc_url in rpc_list:
            try:
                result = await benchmark_rpc(rpc_url)
                results.append(result)
            except Exception as e:
                print(Fore.RED + f"Error while benchmarking {rpc_url}: {e}")

    elif choice == "2":
        with open(PROXY_FILE, 'r') as file:
            proxy_list = [line.strip() for line in file if line.strip()]

        with open(RPC_FILE, 'r') as file:
            rpc_list = [line.strip() for line in file if line.strip()]

        results = []
        for rpc_url in rpc_list:
            try:
                result = await benchmark_rpc(rpc_url, proxy_list)
                results.append(result)
            except Exception as e:
                print(Fore.RED + f"Error while benchmarking {rpc_url}: {e}")

    else:
        print(Fore.YELLOW + "Invalid choice")
        return

    with open(OUTPUT_JSON, 'w') as file:
        for idx, result in enumerate(results):
            json.dump(result, file, separators=(',', ':'), ensure_ascii=False)
            if idx != len(results) - 1:
                file.write('\n')

    headers = ["RPC URL", "Proxy", "Avg Response Time (ms)", "Min Response Time (ms)", "Max Response Time (ms)", "Successful Responses", "Error Responses", "RPS"]
    table_data = [
        [
            colored(res['rpc_url'], 'cyan'),
            colored(res['proxy'], 'yellow' if res['proxy'] else 'black'),
            colored(res['avg_response_time'], 'green' if isinstance(res['avg_response_time'], float) and res['avg_response_time'] < 100 else 'red'),
            colored(res['min_response_time'], 'green' if isinstance(res['min_response_time'], float) and res['min_response_time'] < 200 else 'red'),
            colored(res['max_response_time'], 'green' if isinstance(res['max_response_time'], float) and res['max_response_time'] < 200 else 'red'),
            colored(res['successful_responses'], 'green'),
            colored(res['error_responses'], 'red'),
            colored(res['rps'], 'green')
        ]
        for res in results
    ]
    
    table = tabulate(table_data, headers=headers, tablefmt="grid", stralign="center")
    print(table)


if __name__ == "__main__":
    asyncio.run(main())
