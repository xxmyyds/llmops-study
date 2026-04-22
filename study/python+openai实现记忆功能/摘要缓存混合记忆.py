# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/21 17:13
# @FileName: 摘要缓存混合记忆.py
from typing import Any

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


class ConversationSummaryBufferMemory:
    def __init__(self, summary: str = '', chat_histories: list = None, max_tokens: int = 300):
        # 旧的摘要
        self.summary = summary
        # 历史对话
        self.chat_histories = [] if chat_histories is None else chat_histories
        # 最大tokens
        self.max_tokens = max_tokens
        self._client = OpenAI(base_url='https://api.deepseek.com')

    @classmethod
    def get_num_tokens(cls, query: str) -> int:
        """计算token"""
        return len(query)

    def save_context(self, human_query: str, ai_content: str):
        """保存传入的新一次对话信息"""
        self.chat_histories.append({'human': human_query, 'ai': ai_content})

        buffer_string = self.get_buffer_string()

        tokens = self.get_num_tokens(buffer_string)

        if tokens > self.max_tokens:
            first_chat = self.chat_histories[0]
            print('新摘要生成中~')
            self.summary = self.summary_text(
                self.summary,
                f"Human: {first_chat.get('human')}\nAI: {first_chat.get('ai')}"
            )
            print('新摘要生成成功:', self.summary)
            del self.chat_histories[0]

    def get_buffer_string(self) -> str:
        """将历史对话转化为字符串"""
        buffer: str = ''
        for chat in self.chat_histories:
            buffer += f"Human:{chat.get('human')}\nAI:{chat.get('ai')}\n\n"
        return buffer.strip()

    def load_memory_variables(self) -> dict[str, Any]:
        """加载记忆变量为一个字典,便于格式化到prompt中"""
        buffer_string = self.get_buffer_string()
        return {
            'chat_history': f"摘要:{self.summary}\n\n历史信息:{buffer_string}\n"
        }

    def summary_text(self, origin_summary: str, new_line: str) -> str:
        """用于将旧的摘要和传入的新对话生成一个新摘要"""
        prompt = f"""你是一个强大的聊天机器人,请根据用户提高的谈话内容,总结摘要,并将其添加到先前提供的摘要当中,
        
        请不要将<example>标签里的数据当成实际数据,这里的数据只是一个示例数据,告诉你该如何生成新摘要.
        
        <example>
        当前摘要: 人类会人工智能对人工智能的看法,人工智能认为人工智能是一股向善的力量
        
        新对话:
        Human: 为什么你认为人工智能是一股向善的力量?
        AI: 因为人工智能会帮助人类充分发挥潜力.
        
        新摘要: 人类会问人工智能对人工智能的看法,人工智能认为人工智能是一股向善的力量,因为它会帮助人类充分发挥潜力.
        </example>
        
        ============================以下的数据是实际需要处理的数据=========================
        
        当前摘要: {origin_summary}
        
        新的对话: {new_line}
        请帮助用户将上面的信息生成新摘要.
        """

        completion = self._client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'content': prompt, 'role': 'user'}
            ],
        )
        return completion.choices[0].message.content


client = OpenAI(base_url='https://api.deepseek.com')
memory = ConversationSummaryBufferMemory('', [], 300)
while True:
    # 获取人类输入
    query = input('Human:')

    # 输入是否为q,如果是则直接退出
    if query == 'quit' or query == 'q':
        break
    memory_variables = memory.load_memory_variables()
    answer_prompt = (
            "你是一个强大的聊天机器人,请根据对应的上下文和用户的提问解决问题\n\n" +
            f"{memory_variables.get('chat_history')}\n\n" +
            f"用户的提问是: {query}"
    )
    # 调用openai大模型
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {'content': answer_prompt, 'role': 'user'}
        ],
        stream=True
    )

    print('AI: ', flush=True, end='')
    ai_content = ''
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        ai_content += content

        print(content, flush=True, end='')
    print('')
    memory.save_context(query, ai_content)
