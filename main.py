import requests

import math


def convert_size(size_bytes):  # bite converter
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


CLIENT_ID = 'f6f0240116aa47e9915a90822469223c'
CLIENT_SECRET = 'a67a13c4081e48698f5b9550da6a7e02'
REDIRECT_URL = 'https://oauth.yandex.ru/verification_code'

YANDEX_BASE_AUTH_URL = 'https://oauth.yandex.ru/authorize'


def get_token():
    print("Enter to the link te get code \U0001F447 ")
    print(f"{YANDEX_BASE_AUTH_URL}?response_type=code&client_id={CLIENT_ID}")
    ver_code = input("Enter the code -> ")
    response = requests.post("https://oauth.yandex.ru/token", data={
        'grant_type': 'authorization_code',
        'code': ver_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    if response.status_code != 200:
        print(response.json())
        return
    return response.json()["access_token"]


resources = 'https://cloud-api.yandex.net/v1/disk/resources/'


def get_user_info(token: str):
    response = requests.get('https://cloud-api.yandex.net/v1/disk', headers={'Authorization': f'OAuth {token}'})
    return response.json()


def run():
    token = get_token()
    if not token:
        print("I DIDN'T GET TOKEN :(")
        return
    print("\t\tWelcome", get_user_info(token)['user']['display_name'], "\U0001F44B",
          "\n\t\t\tChoose what option you want to use \U0001F447 \n",
          "\t1 - Information About User Disk \U0001F4D1"
          "\n\t2 - Files and Folders \U0001F5C2")
    option = input()
    match option:
        case "1":
            info = get_user_info(token)
            print("Total space  \U0001F4E6: ", convert_size(info['total_space']),
                  "\nUsed space \U0001F5F3: ", convert_size(info["used_space"]),
                  "\nTrash size\U0001F5D1: ", convert_size(info['trash_size']))
        case "2":
            cin = input("\t\t\tChoose option \U0001F447"
                        "\n\t 1 - Create a folder \U0001F4C2"
                        "\n\t 2 - Deleting files \U0001F6AE"
                        "\n\t 3 - Get a link to download files \U0001F4E5"
                        "\n\t 4 - Get a link to upload files \U0001F4E4"
                        "\n\t 5 - Upload files to disk by URL \U0001F4E4 \U0001F4E5 \n")
            match cin:
                case '1':
                    path = input("  Enter name: ")
                    files = requests.put(resources + f"?path=%2F{path}",
                                         headers={'Authorization': f'OAuth {token}'}).json()
                    if 'description' in files:
                        print(files['description'])
                    else:
                        print("Folder successfully created :)")
                case '2':
                    path = input("  Enter name: ")
                    requests.delete(resources + f"?path=%2F{path}",
                                    headers={'Authorization': f'OAuth {token}'})
                    print("Successfully deleted :)")
                case '3':
                    path = input("Enter path: ")
                    download = requests.get(resources + f"download?path=%2F{path}",
                                            headers={'Authorization': f'OAuth {token}'}).json()
                    if 'description' in download:
                        print(download['description'])
                    else:
                        print("Cath the link dude -> ", download["href"])
                case '4':
                    path = input("Enter path: ")
                    upload = requests.get(resources + f"upload?path=%2F{path}",
                                          headers={'Authorization': f'OAuth {token}'}).json()
                    if 'description' in upload:
                        print(upload['description'])
                    else:
                        print("Cath the link dude -> ", upload["href"])
                case '5':
                    url = input("Enter URL: ")
                    path = input("Enter PATH: ")
                    publish = requests.post(resources + f"upload?url={url}&path=%2F{path}",
                                            headers={'Authorization': f'OAuth {token}'}).json()
                    if 'description' in publish:
                        print(publish['description'])
                    else:
                        print("Successfully downloaded :)")


if __name__ == '__main__':
    run()
