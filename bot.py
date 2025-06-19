from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from datetime import datetime
from colorama import *
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

USER_AGENT = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
]

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://monami.network",
    "Referer": "https://monami.network/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": random.choice(USER_AGENT)
}

class Monami:
    def __init__(self) -> None:
        self.HEADERS = {}
        self.BASE_API = "https://api.monami.network"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.password = {}
        self.access_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n" + "═" * 60)
        print(Fore.GREEN + Style.BRIGHT + "    ⚡ Auto Connect Node Ping BOT ⚡")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.YELLOW + Style.BRIGHT + "    🧠 Project    : Monami - Automation Bot")
        print(Fore.YELLOW + Style.BRIGHT + "    🧑‍💻 Author     : YetiDAO")
        print(Fore.YELLOW + Style.BRIGHT + "    🌐 Status     : Active & Listening...")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.MAGENTA + Style.BRIGHT + "    🧬 Powered by Cryptodai3 × YetiDAO | Buddy v1.0 🚀")
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "═" * 60 + "\n")

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account

    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, email: str, proxy=None):
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                async with session.post(url="http://ip-api.com/json") as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            self.print_message(email, proxy, Fore.RED, f"Connection Not 200 OK: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
            return None
    
    async def user_login(self, email: str, proxy=None, retries=5):
        url = "https://monami.network/api/login"
        data = json.dumps({"email":email,"password":self.password[email]})
        headers = self.HEADERS[email].copy()
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"Login Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def user_info(self, email: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/users"
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"GET User Info Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def perform_checkin(self, email: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/users/checkin"
        data = json.dumps({"email":email})
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.patch(url=url, headers=headers, data=data, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"Check-In Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def connect_node(self, email: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/points/update-last-active"
        data = json.dumps({"email":email})
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.patch(url=url, headers=headers, data=data, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"Lite Node Not Connected: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def update_point(self, email: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/points/update-point?email={email}"
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"Update Point Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def task_lists(self, email: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/tasks/?email={email.replace('@', '%40')}"
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"GET Task Lists Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def complete_task(self, email: str, task_field: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/users/task"
        data = json.dumps({"email":email, "field":task_field})
        headers = self.HEADERS[email].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.patch(url=url, headers=headers, data=data, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(email, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[email]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.WHITE, f"Task {task_field}{Fore.RED+Style.BRIGHT} Not Completed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def process_check_connection(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            check = await self.check_connection(email, proxy)
            if check and check.get("status") == "success":
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(email)

            await asyncio.sleep(5)

    async def process_user_login(self, email: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(email, use_proxy, rotate_proxy)
        if is_valid:
            while True:
                proxy = self.get_next_proxy_for_account(email) if use_proxy else None

                login = await self.user_login(email, proxy)
                if login:
                    self.access_tokens[email] = login["accessToken"]

                    self.print_message(email, proxy, Fore.GREEN, "Login Success")
                    return True

                await asyncio.sleep(5)

    async def looping_user_login(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            await asyncio.sleep(24 * 60 * 55)
            await self.process_user_login(email, use_proxy, rotate_proxy)

    async def looping_perform_checkin(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            users = await self.user_info(email, use_proxy, rotate_proxy, proxy)
            if users:
                checked_in = users["checkedIn"]

                if checked_in:
                    self.print_message(email, proxy, Fore.YELLOW, "Already Check-In Today")
                else:
                    checkin = await self.perform_checkin(email, use_proxy, rotate_proxy, proxy)
                    if checkin:
                        self.print_message(email, proxy, Fore.GREEN, "Check-In Success")

            await asyncio.sleep(12 * 60 * 60)

    async def process_connect_node(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            connect = await self.connect_node(email, use_proxy, rotate_proxy, proxy)
            if connect and connect.get("message") == "Last active time updated":
                self.print_message(email, proxy, Fore.GREEN, "Lite Node Connected")
                return True

            await asyncio.sleep(5)

    async def looping_connect_node(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            await self.process_connect_node(email, use_proxy, rotate_proxy)
            await asyncio.sleep(24 * 60 * 60)

    async def looping_update_point(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            update = await self.update_point(email, use_proxy, rotate_proxy, proxy)
            if update:
                point_today = update["pointsFarmToday"]
                point_total = update["totalPointsReceived"]
                today_uptime = update["todayUptime"]
                total_uptime = update["totalUptime"]

                self.print_message(email, proxy, Fore.GREEN, "Point Updated"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Earning:{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Today {point_today:.3f} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Total {point_total:.3f} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Uptime: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Today {today_uptime}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Total {total_uptime}{Style.RESET_ALL}"
                )

            await asyncio.sleep(90)

    async def looping_complete_tasks(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            task_lists = await self.task_lists(email, use_proxy, rotate_proxy, proxy)
            if task_lists:

                tasks = [
                    (key, value) for key, value in task_lists.items()
                    if key not in ['_id', 'email', '__v']
                ]

                for task_filed, status in tasks:
                    if status is True:
                        continue

                    complete = await self.complete_task(email, task_filed, use_proxy, rotate_proxy, proxy)
                    if complete:
                        self.print_message(email, proxy, Fore.WHITE, f"Task {task_filed} "
                            f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                        )

                    await asyncio.sleep(1)

                self.print_message(email, proxy, Fore.GREEN, "All Available Tasks Have Been Processed")

            await asyncio.sleep(24 * 60 * 60)                

    async def process_accounts(self, email: str, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_user_login(email, use_proxy, rotate_proxy)
        if logined:
            tasks = [
                asyncio.create_task(self.looping_user_login(email, use_proxy, rotate_proxy)),
                asyncio.create_task(self.looping_perform_checkin(email, use_proxy, rotate_proxy)),
                asyncio.create_task(self.looping_connect_node(email, use_proxy, rotate_proxy)),
                asyncio.create_task(self.looping_update_point(email, use_proxy, rotate_proxy)),
                asyncio.create_task(self.looping_complete_tasks(email, use_proxy, rotate_proxy))
            ]
            await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED + Style.BRIGHT}No Accounts Loaded.{Style.RESET_ALL}")
                return
            
            use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    email = account["Email"]
                    password = account["Password"]

                    if not "@" in email or not password:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Account Data {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    self.HEADERS[email] = HEADERS
                    self.password[email] = password

                    tasks.append(asyncio.create_task(self.process_accounts(email, use_proxy, rotate_proxy)))

            await asyncio.gather(*tasks)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Monami()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Monami Network - BOT{Style.RESET_ALL}                                       "                              
        )
