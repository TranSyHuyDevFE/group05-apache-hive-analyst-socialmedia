import random
import requests
from typing import Dict, List, Optional, Tuple


class ProxyRotator:
    """
    A class to handle random rotation of proxies with authentication.
    """

    def __init__(self, proxy_list: Optional[List[str]] = None):
        """
        Initialize the ProxyRotator with a list of proxies.

        Args:
            proxy_list: List of proxy strings in format "ip:port:username:password"
        """
        if proxy_list is None:
            self.proxy_list = [
                "23.95.150.145:6114:gxpbgqzo:jw4s6taqhzfd",
                "198.23.239.134:6540:gxpbgqzo:jw4s6taqhzfd",
                "45.38.107.97:6014:gxpbgqzo:jw4s6taqhzfd",
                "207.244.217.165:6712:gxpbgqzo:jw4s6taqhzfd",
                "107.172.163.27:6543:gxpbgqzo:jw4s6taqhzfd",
                "104.222.161.211:6343:gxpbgqzo:jw4s6taqhzfd",
                "64.137.96.74:6641:gxpbgqzo:jw4s6taqhzfd",
                "216.10.27.159:6837:gxpbgqzo:jw4s6taqhzfd",
                "136.0.207.84:6661:gxpbgqzo:jw4s6taqhzfd",
                "142.147.128.93:6593:gxpbgqzo:jw4s6taqhzfd"
            ]
        else:
            self.proxy_list = proxy_list

        self.working_proxies = self.proxy_list.copy()
        self.failed_proxies = []

    def _parse_proxy(self, proxy_string: str) -> Tuple[str, str, str, str]:
        """
        Parse proxy string into components.

        Args:
            proxy_string: Proxy in format "ip:port:username:password"

        Returns:
            Tuple of (ip, port, username, password)
        """
        parts = proxy_string.split(':')
        if len(parts) != 4:
            raise ValueError(f"Invalid proxy format: {proxy_string}")
        return parts[0], parts[1], parts[2], parts[3]

    def get_random_proxy(self) -> Optional[str]:
        """
        Get a random proxy from the working proxy list.

        Returns:
            Random proxy string or None if no working proxies available
        """
        if not self.working_proxies:
            return None
        return random.choice(self.working_proxies)

    def get_proxy_dict(self, proxy_string: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        Get proxy configuration as a dictionary for use with requests.

        Args:
            proxy_string: Specific proxy to use, or None for random selection

        Returns:
            Dictionary with proxy configuration for requests library
        """
        if proxy_string is None:
            proxy_string = self.get_random_proxy()

        if proxy_string is None:
            return None

        try:
            ip, port, username, password = self._parse_proxy(proxy_string)
            proxy_url = f"http://{username}:{password}@{ip}:{port}"

            return {
                'http': proxy_url,
                'https': proxy_url
            }
        except ValueError:
            return None

    def get_proxy_auth(self, proxy_string: Optional[str] = None) -> Optional[Tuple[str, Dict[str, str]]]:
        """
        Get proxy URL and auth separately.

        Args:
            proxy_string: Specific proxy to use, or None for random selection

        Returns:
            Tuple of (proxy_url, auth_dict) or None
        """
        if proxy_string is None:
            proxy_string = self.get_random_proxy()

        if proxy_string is None:
            return None

        try:
            ip, port, username, password = self._parse_proxy(proxy_string)
            proxy_url = f"http://{ip}:{port}"
            auth = {'username': username, 'password': password}

            return proxy_url, auth
        except ValueError:
            return None

    def mark_proxy_failed(self, proxy_string: str) -> None:
        """
        Mark a proxy as failed and remove it from working proxies.

        Args:
            proxy_string: The proxy that failed
        """
        if proxy_string in self.working_proxies:
            self.working_proxies.remove(proxy_string)
            self.failed_proxies.append(proxy_string)

    def reset_failed_proxies(self) -> None:
        """
        Reset failed proxies back to working state.
        """
        self.working_proxies.extend(self.failed_proxies)
        self.failed_proxies.clear()

    def test_proxy(self, proxy_string: str, test_url: str = "http://httpbin.org/ip", timeout: int = 10) -> bool:
        """
        Test if a proxy is working.

        Args:
            proxy_string: Proxy to test
            test_url: URL to test against
            timeout: Request timeout in seconds

        Returns:
            True if proxy is working, False otherwise
        """
        proxy_dict = self.get_proxy_dict(proxy_string)
        if proxy_dict is None:
            return False

        try:
            response = requests.get(
                test_url, proxies=proxy_dict, timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False

    def get_working_proxy_count(self) -> int:
        """
        Get the number of working proxies.

        Returns:
            Number of working proxies
        """
        return len(self.working_proxies)

    def get_failed_proxy_count(self) -> int:
        """
        Get the number of failed proxies.

        Returns:
            Number of failed proxies
        """
        return len(self.failed_proxies)


# # Example usage
# if __name__ == "__main__":
#     # Initialize proxy rotator
#     rotator = ProxyRotator()

#     # Get a random proxy
#     proxy = rotator.get_random_proxy()
#     print(f"Random proxy: {proxy}")

#     # Get proxy dict for requests
#     proxy_dict = rotator.get_proxy_dict()
#     print(f"Proxy dict: {proxy_dict}")

#     # Test a proxy
#     if proxy:
#         is_working = rotator.test_proxy(proxy)
#         print(f"Proxy {proxy} is working: {is_working}")

#     print(f"Working proxies: {rotator.get_working_proxy_count()}")
#     print(f"Failed proxies: {rotator.get_failed_proxy_count()}")
