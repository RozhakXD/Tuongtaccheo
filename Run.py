#!/usr/bin/env python3
try:
    import requests, re, json, time, os
    from requests.exceptions import RequestException
    from rich.columns import Columns
    from rich import print as Println
    from rich.panel import Panel
    from rich.console import Console
except ModuleNotFoundError:
    print(f"Error: It seems some required modules are missing! Please install the necessary dependencies before running the program.")
    exit()

INFORMATION, SUKSES, GAGAL, KOIN = [], [], [], {
    "Jumlah": 0
}

class LOGIN:

    def __init__(self) -> None:
        pass

    def COOKIES(self) -> None:
        try:
            BANNER()
            Println(Panel(f"[bold white]Please enter the Tuongtaccheo cookies. You can obtain these cookies in the account settings!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Cookies TTC] <<"))
            cookies_ttc = Console().input(f"[bold misty_rose1]   ╰─> ")
            self.username, self.koin = self.MENGECEK_TUONGTACCHEO(cookies_ttc)
            Println(Panel(f"[bold white]Please enter the Facebook account cookies. Ensure the user is already configured,\nand the account is set to use the Indonesian language!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [FB Login] <<"))
            cookies_fb = Console().input(f"[bold misty_rose1]   ╰─> ")
            self.name, self.user = self.MENGECEK_FACEBOOK(cookies_fb)
            with requests.Session() as session:
                session.headers.update(
                    {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'tuongtaccheo.com',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'Accept': '*/*',
                        'Cookie': f'{cookies_ttc}',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        'Sec-Fetch-Dest': 'empty',
                    }
                )
                if 'i_user=' in str(cookies_fb):
                    self.iddat = re.search(r"i_user=(\d+);", str(cookies_fb)).group(1)
                else:
                    self.iddat = re.search(r"c_user=(\d+);", str(cookies_fb)).group(1)
                data = {
                    'iddat[]': self.iddat,
                    'loai': 'fb',
                }
                response = session.post('https://tuongtaccheo.com/cauhinh/datnick.php', data=data, allow_redirects=False, verify=True)
                if response.text == '2':
                    Println(Panel(f"[bold red]You must add the account to the configuration. Please visit the Tuongtaccheo website!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [TTC Configuration] <<"))
                    exit()
                elif response.text == '1':
                    Println(Panel(f"""[bold white]Username :[bold green] {self.username}
[bold white]Link :[bold red] https://web.facebook.com/{self.user}""", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Welcome] <<"))
                    with open('Penyimpanan/Cookies.json', 'w') as w:
                        w.write(
                            json.dumps(
                                {
                                    'Tuongtaccheo': f'{cookies_ttc}',
                                    'Facebook': f'{cookies_fb}',
                                }, indent=4
                            )
                        )
                    MISI().DAPATKAN_DATA_FOLLOW(cookies_fb, '100006609458697')
                    FITUR()
                else:
                    Println(Panel(f"[bold red]{str(response.text).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                    exit()
        except Exception as error:
            Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
            exit()

    def MENGECEK_TUONGTACCHEO(self, cookies_ttc: str) -> tuple:
        with requests.Session() as session:
            session.headers.update(
                {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Host': 'tuongtaccheo.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Cookie': f'{cookies_ttc}',
                }
            )
            response = session.get('https://tuongtaccheo.com/caidat/', allow_redirects=False, verify=True)
            INFORMATION.clear()
            for strings in ['Tên tài khoản', 'Số dư']:
                self.find_coins = re.search(r'''<th scope="row">{}</th>
      <td>(.*?)</td>'''.format(strings), response.text).group(1)
                INFORMATION.append(f'{self.find_coins}')
            self.username, self.koin = INFORMATION[0], INFORMATION[1]
            KOIN.update({
                "Jumlah": self.koin
            })
        return (
            self.username, self.koin
        )
    
    def MENGECEK_FACEBOOK(self, cookies_fb: str) -> tuple:
        with requests.Session() as session:
            session.headers.update(
                {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Host': 'web.facebook.com',
                    'Accept-Language': 'en-US,en;q=0.9',
                }
            )
            response = session.get('https://web.facebook.com/', cookies = {
                'Cookie': cookies_fb
            }, allow_redirects=True, verify=True)
            self.find_account = re.search(r'{"ACCOUNT_ID":"(\d+)","USER_ID":".*?","NAME":"(.*?)"', response.text)
            self.name, self.user = self.find_account.group(2), self.find_account.group(1)
            if len(self.name) == 0 and int(self.user) == 0:
                Println(Panel(f"[bold red]Sorry, it seems your Facebook cookies can no longer be use\nd. Please try retrieving the cookies again!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Cookies Expired] <<"))
                time.sleep(4.5)
                self.COOKIES()
            else:
                return (
                    self.name, self.user
                )

class FITUR:

    def __init__(self) -> None:
        try:
            BANNER()
            self.cookies_ttc = json.loads(open('Penyimpanan/Cookies.json', 'r').read())['Tuongtaccheo']
            self.cookies_fb = json.loads(open('Penyimpanan/Cookies.json', 'r').read())['Facebook']
            self.username, self.koin = LOGIN().MENGECEK_TUONGTACCHEO(self.cookies_ttc)
            self.name, self.user = LOGIN().MENGECEK_FACEBOOK(self.cookies_fb)
            Println(Columns([
                Panel(f"""[bold white]Username :[bold green] {self.username[:14]}
[bold white]Coin :[bold yellow] {self.koin[:18]}""", width=31, style="bold misty_rose1"),
                Panel(f"""[bold white]Name :[bold green] {self.name[:18]}
[bold white]User :[bold yellow] {self.user[:18]}""", width=31, style="bold misty_rose1")
            ]))
        except Exception as error:
            Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
            time.sleep(5.0)
            LOGIN().COOKIES()

        Println(Panel("""[bold green]1[bold white]. Starting a Facebook Follow Mission
[bold green]2[bold white]. Starting a Facebook Likes Mission
[bold green]3[bold white]. Exchange Coins To Followers
[bold green]4[bold white]. Exchange Coins To Likes ([bold green]New[bold white])
[bold green]5[bold white]. Logout ([bold red]Exit[bold white])""", width=63, style="bold misty_rose1", title=f"[bold misty_rose1]>> [Key Features] <<", subtitle="[bold misty_rose1]╭──────", subtitle_align="left"))
        choose = Console().input(f"[bold misty_rose1]   ╰─> ")
        if choose == '01' or choose == '1':
            try:
                Println(Panel(f"[bold white]Please enter the delay for running the mission. You must use a minimum delay\nof 60 seconds for safety and input numbers only!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Set Delay] <<"))
                delay = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                if delay < 10:
                    Println(Panel(f"[bold red]Sorry, you cannot use a mission delay of less than 10 secon\nds. This may cause your account to be blocked!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Mission Delay] <<"))
                    exit()
                else:
                    Println(Panel(f"[bold white]You can use[bold green] CTRL + C[bold white] if it gets stuck and[bold red] CTRL + Z[bold white] if you want to stop. If\nmissions keep failing, your account might be blocked!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Note] <<"))
                    while True:
                        try:
                            MISI().FOLLOWING(self.cookies_ttc, self.cookies_fb, delay)
                        except RequestException:
                            Println(f"[bold misty_rose1]   ──>[bold red] CONNECTION ERROR...                 ", end='\r')
                            time.sleep(10.0)
                            continue
                        except KeyboardInterrupt:
                            continue
            except Exception as error:
                Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                exit()
        elif choose == '02' or choose == '2':
            try:
                Println(Panel(f"[bold white]Please enter the delay for running the mission. You must use a minimum delay\nof 60 seconds for safety and input numbers only!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Set Delay] <<"))
                delay = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                if delay < 10:
                    Println(Panel(f"[bold red]Sorry, you cannot use a mission delay of less than 10 secon\nds. This may cause your account to be blocked!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Mission Delay] <<"))
                    exit()
                else:
                    Println(Panel(f"[bold white]You can use[bold green] CTRL + C[bold white] if it gets stuck and[bold red] CTRL + Z[bold white] if you want to stop. If\nmissions keep failing, your account might be blocked!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Note] <<"))
                    while True:
                        try:
                            MISI().LIKES(self.cookies_ttc, self.cookies_fb, delay)
                        except RequestException:
                            Println(f"[bold misty_rose1]   ──>[bold red] CONNECTION ERROR...                 ", end='\r')
                            time.sleep(10.0)
                            continue
                        except KeyboardInterrupt:
                            continue
            except Exception as error:
                Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                exit()
        elif choose == '03' or choose == '3':
            try:
                Println(Panel(f"[bold white]Please enter the Facebook account ID. Make sure the account only has a follow button and is set to public mode!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [UserID Facebook] <<"))
                target_id = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                Println(Columns([
                    Panel(f"[bold green]20[bold white] Follower :[bold red] 22.000 Coin", width=31, style="bold misty_rose1"),
                    Panel(f"[bold green]100[bold white] Follower :[bold red] 110.000", width=31, style="bold misty_rose1"),
                ]))
                Println(Panel(f"[bold white]Please enter the number of followers you want to purchase. Ensure you have enough coins to buy the followers!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Follower Count] <<"))
                jumlah = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                TUKARKAN().KOIN(self.cookies_ttc, jumlah, target_id, 'SUBNICK', 'tangsub')
            except Exception as error:
                Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                exit()
        elif choose == '04' or choose == '4':
            try:
                Println(Panel(f"[bold white]Please enter the Facebook post link. Make sure the post can be liked by the public!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Post Link] <<"))
                target_id = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                Println(Columns([
                    Panel(f"[bold green]50[bold white] Likes :[bold red] 42.500 Coin", width=31, style="bold misty_rose1"),
                    Panel(f"[bold green]1000[bold white] Likes :[bold red] 850.000", width=31, style="bold misty_rose1"),
                ]))
                Println(Panel(f"[bold white]Please enter the number of likes you want to purchase. Ensu\nre you have enough coins to buy the likes!", width=63, style="bold misty_rose1", subtitle="[bold misty_rose1]╭──────", subtitle_align="left", title="[bold misty_rose1]>> [Like Count] <<"))
                jumlah = int(Console().input(f"[bold misty_rose1]   ╰─> "))
                TUKARKAN().KOIN(self.cookies_ttc, jumlah, target_id, 'LIKE', 'tanglike')
            except Exception as error:
                Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                exit()
        elif choose == '05' or choose == '5':
            try:
                os.remove('Penyimpanan/Cookies.json')
                Println(Panel(f"[bold white]You have selected the exit option. Thank you for using this program!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Exit] <<"))
                exit()
            except:
                exit()
        else:
            Println(Panel(f"[bold red]The option you entered is not available in this feature. Please try again!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Invalid Option] <<"))
            time.sleep(5.0)
            FITUR()

class TUKARKAN:

    def __init__(self) -> None:
        pass

    def KOIN(self, cookies_ttc: str, jumlah: int, target_id: int, loai: str, tang: str) -> None:
        with requests.Session() as session:
            session.headers.update(
                {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Host': 'tuongtaccheo.com',
                    'Accept': '*/*',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Cookie': f'{cookies_ttc}',
                }
            )
            data = {
                'link': f'https://www.facebook.com/{target_id}',
                'loai': f'{loai}',
                'sl': f'{jumlah}',
                'id': f'{target_id}',
            }
            response = session.post('https://tuongtaccheo.com/{}/themvip.php'.format(tang), data=data, allow_redirects=False, verify=True)
            if str(response.text) == '1':
                Println(Panel(f"[bold red]Sorry, you do not have enough coins to purchase followers or likes. Please try running a mission first!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Insufficient Coins] <<"))
                exit()
            elif 'Mua thành công' in str(response.text):
                if str(tang) == 'tanglike':
                    Println(Panel(f"""[bold white]Status :[bold green] Successful purchase![/]
[bold white]Link :[bold yellow] https://web.facebook.com/{target_id}
[bold white]Likes :[bold green] +{jumlah}""", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Success] <<"))
                    exit()
                else:
                    Println(Panel(f"""[bold white]Status :[bold green] Successful purchase![/]
[bold white]Link :[bold yellow] https://web.facebook.com/{target_id}
[bold white]Followers :[bold green] +{jumlah}""", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Success] <<"))
                    exit()
            else:
                Println(Panel(f"[bold red]{str(response.text).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
                exit()

class MISI:

    def __init__(self) -> None:
        pass

    def LIKES(self, cookies_ttc: str, cookies_fb: str, delay: int) -> None:
        with requests.Session() as session:
            session.headers.update(
                {
                    'referer': 'https://tuongtaccheo.com/kiemtien/likepostcheo/',
                    'x-requested-with': 'XMLHttpRequest',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'cookie': f'{cookies_ttc}',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'sec-fetch-site': 'same-origin',
                    'Host': 'tuongtaccheo.com',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'accept-language': 'en-US,en;q=0.9',
                }
            )
            response = session.get('https://tuongtaccheo.com/kiemtien/likepostcheo/getpost.php')
            if '"idpost":' in str(response.text):
                for data in json.loads(response.text):
                    self.idpost, self.profile_url = data['idpost'], data['link'].replace('\\', '')
                    session.headers.clear()
                    session.cookies.clear()
                    for sleep in range(delay, 0, -1):
                        Println(f"[bold misty_rose1]   ──>[bold blue] {self.idpost}[bold white]/[bold green]{sleep}[bold white] SUCCESS:-[bold blue]{len(SUKSES)}[bold white] FAILED:-[bold red]{len(GAGAL)}[bold white]    ", end='\r')
                        time.sleep(1)
                    if self.DAPATKAN_DATA_LIKES(cookies_fb, self.idpost) == 'Sukses':
                        session.headers.update(
                            {
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                                'referer': 'https://tuongtaccheo.com/kiemtien/likepostcheo/',
                                'origin': 'https://tuongtaccheo.com',
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-site': 'same-origin',
                                'accept': '*/*',
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'cookie': f'{cookies_ttc}',
                                'Host': 'tuongtaccheo.com',
                                'sec-fetch-dest': 'empty',
                                'x-requested-with': 'XMLHttpRequest',
                            }
                        )
                        data = {
                            'id': self.idpost
                        }
                        time.sleep(5)
                        response2 = session.post('https://tuongtaccheo.com/kiemtien/likepostcheo/nhantien.php', data = data)
                        if 'Thành công' in response2.text:
                            try:
                                self.obtained = re.search('cộng (.*?) xu', response2.text).group(1)
                                self.username, self.koin = LOGIN().MENGECEK_TUONGTACCHEO(cookies_ttc)
                            except Exception:
                                self.obtained, self.username, self.koin = (600, None, 404)
                            Println(Panel(f"""[bold white]Status :[bold green] Liked successfully[/]
[bold white]Link :[bold red] https://web.facebook.com/{str(self.idpost)[:23]}
[bold white]Coin :[bold green] +{self.obtained}[bold white] >[bold yellow] {self.koin}""", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Success] <<"))
                            SUKSES.append(self.idpost)
                        elif "Bạn chưa like ID này, vui lòng tải lại làm lại" in response2.text:
                            Println(f"[bold misty_rose1]   ──>[bold red] YOU HAVEN'T LIKED THIS POST!", end='\r')
                            time.sleep(3.5)
                            GAGAL.append(self.idpost)
                            continue
                        elif "Bạn đang sử dụng nick tên nước ngoài" in response2.text:
                            Println(Panel(f"[bold red]Sorry, it seems you're not using a Vietnamese name, which caused you to fail in earning coins.\nPlease change your Facebook account name and try again!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Name Issue] <<"))
                            exit()
                        else:
                            GAGAL.append(self.idpost)
                            continue
                    else:
                        GAGAL.append(self.idpost)
                        continue
            else:
                Println(f"[bold misty_rose1]   ──>[bold red] THERE ARE NO MISSIONS...                 ", end='\r')
                time.sleep(10.0)
                return

    def DAPATKAN_DATA_LIKES(self, cookies_fb: str, target_id: str) -> str:
        with requests.Session() as session:
            session.headers.update(
                {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'Host': 'web.facebook.com',
                    'sec-fetch-site': 'none',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'sec-fetch-mode': 'navigate',
                }
            )
            response = session.get('https://web.facebook.com/{}'.format(target_id), cookies = {
                'Cookie': cookies_fb
            }, allow_redirects=True, verify=True)
            try:
                self.lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', response.text).group(1)
                self.actorID = re.search(r'"actorID":"(\d+)"', response.text).group(1)
                self.__hs = re.search(r'"haste_session":"(.*?)"', response.text).group(1)
                self.all_spin__ = re.search(r'"__spin_r":(\d+),"__spin_b":"(.*?)","__spin_t":(\d+),', response.text)
                self.__spin_r, self.__spin_b, self.__spin_t = self.all_spin__.group(1), self.all_spin__.group(2), self.all_spin__.group(3)
                self.__hsi = re.search(r'"hsi":"(\d+)"', response.text).group(1)
                self.fb_dtsg = re.search(r'"DTSGInitData",\[\],{"token":"(.*?)",', response.text).group(1)
                self.jazoest = re.search(r'&jazoest=(\d+)"', response.text).group(1)
                self.feedback_id = re.search(r'feedback":{"id":"(.*?)"', response.text).group(1)
                self.tracking = re.findall(r'"encrypted_tracking":"(.*?)"', response.text)[3]
            except (AttributeError, IndexError):
                Println(f"[bold misty_rose1]   ──>[bold yellow] FORMS NOT FOUND...                 ", end='\r')
                time.sleep(4.5)
                return "Error"
            if self.SUBMIT_LIKES(cookies_fb, target_id) == 'Sukses':
                return "Sukses"
            else:
                return "Gagal"
            
    def SUBMIT_LIKES(self, cookies_fb: str, target_id: str) -> str:
        with requests.Session() as session:
            session.headers.update(
                {
                    'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-fetch-site': 'same-origin',
                    'Host': 'web.facebook.com',
                    'referer': 'https://web.facebook.com/',
                    'x-asbd-id': '198387',
                    'sec-fetch-dest': 'empty',
                    'accept': '*/*',
                    'accept-language': 'id,en;q=0.9',
                    'origin': 'https://web.facebook.com',
                    'x-fb-lsd': f'{self.lsd}',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'sec-fetch-mode': 'cors',
                }
            )
            data = {
                'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
                '__spin_b': f'{self.__spin_b}',
                'fb_dtsg': f'{self.fb_dtsg}',
                '__rev': f'{self.__spin_r}',
                'av': f'{self.actorID}',
                'fb_api_caller_class': 'RelayModern',
                '__hs': f'{self.__hs}',
                'jazoest': f'{self.jazoest}',
                '__ccg': 'GOOD',
                '__user': f'{self.actorID}',
                '__hsi': f'{self.__hsi}',
                'server_timestamps': True,
                '__a': '1',
                'lsd': f'{self.lsd}',
                '__csr': '',
                '__s': 'nuoh4g:afciv2:spgqb1',
                '__comet_req': '15',
                'doc_id': '5703418209680126',
                '__dyn': '',
                '__req': 's',
                '__spin_r': f'{self.__spin_r}',
                'dpr': '1.5',
                'variables': '{"input":{"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1684054738994,342738,,","feedback_id":"' + str(self.feedback_id) + '","feedback_reaction_id":"1635855486666999","feedback_source":"OBJECT","is_tracking_encrypted":true,"tracking":["' + str(self.tracking) + '"],"session_id":"fa3b7bd8-b923-4a9e-8f43-5dd993158af5","actor_id":"' + str(self.actorID) + '","client_mutation_id":"1"},"useDefaultActor":false,"scale":1.5}',
                '__spin_t': f'{self.__spin_t}',
            }
            response = session.post('https://web.facebook.com/api/graphql/', data=data, cookies={
                'Cookie': cookies_fb
            }, allow_redirects=False, verify=True)
            if '"can_viewer_react":true' in str(response.text):
                Println(f"[bold misty_rose1]   ──>[bold green] LIKES @{target_id} SUCCESS...           ", end='\r')
                time.sleep(3.5)
                return "Sukses"
            else:
                Println(f"[bold misty_rose1]   ──>[bold red] LIKES @{target_id} FAILED...              ", end='\r')
                time.sleep(3.5)
                return "Gagal"

    def FOLLOWING(self, cookies_ttc: str, cookies_fb: str, delay: int) -> None:
        with requests.Session() as session:
            session.headers.update(
                {
                    'referer': 'https://tuongtaccheo.com/kiemtien/subcheo/',
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'x-requested-with': 'XMLHttpRequest',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Host': 'tuongtaccheo.com',
                    'cookie': f'{cookies_ttc}',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'accept-language': 'en-US,en;q=0.9',
                }
            )
            response = session.get('https://tuongtaccheo.com/kiemtien/subcheo/getpost.php', allow_redirects=False, verify=True)
            if '"idpost":' in str(response.text):
                for data in json.loads(response.text):
                    self.idpost, self.profile_url = data['idpost'], data['link'].replace('\\', '')
                    session.headers.clear()
                    session.cookies.clear()
                    for sleep in range(delay, 0, -1):
                        Println(f"[bold misty_rose1]   ──>[bold blue] {self.idpost}[bold white]/[bold green]{sleep}[bold white] SUCCESS:-[bold blue]{len(SUKSES)}[bold white] FAILED:-[bold red]{len(GAGAL)}[bold white]    ", end='\r')
                        time.sleep(1)
                    self.status = self.DAPATKAN_DATA_FOLLOW(cookies_fb, self.idpost)
                    if self.status == 'Sukses':
                        session.headers.update(
                            {
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'referer': 'https://tuongtaccheo.com/kiemtien/subcheo/',
                                'sec-fetch-site': 'same-origin',
                                'sec-fetch-mode': 'cors',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                                'Host': 'tuongtaccheo.com',
                                'accept': '*/*',
                                'cookie': f'{cookies_ttc}',
                                'origin': 'https://tuongtaccheo.com',
                                'sec-fetch-dest': 'empty',
                                'x-requested-with': 'XMLHttpRequest',
                            }
                        )
                        data = {
                            'id': self.idpost
                        }
                        time.sleep(5)
                        response2 = session.post('https://tuongtaccheo.com/kiemtien/subcheo/nhantien.php', data=data, allow_redirects=False, verify=True)
                        if 'Thành công' in response2.text:
                            try:
                                self.obtained = re.search('cộng (.*?) xu', response2.text).group(1)
                                self.username, self.koin = LOGIN().MENGECEK_TUONGTACCHEO(cookies_ttc)
                            except AttributeError:
                                self.obtained, self.username, self.koin = (600, None, 404)
                            Println(Panel(f"""[bold white]Status :[bold green] Following successfully[/]
[bold white]Link :[bold red] https://web.facebook.com/{self.idpost}
[bold white]Coin :[bold green] +{self.obtained}[bold white] >[bold yellow] {self.koin}""", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Success] <<"))
                            SUKSES.append(self.idpost)
                        elif 'Hãy mở cho người lạ xem danh sách người,trang mà bạn theo dõi.' in response2.text:
                            Println(Panel(f"[bold red]You must make your following list public. Please try to ope\nn it in your Facebook account settings!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Follow List] <<"))
                            exit()
                        elif "Bạn chưa theo dõi nick này, vui lòng tải lại làm lại" in response2.text:
                            Println(f"[bold misty_rose1]   ──>[bold red] YOU HAVE NOT FOLLOWED THIS ACCOUNT...", end='\r')
                            time.sleep(3.5)
                            GAGAL.append(self.idpost)
                            continue
                        else:
                            GAGAL.append(self.idpost)
                            continue
                    else:
                        GAGAL.append(self.idpost)
                        continue
            else:
                Println(f"[bold misty_rose1]   ──>[bold red] THERE ARE NO MISSIONS...                 ", end='\r')
                time.sleep(10.0)
                return

    def DAPATKAN_DATA_FOLLOW(self, cookies_fb: str, target_id: str) -> str:
        with requests.Session() as session:
            session.headers.update(
                {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id,en;q=0.9',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'Host': 'web.facebook.com',
                    'sec-fetch-site': 'none',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'sec-fetch-mode': 'navigate',
                }
            )
            response = session.get('https://web.facebook.com/{}'.format(target_id), cookies = {
                'Cookie': cookies_fb
            }, allow_redirects=True, verify=True)
            try:
                self.lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', response.text).group(1)
                self.actorID = re.search(r'"actorID":"(\d+)"', response.text).group(1)
                self.__hs = re.search(r'"haste_session":"(.*?)"', response.text).group(1)
                self.all_spin__ = re.search(r'"__spin_r":(\d+),"__spin_b":"(.*?)","__spin_t":(\d+),', response.text)
                self.__spin_r, self.__spin_b, self.__spin_t = self.all_spin__.group(1), self.all_spin__.group(2), self.all_spin__.group(3)
                self.__hsi = re.search(r'"hsi":"(\d+)"', response.text).group(1)
                self.fb_dtsg = re.search(r'"DTSGInitData",\[\],{"token":"(.*?)",', response.text).group(1)
                self.jazoest = re.search(r'&jazoest=(\d+)"', response.text).group(1)
            except (AttributeError, IndexError):
                Println(f"[bold misty_rose1]   ──>[bold yellow] FORMS NOT FOUND...                 ", end='\r')
                time.sleep(4.5)
                return "Error"

            if self.SUBMIT_FOLLOW(cookies_fb, target_id) == 'Sukses':
                return "Sukses"
            else:
                return "Gagal"

    def SUBMIT_FOLLOW(self, cookies_fb: str, target_id: str) -> str:
        with requests.Session() as session:
            session.headers.update({
                'content-type': 'application/x-www-form-urlencoded',
                'referer': 'https://web.facebook.com/',
                'accept-language': 'id,en;q=0.9',
                'x-fb-friendly-name': 'CometUserFollowMutation',
                'Host': 'web.facebook.com',
                'x-asbd-id': '198387',
                'accept': '*/*',
                'x-fb-lsd': f'{self.lsd}',
                'origin': 'https://web.facebook.com',
                'sec-fetch-dest': 'empty',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'sec-fetch-mode': 'cors',
            })
            data = {
                'fb_api_req_friendly_name': 'CometUserFollowMutation',
                '__spin_b': f'{self.__spin_b}',
                'fb_api_caller_class': 'RelayModern',
                '__user': f'{self.actorID}',
                '__hs': f'{self.__hs}',
                'fb_dtsg': f'{self.fb_dtsg}',
                'jazoest': f'{self.jazoest}',
                '__ccg': 'GOOD',
                '__hsi': f'{self.__hsi}',
                'server_timestamps': True,
                '__a': '1',
                '__rev': f'{self.__spin_r}',
                'av': f'{self.actorID}',
                'lsd': f'{self.lsd}',
                '__csr': '',
                '__s': '66tl9r:afciv2:6uzrkk',
                '__comet_req': '8',
                'doc_id': '28167180839546919',
                '__dyn': '',
                '__req': 's',
                '__spin_r': f'{self.__spin_r}',
                'dpr': '1',
                'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1737545688828,497388,250100865708545,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"' + str(target_id) + '","tracking":null,"actor_id":"' + str(self.actorID) + '","client_mutation_id":"1"},"scale":1}',
                '__spin_t': f'{self.__spin_t}',
            }
            response = session.post('https://web.facebook.com/api/graphql/', data = data, cookies = {
                'Cookie': cookies_fb
            })
            if str(target_id) != '100006609458697':
                if '{"data":{"actor_subscribe":{"subscribee":' in response.text:
                    Println(f"[bold misty_rose1]   ──>[bold green] FOLLOW @{target_id} SUCCESS...           ", end='\r')
                    time.sleep(3.5)
                    return "Sukses"
                elif 'A server error field_exception occured. Check server logs for details.' in response.text:
                    if str(target_id) == '100006609458697':
                        return "Gagal"
                    else:
                        Println(Panel(f"[bold red]Sorry, we noticed your account has failed to follow repeat\nedly. Your Facebook account might be blocked!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Account Blocked] <<"))
                        exit()
                else:
                    Println(f"[bold misty_rose1]   ──>[bold red] FOLLOW @{target_id} FAILED...              ", end='\r')
                    time.sleep(3.5)
                    return "Gagal"
            else:
                return "Sukses"

def BANNER() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    Println(
        Panel(r"""[bold red]●[bold yellow] ●[bold green] ●[/]
[bold green]   _____                ______    _ _                   
  |_   _|               |  ___|  | | |                  
    | | __ _ _ __   __ _| |_ ___ | | | _____      _____ 
    | |/ _` | '_ \ / _` |  _/ _ \| | |/ _ \ \ /\ / / __|
    | | (_| | | | | (_| | || (_) | | | (_) \ V  V /\__ \
    \_/\__,_|_| |_|\__, \_| \___/|_|_|\___/ \_/\_/ |___/
                    __/ |                               
[bold green]                   |___/                                
       [underline red]Free Facebook Followers - Coded by Rozhak-XD""", width=63, style="bold misty_rose1")
    )

if __name__ == '__main__':
    try:
        if not os.path.exists('Penyimpanan/Subscribe.json'):
            youtube_video = requests.get('https://raw.githubusercontent.com/RozhakXD/Tuongtaccheo/refs/heads/main/Penyimpanan/Youtube.json', allow_redirects=False, verify=True).json()['Link']
            os.system(f'xdg-open {youtube_video}')
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                json.dump({"Status": True}, w, indent=4)
            time.sleep(2.5)
        os.system('git pull')
        FITUR()
    except Exception as error:
        Println(Panel(f"[bold red]{str(error).title()}!", width=63, style="bold misty_rose1", title="[bold misty_rose1]>> [Error] <<"))
        exit()
    except KeyboardInterrupt:
        exit()