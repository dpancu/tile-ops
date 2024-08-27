import time
import requests
import argparse
import socket
import ssl
import urllib3

def calculate_latency(url, headers):
    http = urllib3.PoolManager()
    total_start = time.time()

    dns_start = time.time()
    parsed_url = urllib3.util.parse_url(url)
    addr_info = socket.getaddrinfo(parsed_url.host, parsed_url.port or 443)
    dns_end = time.time()
    dns_time = dns_end - dns_start

    conn_start = dns_end
    conn = http.connection_from_url(url)
    conn.request('GET', url, headers=headers)
    conn_end = time.time()
    conn_time = conn_end - conn_start

    ttfb_start = conn_end
    response = conn.urlopen('GET', url, headers=headers, preload_content=False)
    ttfb_end = time.time()
    ttfb_time = ttfb_end - ttfb_start

    content_start = ttfb_end
    content = response.read()
    content_end = time.time()
    content_time = content_end - content_start

    total_end = time.time()
    total_time = total_end - total_start

    return dns_time, conn_time, ttfb_time, content_time, total_time, response.status, content.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description="Calculate various latency metrics of a given HTTP request.")
    parser.add_argument("url", type=str, help="The URL to send the request to.")
    parser.add_argument("--header", action="append", help="HTTP headers to include in the request, in 'Key: Value' format.")

    args = parser.parse_args()

    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()

    dns_time, conn_time, ttfb_time, content_time, total_time, status_code, response_text = calculate_latency(args.url, headers)

    print(f"DNS Resolution Time: {dns_time:.4f} seconds")
    print(f"Connection Time: {conn_time:.4f} seconds")
    print(f"Time to First Byte (TTFB): {ttfb_time:.4f} seconds")
    print(f"Content Download Time: {content_time:.4f} seconds")
    print(f"Total Time: {total_time:.4f} seconds")
    print(f"Status Code: {status_code}")
    print(f"Response Text: {response_text}")

if __name__ == "__main__":
    main()