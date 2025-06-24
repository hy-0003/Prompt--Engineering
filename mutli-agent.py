import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm

# 加载环境变量
load_dotenv()

class DeepSeekClient:
    def __init__(self, model):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages
        }
        data = self.send("chat/completions", payload)
        return data["choices"][0]["message"]["content"].strip()

class Agent:
    def __init__(self, name, model="deepseek-chat"):
        self.name = name
        self.client = DeepSeekClient(model)

    def handle(self, prompt):
        messages = [
            {"role": "system", "content": f"You are {self.name}."},
            {"role": "user", "content": prompt}
        ]
        return self.client.chat(messages)

class SearchAgent(Agent):
    def handle(self, query):
        prompt = f"请联网搜索以下主题的相关文章，并返回要点：\n{query}"
        return super().handle(prompt)

class PoemAgent(Agent):
    def handle(self, materials):
        prompt = f"根据以下资料整合信息，并生成一首中文诗句：\n{materials}"
        return super().handle(prompt)

class ImageAgent(Agent):
    def handle(self, materials):
        prompt = f"根据以下资料描述一幅画面并返回可用于绘图的图像提示：\n{materials}"
        return super().handle(prompt)

class TranslateAgent(Agent):
    def handle(self, text):
        prompt = f"请将以下中文诗句翻译为地道的英文：\n{text}"
        return super().handle(prompt)

class HeadAgent(Agent):
    def __init__(self, name):
        super().__init__(name, model="deepseek-reasoner")

    def distribute_and_review(self, requirements):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始任务拆分")
        start_overall = time.time()
        head_prompt = f"根据用户要求自动拆分任务并给各AI分配指令：\n{requirements}"
        subprompts = self.handle(head_prompt).split("\n")[:4]
        tasks = [
            ("搜索", search_agent, subprompts[0]),
            ("生成诗句", poem_agent, None),
            ("生成图像提示", image_agent, None),
            ("翻译诗句", translate_agent, None)
        ]

        results = {}
        # 按顺序显示进度
        for name, agent, arg in tqdm(tasks, desc="任务进度", unit="step"):
            t0 = time.time()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始 {name}")
            if name == "搜索":
                res = agent.handle(arg)
                results['search'] = res
            elif name == "生成诗句":
                res = agent.handle(results['search'])
                results['poem'] = res
            elif name == "生成图像提示":
                res = agent.handle(results['search'])
                results['image'] = res
            elif name == "翻译诗句":
                res = agent.handle(results['poem'])
                results['translate'] = res
            dt = time.time() - t0
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 完成 {name}，耗时 {dt:.2f} 秒")

        # 聚合
        aggregate = (
            f"=== 中文诗句 ===\n{results['poem']}\n\n"
            f"=== 英文诗句 ===\n{results['translate']}\n\n"
            f"=== 图像提示 ===\n{results['image']}"
        )
        # 审核
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始审核与润色")
        final = self.handle(f"请审核并润色以下内容,不要再说改动说明优化等等：\n{aggregate}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务完成，总耗时 {(time.time() - start_overall):.2f} 秒")
        return final

# 实例化 Agents
head_agent = HeadAgent("DeepSeek 首脑AI")
search_agent = SearchAgent("AI1_搜索", model="deepseek-chat")
poem_agent = PoemAgent("AI2_整合诗句", model="deepseek-chat")
image_agent = ImageAgent("AI3_图片生成提示", model="deepseek-chat")
translate_agent = TranslateAgent("AI4_翻译", model="deepseek-chat")

if __name__ == "__main__":
    user_requirements = (
        "我想生成一首基于最新数学成就的中文诗，附带英文翻译，并生成一幅符合诗意的图像提示。"
    )
    result = head_agent.distribute_and_review(user_requirements)
    print("最终结果:\n", result)

