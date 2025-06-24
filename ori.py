import os
import json
import requests
from dotenv import load_dotenv
from PIL import Image
import io
import time


# 加载环境变量
load_dotenv()


# model:DeepSeek-V3-0324 to deepseek-chat
# model:DeepSeek-R1-0528 to deepseek-reasoner


class DeepSeekCRISPEGenerator:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_with_crispe(self, capacity, role, insight, statement, personality, experiment, context, requirement, model="deepseek-chat"):
        # 构建CRISPE提示模板
        prompt = (
            f"[Capacity] {capacity}\n"                # 能力定位
            f"[Role] {role}\n"                        # 角色设定
            f"[Insight] {insight}\n"                  # 背景洞察
            f"[Statement] {statement}\n"              # 任务陈述
            f"[Personality] {personality}\n"          # 输出个性
            f"[Experiment] {experiment}\n"            # 实验要求
            f"[Context] {context}\n"                  # 更多信息
            f"[Requirement] {requirement}\n"          # 额外要求
        )
        
        # 构建请求数据
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个专业的人工智能助手，严格遵循CRISPE框架执行任务。还可能会增加“内容”框架以及“要求”框架。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,   # 值越大，生成的文本越随机，越创造性但是不稳定
            "max_tokens": 2000,
            "top_p": 0.9
        }
        
        # 发送API请求
        response = requests.post(
            url=f"{self.base_url}/chat/completions",
            headers=self.headers,
            data=json.dumps(payload))
        
        # 检查响应状态
        if response.status_code != 200:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
        # 解析响应
        result = response.json()
        return result['choices'][0]['message']['content']
    

    def generate_and_print(self, crispe_params, model="deepseek-chat"):
        start_time = time.time()
        
        print("\n" + "="*60)
        print("CRISPE 参数配置:")
        print("="*60)
        for key, value in crispe_params.items():
            print(f"{key.upper()}: {value}")
        
        print("\n" + "="*60)
        print("模型响应:")
        print("="*60)
        
        try:
            response = self.generate_with_crispe(model=model, **crispe_params)
            print(response)
            
            # 性能统计
            end_time = time.time()
            print("\n" + "-"*60)
            print(f"生成完成 | 耗时: {end_time - start_time:.2f}秒")
            
        except Exception as e:
            print(f"错误: {str(e)}")



generator = DeepSeekCRISPEGenerator()


# CRISPE参数配置 - 数学家
architecture_params = {
    "capacity": "你是一位精通欧几里得几何的数学家，特别擅长平面几何的演绎证明",
    "role": "正在编写《几何原本》的现代补充卷",
    "insight": "学生普遍理解困难在于面积关系的可视化",
    "statement": "严格证明勾股定理，并提供可视化辅助",
    "personality": "避免使用现代代数符号，保持古典几何纯粹性",
    "experiment": "1. 构造辅助几何图形2. 建立面积等价关系3. 使用全等三角形性质4. 推导面积等式5. 得出最终结论",
    "context": "无",
    "requirement": "无"
}


print("正在生成技术架构方案...")
generator.generate_and_print(architecture_params)