import datetime
import json
from time import sleep
import os
from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help


def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = "example/stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                # browser = chromium.launch(headless=True)
                browser = chromium.launch(headless=False)
                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(2)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


if __name__ == '__main__':
    # cookie = "please get cookie from your website"
    cookie = "smidV2=20220726204655da23398e128369d7be9b966b4c13157d00c67dc61296c0ad0; abRequestId=174779e6-00f8-5f9e-b0e0-8a901937450f; a1=18b134b5eeb3rzizxhtpj6gtux73gca4g0e62e3lj50000750791; webId=61e38f403125ae04270c101d37e427c2; gid=yYDyq4DKYSkWyYDyq4D2d8dqdDqFu3uCx9UVd1VKk97CWK28qkS04J888W28Wjy8Dy08KiWY; web_session=040069b457ea01f8c69175d526344b652a26ff; galaxy_creator_session_id=Tmpw4tyjguy5L4qVqpeqDFUsQ09Rv1Z4qE3j; galaxy.creator.beaker.session.id=1712563872708033577824; xsecappid=xhs-pc-web; webBuild=4.11.0; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=9c4d7773-f961-4555-be8f-a3dfaaa52234"
    xhs_client = XhsClient(cookie, sign=sign)
    print(datetime.datetime.now())

    current_dir = os.getcwd()
    sub_dir = "img"
    sub_dir_comments = "comments_data"
    dir_path = os.path.join(current_dir, sub_dir)
    dir_path_comments =os.path.join(current_dir, sub_dir_comments)
    
    for _ in range(10):
        # 即便上面做了重试，还是有可能会遇到签名失败的情况，重试即可
        try:
            # 获取xhs的 note
            note = xhs_client.get_note_by_id("6505318c000000001f03c5a6")
            print(json.dumps(note, indent=4))
            print(help.get_imgs_url_from_note(note))

            # # 保存xhs的 图片
            # xhs_client.save_files_from_note_id("6505318c000000001f03c5a6",dir_path)

            # # 保存xhs的 comment
            # note_comment = xhs_client.get_note_all_comments("6505318c000000001f03c5a6")
            # filename = os.path.join(dir_path_comments, 'comments.json')
            # with open(filename, 'w', encoding='utf-8') as f:
            #     json.dump(note_comment, f, ensure_ascii=False, indent=4)
            # print(f"评论数据已保存到文件：{filename}")

            # # 保存xhs的 note
            # note = xhs_client.get_note_by_id("6505318c000000001f03c5a6")
            # filename = os.path.join(dir_path_comments, 'note.json')
            # with open(filename, 'w', encoding='utf-8') as f:
            #     json.dump(note, f, ensure_ascii=False, indent=4)

                
            break
        except DataFetchError as e:
            print(e)
            print("失败重试一下下")
