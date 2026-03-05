#!/usr/bin/env python3
"""SEO+GEO optimization script for fortune-tools"""
import re, os, json

BASE = "/home/msdn/fortune-tools"
OG_IMAGE = "https://fortune-tools.vercel.app/og-image.png"

# Per-page data: (filename, tool_name, title, description, faq_list, howto_steps, has_twitter)
PAGES = [
    {
        "file": "index.html",
        "tool": 「灵算阁」,
        "title": 「灵算阁 - AI算命占卜工具 | 八字算命 塔罗牌 姓名测分」,
        "desc": 「灵算阁提供专业AI八字算命、塔罗牌占卜、姓名测分、周公解梦、今日运势等免费算命工具，传承千年易学智慧。",
        "faq": [
            (「灵算阁的算命工具准确吗？", 「灵算阁融合传统命理学原理与AI分析技术，基于数千年积累的易学体系，提供科学化、系统化的命理分析结果，供用户参考与思考。"),
            (「灵算阁所有工具都免费吗？", 「是的，灵算阁所有工具均完全免费开放使用，包括八字算命、塔罗牌、姓名测分、周公解梦、今日运势等19款工具，无需注册登录。"),
            (「灵算阁的数据会被保存吗？", 「灵算阁不存储任何用户个人信息。所有分析均在浏览器本地完成，您的生日、姓名等信息不会被上传或记录。"),
        ],
        "howto": [
            (「选择工具」, 「在首页浏览19款命理工具，根据需求选择八字算命、塔罗牌、姓名测分等对应工具。"),
            (「输入信息」, 「按页面提示输入姓名、出生日期等基本信息，系统即时生成分析报告。"),
            (「解读结果」, 「阅读AI生成的命理分析报告，结合个人实际情况理解和应用。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "bazi.html",
        "tool": "AI八字算命」,
        "title": "AI八字算命 - 灵算阁 | 免费生辰八字测算」,
        "desc": 「输入出生年月日时，AI精确排出四柱八字，分析天干地支、五行旺衰、十神格局，揭示命运密码。",
        "faq": [
            (「八字算命准确吗？", 「八字命理是中国传统文化中历史最悠久的预测方法之一，有超过3000年历史。本工具基于传统四柱八字原理，通过出生年月日时排出天干地支，结合五行生克理论分析命运走势，结果供参考。"),
            (「如何看八字中的五行？", 「八字由出生年月日时各对应的天干地支组成，共八个字。五行（金木水火土）分布体现个人先天能量格局，旺则为优势，弱则需注意。系统会自动计算各五行比例并可视化展示。"),
            (「免费八字算命和付费有什么区别？", 「本平台提供基础的AI辅助八字分析完全免费，包含四柱排盘、五行分析、十神解读等核心内容。付费命理师通常提供更个性化的解读和运程预测，两者各有侧重。"),
        ],
        "howto": [
            (「输入出生信息」, 「在表单中填写出生年份、月份、日期和出生时辰（如子时、午时等）。"),
            (「点击排盘」, 「点击「排八字「按钮，系统自动计算四柱天干地支和五行属性。"),
            (「查看分析报告」, 「阅读AI生成的五行分析、十神格局和命运解读，了解个人先天命理格局。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "chinese-zodiac.html",
        "tool": 「生肖运势查询」,
        "title": 「生肖运势查询 | 灵算阁 - 十二生肖运势分析」,
        "desc": 「免费在线十二生肖运势查询，根据出生年份查询鼠牛虎兔龙蛇马羊猴鸡狗猪的年度运势。",
        "faq": [
            (「十二生肖是怎么确定的？", 「十二生肖以出生年份的农历年支来确定，12年一循环。如鼠年出生者属鼠，牛年出生者属牛。需注意农历春节前后出生者可能与公历年份不同。"),
            (「生肖运势包含哪些内容？", 「生肖运势通常涵盖年度整体运势、事业财运、感情婚姻、健康养生及本年度需注意的方位、颜色、幸运数字等方面，帮助制定年度规划。"),
            ("2026年哪些生肖最旺？", "2026年为丙午马年，马年生肖中马本命年需戴红，属虎、属狗与马相合运势较佳，具体以个人八字为准，本工具可查询各生肖详细运势。"),
        ],
        "howto": [
            (「选择生肖」, 「从下拉菜单或生肖图标中选择您的出生生肖。"),
            (「查看运势」, 「系统即时显示该生肖当年整体运势评分及各方面详细分析。"),
            (「参考建议」, 「根据运势报告中的建议，合理安排事业、感情等重要事项。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "daily.html",
        "tool": 「今日运势」,
        "title": 「今日运势 - 灵算阁 | 星座生肖每日运势」,
        "desc": 「融合星座与生肖智慧，为你定制今日运势，把握每一天的机遇与方向。",
        "faq": [
            (「今日运势每天都会更新吗？", 「是的，今日运势根据当天日期动态生成，每天提供全新的运势分析，融合星座和生肖的当日影响，帮助你把握当天的机遇和注意事项。"),
            (「每日运势和星座运势有什么不同？", 「每日运势综合了生肖与星座双重体系的当日能量，分析更为全面。星座侧重太阳位置对性格的影响，生肖侧重年支能量，两者结合能提供更立体的当日运势参考。"),
            (「看今日运势需要输入什么信息？", 「输入您的星座或生肖即可获取今日运势分析，包括整体运气、事业财运、感情运势、健康指数及当日幸运色和幸运数字。"),
        ],
        "howto": [
            (「选择星座或生肖」, 「输入您的星座（如白羊座）或出生年份对应的生肖。"),
            (「获取今日运势」, 「系统自动结合当天日期生成专属运势报告。"),
            (「查看当日建议」, 「阅读运势评分、宜忌事项和当日幸运提示，合理安排行程。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "dream.html",
        "tool": 「周公解梦」,
        "title": 「周公解梦 - 灵算阁 | 免费在线解梦」,
        "desc": 「传承周公解梦古籍精髓，输入梦境关键词，为你揭示梦中隐含的天机与预兆。",
        "faq": [
            (「周公解梦有科学依据吗？", 「周公解梦是中国古代流传数千年的梦境解析体系，融合了心理学、象征符号学和传统文化。现代心理学也认为梦境与潜意识密切相关，解梦可作为自我认知和心理探索的工具。"),
            (「如何用周公解梦查询梦境含义？", 「在搜索框中输入梦到的事物关键词，如「蛇」「飞翔」「水「等，系统将从传统解梦典籍中检索相关解释，并提供现代心理学角度的参考解读。"),
            (「梦见死亡或不吉利的事是坏兆头吗？", 「在传统解梦中，梦见死亡往往象征「结束与新生」，并不一定代表不吉利。梦境多为心理状态的投射，建议结合近期生活状况综合理解，不必过度担忧。"),
        ],
        "howto": [
            (「输入梦境关键词」, 「在搜索框中输入您印象最深的梦境内容，如人物、动物、场景等关键词。"),
            (「查看解梦结果」, 「系统从周公解梦典籍中提取相关解释，并提供传统吉凶分析。"),
            (「结合实际理解」, 「参考解梦结果，结合近期心理状态和生活情况，理性分析梦境信息。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "face-reading.html",
        "tool": 「面相分析」,
        "title": 「面相分析入门 | 灵算阁 - 免费面相学指南」,
        "desc": 「免费在线面相学基础知识和分析指南，学习额头、眼神、鼻型、嘴唇等面部特征的命理解读。",
        "faq": [
            (「面相学有科学依据吗？", 「面相学是中国传统命理文化的重要组成部分，通过观察面部特征来分析个人性格与命运走势。现代心理学研究也发现面部表情与性格存在一定关联性，本工具提供传统面相知识供学习参考。"),
            (「面相学主要看哪些部位？", 「传统面相学重点关注三停（额头、鼻子、下巴）、五岳（额、颧骨、下巴、左颊、右颊）以及眼睛、眉毛、鼻梁、嘴唇、耳朵等十二宫位，各部位对应不同的命运领域。"),
            (「面相会随年龄改变吗？", 「是的，面相会随着人生经历和心态变化而改变。古人认为「相由心生」，长期保持积极心态和良好习惯，面相也会相应改善，这与现代医学关于面部表情肌影响外观的研究不谋而合。"),
        ],
        "howto": [
            (「了解面相基础知识」, 「阅读三停、五岳、十二宫位等面相学基础理论介绍。"),
            (「对照面部特征」, 「参考图文说明，对照自己的额头高度、眼型、鼻型、嘴型等面部特征。"),
            (「查看性格解读」, 「根据各部位的面相特征，查看对应的性格分析和命运建议。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "fengshui.html",
        "tool": 「风水罗盘方位测算」,
        "title": 「风水罗盘方位测算 | 灵算阁 - 免费在线风水工具」,
        "desc": 「免费在线风水方位测算工具，输入房屋朝向和个人命卦，计算最佳吉位、旺位和化煞建议。",
        "faq": [
            (「风水是迷信还是科学？", 「风水（堪舆学）是中国古代环境学的重要组成部分，研究地理环境、建筑朝向与人体健康、运势的关系。现代建筑学、环境心理学中也有类似研究，如采光、通风、空间布局对居住者的影响。"),
            (「如何用风水罗盘确定方位？", 「传统风水罗盘通过磁针指北，结合建筑坐向确定八个基本方位（东西南北及四隅）。本工具根据您输入的房屋朝向和出生年份计算命卦，给出适合个人的吉祥方位建议。"),
            (「风水布局对家居有实际影响吗？", 「风水中的许多原则与现代居家设计理念相符，如充足采光、良好通风、整洁有序、家具摆放不阻挡动线等，这些都被证明有助于提升居住舒适度和心理状态。"),
        ],
        "howto": [
            (「输入房屋朝向」, 「选择或输入您房屋大门的朝向方位（如坐北朝南）。"),
            (「输入出生年份」, 「填写出生年份，系统计算您的个人命卦（东四命或西四命）。"),
            (「查看方位建议」, 「获取适合您的吉位（旺财、旺丁方位）和需要注意的煞位，以及相应的布局建议。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "iching.html",
        "tool": 「易经占卜」,
        "title": 「易经占卜 — 在线抛铜钱 | 灵算阁」,
        "desc": 「免费在线易经占卜工具，模拟传统抛铜钱起卦，解读六十四卦卦象与爻辞。",
        "faq": [
            (「易经占卜如何运作？", 「易经占卜通过抛铜钱（或蓍草）随机生成六个爻，组成六十四卦之一。每卦对应特定的自然现象和人生哲理，爻辞进一步细化当前情境的分析，是中国最古老的预测体系。"),
            (「如何理解易经卦象？", 「每个卦由上卦和下卦组成，各代表不同的自然力量（天地雷风水火山泽）。卦象描述当前形势，六个爻从下到上代表事情的发展阶段，变爻处是最关键的转变点。"),
            (「易经占卜一天可以占几次？", 「传统易学认为一事一卦，一天内就同一件事不宜反复起卦，否则容易得到混乱的结果。建议带着清晰的问题专注地占一次，认真思考卦象的指引。"),
        ],
        "howto": [
            (「心中默想问题」, 「在占卜前，清晰地在心中默想您想询问的问题，保持专注。"),
            (「模拟抛铜钱」, 「点击「起卦「按钮，系统模拟传统三枚铜钱投掷六次，生成六个爻。"),
            (「解读卦象」, 「阅读系统生成的卦名、卦象图、卦辞和对应的人生指引建议。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "love.html",
        "tool": 「缘分配对测试」,
        "title": 「缘分配对测试 - 灵算阁 | 姓名缘分测试」,
        "desc": 「输入两人姓名和生日，测算缘分指数、性格互补分析和恋爱建议，免费缘分配对测试。",
        "faq": [
            (「缘分配对测试准确吗？", 「本测试基于姓名五格数理和生辰八字的传统命理配对方法，结合现代心理学性格互补理论，提供趣味性的缘分分析。测试结果供参考，真实感情需要双方共同经营。"),
            (「测试需要输入哪些信息？", 「需要输入两人的姓名（中文）和出生日期，系统将根据姓名笔画数理和出生八字分析两人的五行相合程度、性格互补指数和整体缘分评分。"),
            (「什么样的八字配对最佳？", 「传统命理认为五行互补者缘分深厚，例如对方五行中的强项恰好补足自身的弱项。但感情的维系更重要的是相互理解、尊重和包容，命理配对只是一个参考维度。"),
        ],
        "howto": [
            (「输入双方信息」, 「分别填写两人的姓名和出生年月日。"),
            (「点击测算缘分」, 「系统根据姓名数理和八字信息计算缘分指数。"),
            (「查看配对分析」, 「阅读缘分评分、性格互补分析、相处建议等详细报告。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "lucky-number.html",
        "tool": 「幸运数字计算」,
        "title": 「幸运数字计算 | 灵算阁 - 姓名生日幸运数」,
        "desc": 「根据姓名和生日计算你的幸运数字，融合数字命理学与中国传统吉数理论。",
        "faq": [
            (「幸运数字是怎么计算的？", 「幸运数字基于数字命理学（Numerology）原理，将姓名的字母/笔画数值和出生日期通过特定计算方法归纳为1-9的核心数字，代表个人的生命路径和内在特质。"),
            (「幸运数字有什么用处？", 「幸运数字可用于选择手机号码、车牌、重要日期、房间号等。传统文化认为与个人命数相合的数字能带来更顺畅的能量流动，但现代心理学认为这更多是增强自信心的积极心理暗示。"),
            (「中国传统吉数有哪些？", 「中国传统认为6（路路顺）、8（发财）、9（长长久久）为吉数，而4（死谐音）通常被视为不吉。但从数字命理学角度，每个数字都有其独特含义，需结合个人生命数字综合分析。"),
        ],
        "howto": [
            (「输入姓名和生日」, 「填写您的姓名（中文或英文）和完整出生日期。"),
            (「计算幸运数字」, 「系统自动通过数字命理学公式计算您的生命数字、灵魂数字和幸运数字。"),
            (「应用幸运数字」, 「参考计算结果，在选择重要数字时优先考虑您的幸运数字。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "mbti.html",
        "tool": "MBTI性格测试」,
        "title": "MBTI性格测试 - 灵算阁 | 16型人格免费测试」,
        "desc": 「免费MBTI十六型人格测试，28道精选题目快速测出你的性格类型，含详细性格描述、适合职业、恋爱匹配分析。",
        "faq": [
            ("MBTI测试准确吗？", "MBTI（迈尔斯-布里格斯类型指标）是全球最广泛使用的人格测试之一，基于荣格心理类型理论。研究显示MBTI对理解个人偏好、工作风格和沟通方式有较好的参考价值，但人格是复杂且动态的，测试结果仅供参考。"),
            ("16种MBTI类型是哪些？", "MBTI将人格分为四个维度：外向(E)/内向(I)、感觉(S)/直觉(N)、思维(T)/情感(F)、判断(J)/知觉(P)，组合形成INFP、ENTJ、ISFJ等16种类型，每种类型都有独特的优势和特点。"),
            ("MBTI会随时间改变吗？", "MBTI类型具有一定稳定性，但会随人生经历、成长和环境变化而调整。建议每隔几年重新测试，同时关注测试中各维度的百分比，接近50%的维度说明您在该维度上有较大灵活性。"),
        ],
        "howto": [
            (「开始答题」, 「点击开始，系统提供28道情景选择题，根据第一直觉作答，不要过多思考。"),
            (「完成测试」, 「认真回答所有题目，通常需要5-10分钟，尽量选择最符合真实自己的答案。"),
            (「查看人格报告」, 「获取您的MBTI类型代码和详细报告，包括性格特点、职业建议和人际关系分析。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "mortgage.html",
        "tool": 「房贷计算器」,
        "title": 「房贷计算器 - 灵算阁 | 等额本息/等额本金计算」,
        "desc": 「在线房贷计算器，支持等额本息和等额本金两种还款方式，计算月供、总利息、还款明细表。",
        "faq": [
            (「等额本息和等额本金哪个更划算？", 「等额本息每月还款金额固定，适合收入稳定人群；总利息较多但前期压力小。等额本金前期还款多、后期递减，总利息更少。收入较高且预计提前还款者适合等额本金，普通工薪族适合等额本息。"),
            (「房贷利率如何影响月供？", 「以100万贷款、30年期为例，利率3.5%时月供约4490元，利率4.5%时约5067元，利率5.5%时约5678元。利率每上涨1%，月供增加约600元，30年总利息差距超过20万。本计算器支持自定义利率精确计算。"),
            (「提前还款能节省多少利息？", 「提前还款节省的利息取决于剩余贷款年限和金额。一般来说，贷款初期提前还款效果最好，因为此时剩余本金最多。使用本计算器可以比较不同还款方案的总利息差异，帮助做出最优决策。"),
        ],
        "howto": [
            (「输入贷款信息」, 「填写贷款总额（元）、贷款年限（年）和年利率（%）。"),
            (「选择还款方式」, 「选择等额本息或等额本金还款方式。"),
            (「查看计算结果」, 「系统即时显示每月还款额、总还款额、总利息，并生成完整还款明细表。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "name.html",
        "tool": 「姓名测分」,
        "title": 「姓名测分 - 灵算阁 | 五格剖象姓名分析」,
        "desc": 「五格剖象法精准分析姓名，笔画数理、三才配置、五行属性，全方位解读姓名吉凶。",
        "faq": [
            (「五格剖象法是什么？", 「五格剖象法是由天格、人格、地格、外格、总格五个数理组成的姓名分析系统，通过汉字笔画数计算各格数值，对照数理灵动表判断姓名吉凶，是目前最流行的中文姓名学方法之一。"),
            (「姓名测分高低代表什么？", 「姓名测分反映姓名的数理能量配置，高分（85分以上）表示姓名数理吉配、三才相生；低分可能存在数理相克或格局不佳的情况。但姓名只是命运的参考因素之一，后天努力更为重要。"),
            (「给新生儿起名需要注意什么？", 「好名字需考虑：读音响亮易记、字义积极美好、五格数理吉配、与父姓三才相合、避免生僻字难写字。本工具可帮助验证候选名字的五格配置，但建议同时考虑字义和文化内涵。"),
        ],
        "howto": [
            (「输入姓名」, 「在输入框中填写要分析的中文姓名（姓+名）。"),
            (「查看五格数理」, 「系统自动计算天格、人格、地格、外格、总格的笔画数和数理评分。"),
            (「阅读综合评分」, 「查看姓名总分、各格吉凶分析和三才五行配置建议。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "numerology.html",
        "tool": 「数字命理学」,
        "title": 「数字命理学计算 | 灵算阁 - 生命数字分析」,
        "desc": 「免费在线数字命理学工具，根据生日计算生命数字（Life Path Number），解析人生使命和性格特质。",
        "faq": [
            (「数字命理学和中国数字文化有什么关系？", 「数字命理学（Numerology）源于古希腊毕达哥拉斯学派，认为数字蕴含宇宙真理。中国传统文化也有深厚的数字哲学，如八卦、九宫格、五行等均以数字为基础，本工具融合了东西方数字文化精髓。"),
            (「生命数字是什么意思？", 「生命数字（Life Path Number）通过将出生日期的所有数字相加直到得到个位数（1-9）或主数（11、22、33）来计算，代表个人的核心性格特质、人生目标和潜在天赋。"),
            (「数字命理学能预测未来吗？", 「数字命理学更多是一种自我认知工具，帮助了解个人优势、挑战和人生主题，而非精确预测具体事件。通过理解自己的核心数字，可以更有意识地做出与自身天赋和使命相契合的选择。"),
        ],
        "howto": [
            (「输入出生日期」, 「填写完整的出生年月日（如：1990年6月15日）。"),
            (「计算生命数字」, 「系统自动将出生日期数字相加并归纳为1-9的生命数字。"),
            (「阅读命理解析」, 「查看您的生命数字含义、性格特质、人生使命和适合的发展方向。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "palm.html",
        "tool": 「手相分析」,
        "title": 「手相分析入门 | 灵算阁 - 免费手相学指南」,
        "desc": 「免费在线手相分析指南，学习生命线、感情线、智慧线、事业线等主要掌纹的命理解读。",
        "faq": [
            (「手相学看哪只手？", 「传统手相学认为「左手天生右手后天」，即左手代表先天命运和潜力，右手反映后天努力和实际发展。现代手相学建议两手对比分析，看主手（惯用手）了解实际生活状态，看非主手了解先天潜能。"),
            (「手相主要看哪几条线？", 「手相学重点分析四条主线：生命线（拇指下方弧线，代表健康和活力）、感情线（小指下方横线，代表情感生活）、智慧线（中间斜线，代表思维方式）、事业线（纵向中线，代表事业发展）。"),
            (「手相会改变吗？", 「是的，手相会随年龄和生活经历变化而改变。古人认为「命运掌握在自己手中」，通过改变行为习惯、心态和努力方向，掌纹也会相应调整，这体现了命运的可变性。"),
        ],
        "howto": [
            (「了解手相基础」, 「阅读生命线、感情线、智慧线等主要掌纹的位置说明和图示。"),
            (「观察自己的掌纹」, 「在自然光下观察惯用手，对照图示找到各条主线和特殊纹路。"),
            (「查看掌纹解读」, 「根据各线的长短、深浅和走向，查看对应的性格分析和命运建议。"),
        ],
        "has_twitter": True,
    },
    {
        "file": "pastlife.html",
        "tool": 「前世今生测试」,
        "title": 「前世今生测试 - 灵算阁 | 探索你的前世身份」,
        "desc": 「输入姓名和生日，探索你的前世身份，了解今生使命。趣味前世今生测试，揭示灵魂的轮回密码。",
        "faq": [
            (「前世今生测试有依据吗？", 「前世今生理论源于佛教、道教的轮回信仰和西方灵性文化，认为灵魂经历多次转世。本测试以姓名数理和生辰能量为基础，通过趣味化方式探索「如果有前世，你可能是谁」，是一种寓教于乐的文化体验。"),
            (「测试会告诉我前世是什么人吗？", 「测试根据您的姓名和生日生成个性化的「前世故事」，包括前世身份、所处时代、主要性格特征和今生可能带来的影响。这是基于数字命理和文化象征的创意解读，供娱乐和自我思考参考。"),
            (「前世今生测试和催眠回溯有什么区别？", 「催眠回溯是由专业催眠治疗师引导的深层意识探索方法，而本测试是基于出生数据的算法生成，快捷便利。两者都是探索内心世界的工具，但深度和方式不同，前者更为个性化和深入。"),
        ],
        "howto": [
            (「输入个人信息」, 「填写您的姓名和出生年月日。"),
            (「生成前世故事」, 「点击测试按钮，系统根据您的数据生成专属的前世身份解读。"),
            (「探索今生连接」, 「阅读前世故事，思考其中描述的性格特质和今生使命是否与您产生共鸣。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "salary.html",
        "tool": 「工资税后计算器」,
        "title": 「工资税后计算器 - 灵算阁 | 五险一金个税计算」,
        "desc": 「在线工资税后计算器，输入税前工资自动计算五险一金、个人所得税、到手工资，支持不同城市社保基数。",
        "faq": [
            (「五险一金是什么？如何计算？", 「五险一金包括养老保险、医疗保险、失业保险、工伤保险、生育保险和住房公积金。个人部分通常需缴纳工资的10-12%（养老8%+医疗2%+失业0.5%+公积金1%-12%），具体比例因城市而异。"),
            (「个人所得税如何计算？", 「中国个税采用累进税率制，月应纳税所得额=月收入-5000元（免征额）-五险一金个人部分-专项附加扣除。适用税率从3%到45%共7级，本计算器支持输入专项附加扣除额精确计算。"),
            (「不同城市社保基数有什么区别？", 「各城市社保缴纳基数上下限不同，通常以上一年度当地职工平均工资为基准。超过上限部分按上限缴纳，低于下限部分按下限缴纳。本工具支持选择主要城市或自定义社保基数进行精确计算。"),
        ],
        "howto": [
            (「输入税前工资」, 「填写您的月税前工资（元）。"),
            (「选择城市和参数」, 「选择所在城市，系统自动填入对应的社保比例和公积金比例，也可手动调整。"),
            (「查看到手工资」, 「系统即时计算五险一金、个税金额和实际到手工资，并显示扣款明细。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "tarot.html",
        "tool": 「塔罗牌占卜」,
        "title": 「塔罗牌占卜 - 灵算阁 | 78张全牌阵在线占卜」,
        "desc": "78张大小阿尔卡纳全牌阵，每日一卡或三卡占卜，正逆位详细解读，指引迷途方向。",
        "faq": [
            (「塔罗牌有多少张？各代表什么？", 「标准塔罗牌共78张，分为大阿尔卡纳（22张，如愚者、魔法师、命运之轮等）和小阿尔卡纳（56张，分权杖、圣杯、宝剑、星币四组）。大阿尔卡纳代表重大人生主题，小阿尔卡纳代表日常事务。"),
            (「塔罗牌正位和逆位有什么区别？", 「塔罗牌正位通常代表该牌能量的正面、直接表达；逆位（倒置）则表示能量受阻、延迟或需内化反思。例如太阳牌正位代表成功喜悦，逆位可能提示需要更多努力或内在成长。"),
            (「每天占卜塔罗有用吗？", 「每日一卡是很好的自我反思习惯，抽到的牌作为当天的思考主题，帮助关注某个特定能量或课题。建议早晨抽牌，带着问题「今天我需要关注什么？"，晚上回顾牌义与当天经历的联系。"),
        ],
        "howto": [
            (「心中默想问题」, 「在抽牌前，清晰地在心中默想您想探询的问题或当天的主题。"),
            (「选择牌阵」, 「选择单卡（今日指引）或三卡（过去-现在-未来）占卜方式。"),
            (「解读牌义」, 「点击翻牌查看所抽塔罗牌，阅读正逆位解读，结合当前情境理解牌的信息。"),
        ],
        "has_twitter": False,
    },
    {
        "file": "zodiac.html",
        "tool": 「十二星座运势查询」,
        "title": 「十二星座运势查询 | 灵算阁 - 星座每日运势」,
        "desc": 「免费在线十二星座运势查询，白羊座至双鱼座每日星座运势，含爱情、事业、财运详细分析。",
        "faq": [
            (「十二星座是怎么划分的？", 「十二星座按太阳在黄道十二宫的位置划分，对应每年固定的时间段。如白羊座（3/21-4/19）、金牛座（4/20-5/20）...双鱼座（2/19-3/20）。出生时太阳所在星座即为您的太阳星座，也是通常所说的星座。"),
            (「星座运势准确吗？", 「星座运势基于占星学原理，通过行星运行与十二星座的相位关系来分析能量趋势。作为一种文化传承和自我反思工具，运势分析提供思考框架，实际结果仍取决于个人选择和行动。"),
            (「星座配对最佳的是哪些？", 「传统占星中同元素星座（火象：白羊、狮子、射手；土象：金牛、处女、摩羯；风象：双子、天秤、水瓶；水象：巨蟹、天蝎、双鱼）相处和谐，互补元素（如火与风、土与水）也常有吸引力。"),
        ],
        "howto": [
            (「选择您的星座」, 「从十二星座列表中点击选择您的太阳星座。"),
            (「查看今日运势」, 「系统显示当日星座运势评分、详细分析和幸运提示。"),
            (「参考运势建议」, 「阅读爱情、事业、财运各维度的运势建议，合理安排当日重要事项。"),
        ],
        "has_twitter": True,
    },
]

def make_twitter_tags(title, desc):
    return f'''<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">'''

def make_software_schema(tool_name, desc):
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool_name,
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CNY"},
        "description": desc,
        "url": "https://fortune-tools.vercel.app/"
    }
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

def make_faq_schema(faq_list):
    items = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_list]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

def make_howto_schema(tool_name, steps):
    step_objs = [{"@type": "HowToStep", "name": name, "text": text} for name, text in steps]
    schema = {"@context": "https://schema.org", "@type": "HowTo", "name": f「如何使用{tool_name}", "step": step_objs}
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

def make_breadcrumb_schema(tool_name, filename):
    slug = filename.replace(".html", "")
    url = f"https://rorojiao.github.io/fortune-tools/{filename}"
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": 「灵算阁」, "item": "https://rorojiao.github.io/fortune-tools/"},
            {"@type": "ListItem", "position": 2, "name": tool_name, "item": url}
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

def make_faq_html(faq_list):
    items = ""
    for q, a in faq_list:
        items += f'''    <div class="faq-item">
      <h3 class="faq-q">{q}</h3>
      <p class="faq-a">{a}</p>
    </div>
'''
    return f'''<!-- FAQ Section -->
<div class="faq-section" style="max-width:800px;margin:40px auto;padding:20px;background:rgba(20,10,40,0.6);border-radius:16px;border:1px solid rgba(255,215,0,0.1);">
  <h2 style="color:#d4a84b;font-size:1.2em;margin-bottom:16px;text-align:center;">常见问题</h2>
{items}</div>
'''

def make_faq_html_light(faq_list):
    """For pages that use light theme (Fortune Tools pages)"""
    items = ""
    for q, a in faq_list:
        items += f'''    <div style="margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid #eee;">
      <h3 style="font-size:1em;color:#333;margin-bottom:8px;">{q}</h3>
      <p style="font-size:0.9em;color:#666;line-height:1.7;margin:0;">{a}</p>
    </div>
'''
    return f'''<!-- FAQ Section -->
<div style="max-width:800px;margin:40px auto;padding:24px;background:#f9f9f9;border-radius:12px;">
  <h2 style="font-size:1.1em;color:#333;margin-bottom:20px;text-align:center;">常见问题</h2>
{items}</div>
'''

DARK_THEME_FILES = {"bazi.html", "daily.html", "dream.html", "love.html", "mbti.html",
                     "mortgage.html", "name.html", "pastlife.html", "salary.html", "tarot.html", "index.html"}

def process_file(page):
    filepath = os.path.join(BASE, page["file"])
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # 1. Add twitter tags if missing
    if not page["has_twitter"]:
        twitter_block = make_twitter_tags(page["title"], page["desc"])
        # Insert before </head>
        if '<meta name="twitter:card"' not in content:
            content = content.replace('</head>', twitter_block + '\n</head>', 1)
            changes.append("twitter cards")
    else:
        # Upgrade existing twitter:card to summary_large_image if needed
        if 'content="summary"' in content and 'twitter:card' in content:
            content = content.replace('content="summary"', 'content="summary_large_image"', 1)
            changes.append("upgraded twitter:card")
        # Add missing twitter:title/description/image if not present
        twitter_additions = ""
        if '<meta name="twitter:title"' not in content:
            twitter_additions += f'\n<meta name="twitter:title" content="{page["title"]}">'
        if '<meta name="twitter:description"' not in content:
            twitter_additions += f'\n<meta name="twitter:description" content="{page["desc"]}">'
        if '<meta name="twitter:image"' not in content:
            twitter_additions += f'\n<meta name="twitter:image" content="{OG_IMAGE}">'
        if twitter_additions:
            # Insert after twitter:card line
            content = re.sub(r'(<meta name="twitter:card"[^>]*>)', r'\1' + twitter_additions, content, count=1)
            changes.append("twitter title/desc/image")

    # 2. Add SoftwareApplication schema
    if "SoftwareApplication" not in content:
        sw_schema = make_software_schema(page["tool"], page["desc"])
        content = content.replace('</head>', sw_schema + '\n</head>', 1)
        changes.append("SoftwareApplication schema")

    # 3. Add FAQPage schema
    if "FAQPage" not in content:
        faq_schema = make_faq_schema(page["faq"])
        content = content.replace('</head>', faq_schema + '\n</head>', 1)
        changes.append("FAQPage schema")

    # 4. Add HowTo schema
    if "HowTo" not in content:
        howto_schema = make_howto_schema(page["tool"], page["howto"])
        content = content.replace('</head>', howto_schema + '\n</head>', 1)
        changes.append("HowTo schema")

    # 4b. Add BreadcrumbList schema (skip index.html - single page has no breadcrumb)
    if "BreadcrumbList" not in content and page["file"] != "index.html":
        bc_schema = make_breadcrumb_schema(page["tool"], page["file"])
        content = content.replace('</head>', bc_schema + '\n</head>', 1)
        changes.append("BreadcrumbList schema")

    # 5. Add FAQ HTML section before </body> (but after <!-- internal-links --> if present)
    if "faq-section" not in content and "FAQ Section" not in content:
        is_dark = page["file"] in DARK_THEME_FILES
        faq_html = make_faq_html(page["faq"]) if is_dark else make_faq_html_light(page["faq"])
        # Insert before <!-- Analytics --> or before </body>
        if "<!-- Analytics -->" in content:
            content = content.replace("<!-- Analytics -->", faq_html + "\n<!-- Analytics -->", 1)
        elif "<!-- AdSense" in content:
            content = content.replace("<!-- AdSense", faq_html + "\n<!-- AdSense", 1)
        else:
            content = content.replace("</body>", faq_html + "\n</body>", 1)
        changes.append("FAQ HTML section")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return page["file"], changes

def update_sitemap():
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    # Collect all page files from PAGES plus any not covered
    all_html = [p["file"] for p in PAGES]
    entries = []
    for f in all_html:
        priority = "1.0" if f == "index.html" else "0.8"
        url = f"https://rorojiao.github.io/fortune-tools/{f}"
        entries.append(f"  <url><loc>{url}</loc><lastmod>2026-03-06</lastmod><priority>{priority}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(entries) + "\n"
    xml += "</urlset>\n"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("✓ sitemap.xml updated")

# Process all pages
results = []
for page in PAGES:
    fname, changes = process_file(page)
    results.append((fname, changes))
    print(f"✓ {fname}: {', '.join(changes) if changes else 'no changes'}")

update_sitemap()
total = len(results)
print(f"\nDone! Processed {total} pages.")
