# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break
from toolbox import apply_gpt_academic_string_mask_langbased
from toolbox import build_gpt_academic_masked_string_langbased
from textwrap import dedent


def get_core_functions():
    return {
        "学术语料润色": {
            # [1*] 前缀字符串，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等。
            #      这里填一个提示词字符串就行了，这里为了区分中英文情景搞复杂了一点
            "Prefix":   build_gpt_academic_masked_string_langbased(
                text_show_english=r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, "
                r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. "
                r"Firstly, you should provide the polished paragraph. "
                r"Secondly, you should list all your modification and explain the reasons to do so in markdown table.",
                text_show_chinese=r"作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，"
                r"同时分解长句，减少重复，并提供改进建议。请先提供文本的更正版本，然后在markdown表格中列出修改的内容，并给出修改的理由:"
            ) + "\n\n",
            # [2*] 后缀字符串，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # [3] 按钮颜色 (可选参数，默认 secondary)
            "Color":    r"secondary",
            # [4] 按钮是否可见 (可选参数，默认 True，即可见)
            "Visible": True,
            # [5] 是否在触发时清除历史 (可选参数，默认 False，即不处理之前的对话历史)
            "AutoClearHistory": True,
            # [6] 文本预处理 （可选参数，默认 None，举例：写个函数移除所有的换行符）
            "PreProcess": None,
        },
        "总结绘制脑图": {
            "Visible": False,
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix":   '''"""\n\n''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":
                # dedent() 函数用于去除多行字符串的缩进
                dedent("\n\n"+r'''
                    """

                    使用mermaid flowchart对以上文本进行总结，概括上述段落的内容以及内在逻辑关系，例如：

                    以下是对以上文本的总结，以mermaid flowchart的形式展示：
                    ```mermaid
                    flowchart LR
                        A["节点名1"] --> B("节点名2")
                        B --> C{"节点名3"}
                        C --> D["节点名4"]
                        C --> |"箭头名1"| E["节点名5"]
                        C --> |"箭头名2"| F["节点名6"]
                    ```

                    注意：
                    （1）使用中文
                    （2）节点名字使用引号包裹，如["Laptop"]
                    （3）`|` 和 `"`之间不要存在空格
                    （4）根据情况选择flowchart LR（从左到右）或者flowchart TD（从上到下）
                '''),
        },
        "查找语法错误": {
            "AutoClearHistory": True,
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # 预处理：清除换行符
        },
        "中译英": {
            "AutoClearHistory": True,
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },
        "学术英中互译": {
            "AutoClearHistory": True,
            "Prefix":   build_gpt_academic_masked_string_langbased(
                text_show_chinese=r"I want you to act as a scientific English-Chinese translator, "
                r"I will provide you with some paragraphs in one language "
                r"and your task is to accurately and academically translate the paragraphs only into the other language. "
                r"Do not repeat the original provided paragraphs after translation. "
                r"You should use artificial intelligence tools, "
                r"such as natural language processing, and rhetorical knowledge "
                r"and experience about effective writing techniques to reply. "
                r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:",
                text_show_english=r"你是经验丰富的翻译，请把以下学术文章段落翻译成中文，"
                r"并同时充分考虑中文的语法、清晰、简洁和整体可读性，"
                r"必要时，你可以修改整个句子的顺序以确保翻译后的段落符合中文的语言习惯。"
                r"你需要翻译的文本如下："
            ) + "\n\n",
            "Suffix":   r"",
        },
        "英译中": {
            "AutoClearHistory": True,
            "Prefix":   r"翻译成地道的中文：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },
        "找图片": {
            "AutoClearHistory": True,
            "Prefix":   r"我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，"
                        r"然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },
        "解释代码": {
            "Prefix":   r"请解释以下代码：" + "\n```\n",
            "Suffix":   "\n```\n",
            "AutoClearHistory": True,
        },
        "总结": {
            "Prefix":   r"请总结以下文本：" + "\n\n",
            "Suffix":   "",
            "AutoClearHistory": True,
        },
        "OCR校正": {
            "Prefix":   r"以下是一段OCR出来的文字，请校正错误：" + "\n\n",
            "Suffix":   "",
            "AutoClearHistory": True,
        },
        "化简答案": {
            "Prefix":   r"",
            "Suffix":   "\n\n你是一名即将期末考试的大学生，请阅读以上问题与解析，尽可能精简出一份方便记忆的答案：",
            "AutoClearHistory": True,
        },
        "提取重点": {
            "Prefix":   r"请提取以下文本的重点：" + '\n\n',
            "Suffix":   "",
            "AutoClearHistory": True,
        },
        "降重": {
            "Prefix":   r"请将这段话改写，通过调整语序增减字数，替换同义词等方式，避免与原文出现连续 8 个字相同的句子，使这段话更加具有逻辑符合论文的规范：" + '\n\n',
            "Suffix":   "",
            "AutoClearHistory": True,
        },
        "DeepSeekMath解题（记得切换模型）":{
            "Prefix":   r"",
            "Suffix":   "\n 请通过逐步推理来解答问题，并把最终答案放置于\\boxed{} 中。",
            "AutoClearHistory": True,
        },
        "DeepSeekMath生成Mathematica（记得切换模型）": {
            "Prefix":   r"",
            "Suffix":   "\n 请通过逐步推理来生成Mathematica代码解答问题。",
            "AutoClearHistory": True,
        },
        "参考文献转Bib": {
            "AutoClearHistory": True,
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style."
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly."
                        r"Items need to be transformed:" + "\n\n",
            "Visible":  False,
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # 热更新prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + \
            inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional[additional_fn]:
            if core_functional[additional_fn]["PreProcess"] is not None:
                inputs = core_functional[additional_fn]["PreProcess"](
                    inputs)  # 获取预处理函数（如果有的话）
        # 为字符串加上上面定义的前缀和后缀。
        inputs = apply_gpt_academic_string_mask_langbased(
            string=core_functional[additional_fn]["Prefix"] +
            inputs + core_functional[additional_fn]["Suffix"],
            lang_reference=inputs,
        )
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
            chatbot.append((f'[{additional_fn}] 是否已清空历史消息？',
                           "[Local Message] 已清空所有历史消息。"))
        return inputs, history


if __name__ == "__main__":
    t = get_core_functions()["总结绘制脑图"]
    print(t["Prefix"] + t["Suffix"])
