import time
import requests
import argparse

def calculate_total_time(url, headers, run_number, output_file):
    total_start = time.time()

    response = requests.get(url, headers=headers)

    total_end = time.time()
    total_time = total_end - total_start

    # Print and write the total time for this specific run
    output_message = f"Run {run_number}: {total_time * 1000:.2f} milliseconds\n"
    print(output_message)
    output_file.write(output_message)

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

    # Open the output file
    with open("latency.out", "w") as output_file:
        for i in range(1, args.runs + 1):
            total_time, status_code, response_text = calculate_total_time(args.url, headers, i, output_file)
            total_times.append(total_time)

        average_time = sum(total_times) / len(total_times)

        summary_message = (
            "\nSummary:\n"
            f"Ran the request {args.runs} times.\n"
            f"Average Total Time: {average_time * 1000:.2f} milliseconds\n"
            f"Status Code: {status_code}\n"
        )

        print(summary_message)
        output_file.write(summary_message)

if __name__ == "__main__":
    main()