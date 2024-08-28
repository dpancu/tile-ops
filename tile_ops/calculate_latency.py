import time
import requests
import argparse

def calculate_total_time(url, headers, run_number):
    total_start = time.time()

    response = requests.get(url, headers=headers)

    total_end = time.time()
    total_time = total_end - total_start

    # Print the total time for this specific run
    print(f"Run {run_number}: {total_time * 1000:.2f} milliseconds")

    return total_time, response.status_code, response.text

def main():
    parser = argparse.ArgumentParser(description="Calculate the average latency of a given HTTP request over multiple runs.")
    parser.add_argument("url", type=str, help="The URL to send the request to.")
    parser.add_argument("--header", action="append", help="HTTP headers to include in the request, in 'Key: Value' format.")
    parser.add_argument("--runs", type=int, default=5, help="Number of times to run the request to calculate the average latency.")

    args = parser.parse_args()

    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()

    total_times = []
    status_code = None

    for i in range(1, args.runs + 1):
        total_time, status_code, response_text = calculate_total_time(args.url, headers, i)
        total_times.append(total_time)

    average_time = sum(total_times) / len(total_times)

    print("\nSummary:")
    print(f"Ran the request {args.runs} times.")
    print(f"Average Total Time: {average_time * 1000:.2f} milliseconds")
    print(f"Status Code: {status_code}")

if __name__ == "__main__":
    main()