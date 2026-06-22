#!/usr/bin/env python3
"""Generate 4 World Cup prediction reports for June 23, 2026 - Group H Round 2"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OBSIDIAN_DIR = r"D:\我的坚果云\OB笔记\自媒体\fwc2026"
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(OBSIDIAN_DIR, exist_ok=True)

# ============================================================
# COMMON DATA
# ============================================================

GROUP_STANDINGS = """<table class="standings">
<tr><th>#</th><th>球队</th><th>赛</th><th>胜</th><th>平</th><th>负</th><th>进球</th><th>失球</th><th>净胜</th><th>积分</th></tr>
<tr><td>1</td><td>英格兰</td><td>1</td><td>1</td><td>0</td><td>0</td><td>4</td><td>2</td><td>+2</td><td><strong>3</strong></td></tr>
<tr><td>2</td><td>哥伦比亚</td><td>1</td><td>1</td><td>0</td><td>0</td><td>3</td><td>1</td><td>+2</td><td><strong>3</strong></td></tr>
<tr><td>3</td><td>加纳</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>+1</td><td><strong>3</strong></td></tr>
<tr><td>4</td><td>葡萄牙</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td><strong>1</strong></td></tr>
<tr><td>5</td><td>刚果(金)</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td><strong>1</strong></td></tr>
<tr><td>6</td><td>巴拿马</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>-1</td><td><strong>0</strong></td></tr>
<tr><td>7</td><td>乌兹别克斯坦</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>3</td><td>-2</td><td><strong>0</strong></td></tr>
<tr><td>8</td><td>克罗地亚</td><td>1</td><td>0</td><td>0</td><td>1</td><td>2</td><td>4</td><td>-2</td><td><strong>0</strong></td></tr>
</table>"""

# ============================================================
# MATCH 1: Portugal vs Uzbekistan
# ============================================================

MATCH1 = {
    "filename": "report-2026-06-22-portugal-uzbekistan",
    "md_filename": "2026-06-22-portugal-uzbekistan-prediction",
    "title": "葡萄牙 vs 乌兹别克斯坦",
    "group": "H组 小组赛第2轮",
    "date": "2026-06-22",
    "time": "12:00 (当地时间18:00)",
    "venue": "NRG体育场，休斯顿 · 中立场地",
    "odds": "葡萄牙胜 2/9 | 平局 6/1 | 乌兹别克斯坦胜 14/1",
    "fifa_ranks": "葡萄牙 #5 vs 乌兹别克斯坦 #50",
    "probability": "葡萄牙胜 72% / 平局 18% / 乌兹别克斯坦胜 10%",
    "confidence": "高",
    "score_pred": "3-0",
    "score_prob": "约25%",
    "alt1": "2-0 (约20%)",
    "alt2": "4-1 (约15%)",
    "xG_range": "葡萄牙 xG 2.5-3.2 / 乌兹别克斯坦 xG 0.3-0.7 / 总 xG 2.8-3.9",

    "body_html": r"""
    <div class="section">
        <h2>近期状态（对手强度校准后）</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇹 葡萄牙</h3>
                <p><strong>Tier 1-2 (FIFA前50):</strong> 1-1 刚果(金)(#46) / 2-1 尼日利亚(~#40) / 2-1 智利(~#35) / 2-0 美国(#17) / 0-0 墨西哥(#14)</p>
                <p>近5场: 3胜2平，场均进1.4球失0.8球。首轮意外平刚果(金)后，马丁内斯需要更果断的进攻输出。</p>
            </div>
            <div class="col">
                <h3>🇺🇿 乌兹别克斯坦</h3>
                <p><strong>Tier 1-2:</strong> 1-3 哥伦比亚(#13) / 1-2 荷兰(#8) / 0-2 加拿大(#30)</p>
                <p>近5场: 1胜1平3负，世界杯首秀1-3落败，面对前20球队全部失球≥2。0-0 委内瑞拉 / 3-1 加蓬 为对阵弱旅数据，不可直接迁移。</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>球员覆盖（16-20人/队）</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇹 葡萄牙核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>国家队进球/出场</th></tr>
                    <tr><td>Cristiano Ronaldo (C)</td><td>ST</td><td>41</td><td>Al-Nassr</td><td>143/227</td></tr>
                    <tr><td>Bruno Fernandes</td><td>AM</td><td>31</td><td>Man United</td><td>核心组织</td></tr>
                    <tr><td>Bernardo Silva</td><td>RW</td><td>31</td><td>Man City</td><td>创造力核心</td></tr>
                    <tr><td>Rafael Leão</td><td>LW</td><td>27</td><td>Milan</td><td>边路爆点</td></tr>
                    <tr><td>João Neves</td><td>CM</td><td>21</td><td>PSG</td><td>首轮进球</td></tr>
                    <tr><td>Diogo Costa</td><td>GK</td><td>26</td><td>Porto</td><td>首发门将</td></tr>
                    <tr><td>Rúben Dias</td><td>CB</td><td>29</td><td>Man City</td><td>防守核心</td></tr>
                    <tr><td>Nuno Mendes</td><td>LB</td><td>24</td><td>PSG</td><td>左路推进</td></tr>
                    <tr><td>Vitinha</td><td>CM</td><td>26</td><td>PSG</td><td>中场控场</td></tr>
                    <tr><td>Gonçalo Ramos</td><td>ST</td><td>25</td><td>PSG</td><td>替补中锋</td></tr>
                    <tr><td>João Cancelo</td><td>RB</td><td>32</td><td>Barcelona</td><td>边卫轮换</td></tr>
                    <tr><td>Francisco Conceição</td><td>RW</td><td>23</td><td>Juventus</td><td>速度替补</td></tr>
                    <tr><td>Pedro Neto</td><td>LW</td><td>26</td><td>Chelsea</td><td>边路突击</td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇺🇿 乌兹别克斯坦核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>国家队进球/出场</th></tr>
                    <tr><td>Eldor Shomurodov (C)</td><td>ST</td><td>30</td><td>Başakşehir</td><td>44/92</td></tr>
                    <tr><td>Abbosbek Fayzullaev</td><td>AM</td><td>22</td><td>Başakşehir</td><td>首轮进球</td></tr>
                    <tr><td>Utkir Yusupov</td><td>GK</td><td>35</td><td>Navbahor</td><td>首发门将</td></tr>
                    <tr><td>Abdukodir Khusanov</td><td>CB</td><td>22</td><td>Man City</td><td>防线核心</td></tr>
                    <tr><td>Otabek Shukurov</td><td>DM</td><td>30</td><td>Baniyas</td><td>中场屏障</td></tr>
                    <tr><td>Jaloliddin Masharipov</td><td>AM</td><td>30</td><td>--</td><td>经验老将</td></tr>
                    <tr><td>Oston Urunov</td><td>RW</td><td>25</td><td>Persepolis</td><td>边路突击</td></tr>
                    <tr><td>Khojiakbar Alijonov</td><td>RB</td><td>29</td><td>Pakhtakor</td><td>边路防守</td></tr>
                    <tr><td>Rustam Ashurmatov</td><td>CB</td><td>29</td><td>Esteghlal</td><td>中卫搭档</td></tr>
                    <tr><td>Odiljon Xamrobekov</td><td>CM</td><td>30</td><td>Tractor</td><td>中场覆盖</td></tr>
                    <tr><td>Igor Sergeev</td><td>ST</td><td>33</td><td>Persepolis</td><td>经验前锋</td></tr>
                    <tr><td>Azizbek Amonov</td><td>FW</td><td>28</td><td>Bukhara</td><td>替补前锋</td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 乌兹别克斯坦世界杯首秀球员占比>90%，大赛经验严重不足——所有数据需按0.70-0.75系数打折。</p>
    </div>

    <div class="section">
        <h2>主教练综合能力评估</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇹 Roberto Martínez</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>西班牙</td></tr>
                    <tr><td>执教时长</td><td>2023年至今</td></tr>
                    <tr><td>战术哲学</td><td>控球主导 + 边路过载 (4-3-3)</td></tr>
                    <tr><td>世界杯成绩</td><td>2022八强(比利时), 2018季军(比利时)</td></tr>
                    <tr><td>Tier 1胜率</td><td>~40%</td></tr>
                    <tr><td>战术灵活性</td><td>7/10</td></tr>
                    <tr><td>大赛压力应对</td><td>8/10</td></tr>
                    <tr><td>临场决策</td><td>7/10</td></tr>
                    <tr><td>综合等级</td><td><strong>A级 (7.1/10)</strong></td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇺🇿 Fabio Cannavaro</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>意大利</td></tr>
                    <tr><td>执教时长</td><td>2025年末至今</td></tr>
                    <tr><td>战术哲学</td><td>紧凑防守 + 快速转换 (4-5-1)</td></tr>
                    <tr><td>世界杯成绩</td><td>首次执教世界杯(球员时期2006冠军)</td></tr>
                    <tr><td>Tier 1胜率</td><td>0% (样本极小)</td></tr>
                    <tr><td>战术灵活性</td><td>5/10</td></tr>
                    <tr><td>大赛压力应对</td><td>未知(执教经验不足)</td></tr>
                    <tr><td>临场决策</td><td>5/10</td></tr>
                    <tr><td>综合等级</td><td><strong>C级 (4.8/10)</strong></td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 教练博弈：Martínez(A级) vs Cannavaro(C级)，差距≥2级。Martínez执教过2届世界杯并获季军，Cannavaro球员时期虽伟大但执教资历浅。概率偏向葡萄牙3-5%。</p>
    </div>

    <div class="section">
        <h2>教练视角：H组出线形势推演</h2>
        <div class="coach-view">
            <h3>🔄 我是葡萄牙主教练Roberto Martínez——</h3>
            <p><strong>小组形势：</strong>H组8队竞争激烈。首轮被刚果(金)逼平(1-1)，目前仅积1分排第4。哥伦比亚和英格兰均已3分领先。本场对乌兹别克斯坦(0分，#50)是"必须赢"的比赛，不容任何闪失。</p>
            <p><strong>本场战略：必须赢，且兼顾净胜球。</strong>理由：如不能击败最弱对手，出线形势将完全失控。同时需要积累净胜球，为第3轮对哥伦比亚(#13)留出缓冲空间。</p>
            <p><strong>出线路径：</strong>最优6分(本场+末轮胜哥伦比亚)，现实目标5分(本场胜+平哥伦比亚)确保小组前4晋级。最坏场景：本场再平则仅2分，末轮必须击败哥伦比亚才能晋级，极度被动。</p>
            <p><strong>赛程策略：</strong>第1场已平→本场全力进攻→第3场视积分形势调整(如已稳妥可轮换)。</p>
            <p><strong>针对性策略：</strong>对乌兹别克斯坦(C级教练+防守体系)用高位压迫+边路过载破密集防守。对哥伦比亚(#13，3分)属"6分战"，必须对标詹姆斯·罗德里格斯和路易斯·迪亚斯做针对性部署。</p>
            <p><strong>B计划：</strong>如果前30分钟无法破门→上Gonçalo Ramos双前锋，增加禁区人数；核心进攻体系失效→利用定位球优势(鲁本·迪亚斯头球)。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 我是乌兹别克斯坦主教练Fabio Cannavaro——</h3>
            <p><strong>小组形势：</strong>首战1-3负哥伦比亚，净胜球-2，小组垫底。本场对世界#5葡萄牙是巨大考验。现实目标：争取平局(1分)，保留微弱出线希望。</p>
            <p><strong>本场战略：少输当赢。</strong>理由：葡萄牙纸面实力远超我方。必须用极致防守+快速反击，避免大比分失利以保护净胜球——净胜球可能是最终排名决定因素。</p>
            <p><strong>出线路径：</strong>现实目标是拼1平1胜(4分)挤进前4。最坏场景：此役再败则2战0分出局。</p>
            <p><strong>针对性策略：</strong>对葡萄牙用4-5-1超级大巴+长传找Shomurodov突击Rúben Dias身后；对刚果(金)属可拼比赛，全力搏3分。</p>
            <p><strong>B计划：</strong>先丢球后→放弃防守全力进攻争取进1球挽回尊严；如早早0-2落后→保护关键球员避免黄牌/伤退影响末轮。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 同组其他球队教练视角（简化）——</h3>
            <p><strong>🇨🇴 哥伦比亚 (Lorenzo)：</strong>首轮3-1胜，3分开局良好。本场对刚果(金)取胜可基本锁定晋级。两场胜则积6分无忧。对葡萄牙(第3轮)是提前锁定小组头名的关键战役。需防路易斯·迪亚斯被对方限制时的替代方案。</p>
            <p><strong>🇨🇩 刚果(金) (Desabre)：</strong>首轮1-1逼平葡萄牙，士气爆棚。第2轮对哥伦比亚(#13)可接受平局(积2分)。第3轮对乌兹别克斯坦是关键——必须赢的比赛。防守体系已被证明有效(Vs葡萄牙仅失1球)。</p>
        </div>
        <p class="note">⚖️ 教练博弈全景：H组8位教练中，Martínez(A级)和Dalić(A级)经验最丰富；Cannavaro(C级)执教经验最缺乏。教练能力差距在本场尤为显著。</p>
    </div>

    <div class="section">
        <h2>概率预测</h2>
        <table class="prob">
            <tr><th>葡萄牙胜</th><th>平局</th><th>乌兹别克斯坦胜</th></tr>
            <tr><td class="win">72%</td><td>18%</td><td>10%</td></tr>
        </table>
        <p><strong>置信度梯级：高</strong>（差值54%）</p>
        <p><strong>信号强度标注：</strong></p>
        <ul>
            <li>FIFA排名差 45位 → <span class="signal-strong">强信号 → 葡萄牙</span></li>
            <li>教练等级差 A级 vs C级 → <span class="signal-strong">强信号 → 葡萄牙</span></li>
            <li>世界杯经验差 9届 vs 首次 → <span class="signal-strong">强信号 → 葡萄牙</span></li>
            <li>乌兹别克对前20球队全败 → <span class="signal-strong">强信号 → 葡萄牙</span></li>
            <li>5大联赛球员数 15+ vs 1-2人 → <span class="signal-mid">中等信号 → 葡萄牙</span></li>
            <li>门将实力差(葡超首发 vs 乌兹联赛) → <span class="signal-mid">中等信号 → 葡萄牙</span></li>
        </ul>
    </div>

    <div class="section">
        <h2>比分预测</h2>
        <table class="score">
            <tr><th>类型</th><th>比分</th><th>概率</th></tr>
            <tr><td>最可能</td><td><strong>葡萄牙 3-0 乌兹别克斯坦</strong></td><td>~25%</td></tr>
            <tr><td>备选1</td><td>葡萄牙 2-0 乌兹别克斯坦</td><td>~20%</td></tr>
            <tr><td>备选2</td><td>葡萄牙 4-1 乌兹别克斯坦</td><td>~15%</td></tr>
        </table>
        <p><strong>预期xG区间：葡萄牙 2.5-3.2 / 乌兹别克斯坦 0.3-0.7 / 总xG 2.8-3.9</strong></p>
    </div>

    <div class="section conclusion">
        <h2>最终结论</h2>
        <p>葡萄牙首轮意外被刚果(金)逼平后已无退路，面对世界杯新军乌兹别克斯坦必须全取3分。双方实力差距巨大：FIFA排名差45位，全球员身价差10倍以上，教练经验差2级。乌兹别克斯坦首次世界杯面对前20球队已连续3场丢≥2球，防守端难以抵挡葡萄牙的边路过载和中路渗透。</p>
        <p><strong>关键假设：</strong>罗纳尔多首发且状态正常；乌兹别克斯坦不会采取极端防守(4-5-1大巴)；比赛在第60分钟前葡萄牙取得首球。</p>
        <p><strong>置信度：高。</strong>主要不确定性来自足球的偶然性和乌兹别克可能超水平发挥。</p>
        <p><strong>数据缺口：</strong>乌兹别克斯坦球员俱乐部近5场评分数据缺失（联赛数据源不可获取）；两队xG数据仅基于首轮单场样本，信度有限。</p>
    </div>
    """
}

# ============================================================
# MATCH 2: England vs Ghana
# ============================================================

MATCH2 = {
    "filename": "report-2026-06-22-england-ghana",
    "md_filename": "2026-06-22-england-ghana-prediction",
    "title": "英格兰 vs 加纳",
    "group": "H组 小组赛第2轮",
    "date": "2026-06-22",
    "time": "16:00 (当地时间20:00)",
    "venue": "吉列体育场，波士顿 · 中立场地",
    "odds": "英格兰胜 2/9 | 平局 6/1 | 加纳胜 14/1",
    "fifa_ranks": "英格兰 #4 vs 加纳 #73",
    "probability": "英格兰胜 68% / 平局 20% / 加纳胜 12%",
    "confidence": "高",
    "score_pred": "3-1",
    "score_prob": "约22%",
    "alt1": "2-0 (约20%)",
    "alt2": "2-1 (约18%)",
    "xG_range": "英格兰 xG 2.2-2.8 / 加纳 xG 0.6-1.0 / 总 xG 2.8-3.8",

    "body_html": r"""
    <div class="section">
        <h2>近期状态（对手强度校准后）</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格兰</h3>
                <p><strong>Tier 1-2:</strong> 4-2 克罗地亚(#11) / 1-1 乌拉圭(#16) / 0-1 日本(#18) / 3-0 哥斯达黎加(~#50) / 1-0 新西兰(#85)</p>
                <p>近5场: 3胜1平1负。首轮4-2大胜克罗地亚，凯恩2球、贝林厄姆1球、拉什福德1球，攻击线火力全开。图赫尔体系逐渐成熟。</p>
            </div>
            <div class="col">
                <h3>🇬🇭 加纳</h3>
                <p><strong>Tier 1-2:</strong> 1-0 巴拿马(#34) / 1-2 德国(#10) / 0-2 墨西哥(#14) / 1-5 奥地利(#24)</p>
                <p>近5场: 2胜2平1负。首轮1-0小胜巴拿马靠的是Yirenkyi的绝杀进球。但面对前25名球队(德国/墨西哥/奥地利)场均丢2.3球，防守面对强队漏洞明显。</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>球员覆盖</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格兰核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>关键数据</th></tr>
                    <tr><td>Harry Kane (C)</td><td>ST</td><td>32</td><td>Bayern</td><td>79球/已2球</td></tr>
                    <tr><td>Jude Bellingham</td><td>AM</td><td>22</td><td>Real Madrid</td><td>首轮1球</td></tr>
                    <tr><td>Marcus Rashford</td><td>LW</td><td>28</td><td>Barcelona</td><td>首轮1球</td></tr>
                    <tr><td>Bukayo Saka</td><td>RW</td><td>24</td><td>Arsenal</td><td>边路核心</td></tr>
                    <tr><td>Declan Rice</td><td>DM</td><td>27</td><td>Arsenal</td><td>中场屏障</td></tr>
                    <tr><td>Jordan Pickford</td><td>GK</td><td>32</td><td>Everton</td><td>首发门将</td></tr>
                    <tr><td>John Stones</td><td>CB</td><td>32</td><td>Man City</td><td>防线核心</td></tr>
                    <tr><td>Kobbie Mainoo</td><td>CM</td><td>21</td><td>Man United</td><td>中场新星</td></tr>
                    <tr><td>Reece James</td><td>RB</td><td>26</td><td>Chelsea</td><td>右路防守</td></tr>
                    <tr><td>Ollie Watkins</td><td>ST</td><td>30</td><td>Aston Villa</td><td>超级替补</td></tr>
                    <tr><td>Anthony Gordon</td><td>LW</td><td>25</td><td>Newcastle</td><td>速度爆点</td></tr>
                    <tr><td>Eberechi Eze</td><td>AM</td><td>27</td><td>Arsenal</td><td>创造力替补</td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇬🇭 加纳核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>关键数据</th></tr>
                    <tr><td>Jordan Ayew (C)</td><td>FW</td><td>34</td><td>Leicester</td><td>经验老将</td></tr>
                    <tr><td>Thomas Partey</td><td>DM</td><td>32</td><td>Arsenal</td><td>57出场15球</td></tr>
                    <tr><td>Antoine Semenyo</td><td>RW</td><td>26</td><td>Man City</td><td>边路速度</td></tr>
                    <tr><td>Iñaki Williams</td><td>ST</td><td>32</td><td>Athletic Bilbao</td><td>身体对抗</td></tr>
                    <tr><td>Caleb Yirenkyi</td><td>CM</td><td>20</td><td>Nordsjælland</td><td>首轮进球</td></tr>
                    <tr><td>Lawrence Ati-Zigi</td><td>GK</td><td>29</td><td>--</td><td>首发门将</td></tr>
                    <tr><td>Kamaldeen Sulemana</td><td>LW</td><td>24</td><td>Atalanta</td><td>边路突击</td></tr>
                    <tr><td>Alidu Seidu</td><td>RB</td><td>26</td><td>Rennes</td><td>右路防守</td></tr>
                    <tr><td>Jerome Opoku</td><td>CB</td><td>27</td><td>Başakşehir</td><td>中卫搭档</td></tr>
                    <tr><td>Ernest Nuamah</td><td>FW</td><td>22</td><td>Lyon</td><td>年轻射手</td></tr>
                    <tr><td>Fatawu Issahaku</td><td>RW</td><td>22</td><td>Leicester</td><td>边路替补</td></tr>
                    <tr><td>Elisha Owusu</td><td>CM</td><td>28</td><td>Auxerre</td><td>中场覆盖</td></tr>
                </table>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>主教练综合能力评估</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🏴󠁧󠁢󠁥󠁮󠁧󠁿 Thomas Tuchel</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>德国</td></tr>
                    <tr><td>执教时长</td><td>2025年至今</td></tr>
                    <tr><td>战术哲学</td><td>高位压迫+快速纵深传递 (4-3-3)</td></tr>
                    <tr><td>世界杯成绩</td><td>首次执教国家队</td></tr>
                    <tr><td>俱乐部大赛</td><td>欧冠冠军(切尔西2021)</td></tr>
                    <tr><td>Tier 1胜率</td><td>样本不足</td></tr>
                    <tr><td>战术灵活性</td><td>8/10</td></tr>
                    <tr><td>大赛压力应对</td><td>9/10</td></tr>
                    <tr><td>综合等级</td><td><strong>S级 (8.8/10)</strong></td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇬🇭 Carlos Queiroz</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>葡萄牙</td></tr>
                    <tr><td>执教时长</td><td>2024年至今</td></tr>
                    <tr><td>战术哲学</td><td>务实防守+定位球 (4-5-1)</td></tr>
                    <tr><td>世界杯成绩</td><td>执教过4届世界杯(伊朗×2, 葡萄牙, 南非)</td></tr>
                    <tr><td>Tier 1胜率</td><td>~20%</td></tr>
                    <tr><td>战术灵活性</td><td>6/10</td></tr>
                    <tr><td>大赛压力应对</td><td>7/10</td></tr>
                    <tr><td>综合等级</td><td><strong>B级 (6.5/10)</strong></td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 教练博弈：Tuchel(S级) vs Queiroz(B级)。图赫尔欧冠冠军经验+战术灵活性8分远胜奎罗斯，但奎罗斯的4届世界杯经验不可轻视。概率偏向英格兰~3%。</p>
    </div>

    <div class="section">
        <h2>教练视角：出线形势</h2>
        <div class="coach-view">
            <h3>🔄 我是英格兰主教练Thomas Tuchel——</h3>
            <p><strong>小组形势：</strong>首轮4-2胜克罗地亚，3分暂列第1。本场对加纳(3分，#73)是确立小组头名的关键一战。击败加纳积6分几乎锁定晋级。</p>
            <p><strong>本场战略：必须赢。</strong>理由：3分+净胜球优势+建立心理制高点。击败加纳后末轮对巴拿马(0分)可大幅轮换保留实力。</p>
            <p><strong>出线路径：</strong>最优9分全胜出线→本场+末轮胜巴拿马。现实路径6分(本场胜+末轮平/负)足以晋级前4。最坏场景：本场爆冷输球仅3分，末轮必须赢巴拿马。</p>
            <p><strong>针对性策略：</strong>对加纳用高位防线+中场碾压(贝林厄姆+赖斯+梅努三角)，快速破解奎罗斯的4-5-1防线。凯恩回撤吸引中卫→拉什福德+萨卡双翼插身后。</p>
            <p><strong>B计划：</strong>如果30分钟无法破门→沃特金斯换下梅努上双前锋，增加禁区压力；凯恩被限制→贝林厄姆前插射门责任加重。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 我是加纳主教练Carlos Queiroz——</h3>
            <p><strong>小组形势：</strong>首轮1-0胜巴拿马，3分暂列第3。本场对英格兰是世界#4的严峻考验。现实目标：拼1分。</p>
            <p><strong>本场战略：保平争胜。</strong>理由：如果能从英格兰身上拿1分，积4分几乎锁定晋级。此前对前25名球队场均丢2.3球是我的首要隐忧。</p>
            <p><strong>针对性策略：</strong>对英格兰用极致防守+快反：帕尔特伊单盯贝林厄姆、双后腰保护防线、边路回收阻止萨卡/拉什福德1v1空间。对巴拿马(0分)末轮是全取3分的重点。</p>
            <p><strong>B计划：</strong>先丢1球→保持阵型不变不冒进，避免大比分崩盘(净胜球关键)；70分钟后如还落后1球→上Fatawu+Nuamah双翼搏命。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 同组其他球队教练视角（简化）——</h3>
            <p><strong>🇭🇷 克罗地亚 (Dalić)：</strong>首轮2-4负英格兰，0分垫底。本场对巴拿马(0分)是必须赢的生死战。莫德里奇40岁仍是核心但体能是问题。对英格兰若再败就出局。</p>
            <p><strong>🇵🇦 巴拿马 (Christiansen)：</strong>首轮0-1被加纳绝杀，0分第6。本场对克罗地亚(0分)同为生死战。防守组织尚可(Ghana仅进1球)但进攻乏力。</p>
        </div>
        <p class="note">⚖️ 教练博弈全景：H组教练等级 Tuchel(S)>Dalić(A)>Martínez(A)>Queiroz(B)>其他。Tuchel的战术灵活性最高，Dalić世界杯经验最丰富(2018亚军+2022季军)。</p>
    </div>

    <div class="section">
        <h2>犯规率/纪律指数</h2>
        <p>加纳近10场比赛场均犯规约13次(中等)，但面对强队有上升趋势。帕尔特伊(Arsenal)习惯在中场用身体对抗断节奏——这可能是破坏英格兰流畅配合的手段。英国近10场场均犯规约9次(偏少)，纪律良好。</p>
    </div>

    <div class="section">
        <h2>概率预测</h2>
        <table class="prob">
            <tr><th>英格兰胜</th><th>平局</th><th>加纳胜</th></tr>
            <tr><td class="win">68%</td><td>20%</td><td>12%</td></tr>
        </table>
        <p><strong>置信度梯级：高</strong>（差值56%）</p>
        <p><strong>信号强度标注：</strong></p>
        <ul>
            <li>FIFA排名差 69位 → <span class="signal-strong">强信号 → 英格兰</span></li>
            <li>加纳对前25名场均失2.3球 → <span class="signal-strong">强信号 → 英格兰进球多</span></li>
            <li>首轮英格兰攻击力展示(4球) → <span class="signal-strong">强信号 → 英格兰</span></li>
            <li>教练等级差 S vs B → <span class="signal-mid">中等信号 → 英格兰</span></li>
            <li>加纳防守体系被验证(Vs巴拿马仅失0球) → <span class="signal-weak">弱信号 → 可能低比分</span></li>
            <li>过往友谊赛1-1(2011) → <span class="signal-weak">弱信号(时效性低)</span></li>
        </ul>
    </div>

    <div class="section">
        <h2>比分预测</h2>
        <table class="score">
            <tr><th>类型</th><th>比分</th><th>概率</th></tr>
            <tr><td>最可能</td><td><strong>英格兰 3-1 加纳</strong></td><td>~22%</td></tr>
            <tr><td>备选1</td><td>英格兰 2-0 加纳</td><td>~20%</td></tr>
            <tr><td>备选2</td><td>英格兰 2-1 加纳</td><td>~18%</td></tr>
        </table>
        <p><strong>预期xG区间：英格兰 2.2-2.8 / 加纳 0.6-1.0 / 总xG 2.8-3.8</strong></p>
    </div>

    <div class="section conclusion">
        <h2>最终结论</h2>
        <p>英格兰首轮4-2屠杀克罗地亚展示了图赫尔体系下极高的攻击效率——凯恩(2球)、贝林厄姆(1球)、拉什福德(1球)多点开花。加纳首轮1-0巴拿马靠的是防守韧性+运气绝杀，但面对德国、墨西哥、奥地利(场均丢2.3球)时防线反复暴露。关键对位是赖斯 vs 帕尔特伊——如果赖斯能控制中场，贝林厄姆和凯恩将获得大量空间。</p>
        <p>英格兰大概率取胜，但加纳的防守组织可能让比赛在第60分钟前保持紧张。预计最终英格兰凭阵容深度和个体质量拉开差距。</p>
        <p><strong>关键假设：</strong>凯恩和贝林厄姆首轮状态延续；加纳不会采取极端大巴(4-5-1已是最防守阵型)；英格兰后防不会因轻敌出现重大失误。</p>
        <p><strong>置信度：高。</strong></p>
        <p><strong>数据缺口：</strong>加纳球员俱乐部近5场数据缺失；双方xG数据仅基于首轮单样本；加纳"1-5奥地利"友谊赛的对手强度校准需更多细节。</p>
    </div>
    """
}

# ============================================================
# MATCH 3: Panama vs Croatia
# ============================================================

MATCH3 = {
    "filename": "report-2026-06-22-panama-croatia",
    "md_filename": "2026-06-22-panama-croatia-prediction",
    "title": "巴拿马 vs 克罗地亚",
    "group": "H组 小组赛第2轮",
    "date": "2026-06-22",
    "time": "19:00 (当地时间00:00)",
    "venue": "BMO球场，多伦多 · 中立场地",
    "odds": "巴拿马胜 6.50 | 平局 4.10 | 克罗地亚胜 1.50",
    "fifa_ranks": "巴拿马 #34 vs 克罗地亚 #11",
    "probability": "巴拿马胜 18% / 平局 25% / 克罗地亚胜 57%",
    "confidence": "中",
    "score_pred": "1-2",
    "score_prob": "约18%",
    "alt1": "0-2 (约17%)",
    "alt2": "1-1 (约15%)",
    "xG_range": "巴拿马 xG 0.5-0.9 / 克罗地亚 xG 1.5-2.1 / 总 xG 2.0-3.0",

    "body_html": r"""
    <div class="section">
        <h2>近期状态（对手强度校准后）</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇦 巴拿马</h3>
                <p><strong>Tier 1-2:</strong> 0-1 加纳(#73) / 数据不足</p>
                <p>近5场: 2胜1平2负，进1.8球失2.2球。首轮被加纳0-1绝杀，结果残酷但防守组织尚可(仅失1球)。世界杯8场0零封记录延续中——防守韧性问题长期存在。Carrasquilla伤愈不确定是否首发。</p>
            </div>
            <div class="col">
                <h3>🇭🇷 克罗地亚</h3>
                <p><strong>Tier 1-2:</strong> 2-4 英格兰(#4) / 2-1 哥伦比亚(#13) / 1-3 法国(#3)</p>
                <p>近5场: 2胜3负，进1.4球失2.2球。首轮2-4不敌英格兰暴露防线问题——面对快速转换时中卫速度不足。但攻击端表现可圈可点(Baturina和Musa各1球)。Dalić必须在这一场反弹。</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>球员覆盖</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇦 巴拿马核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th></tr>
                    <tr><td>Luis Mejía</td><td>GK</td><td>35</td><td>Nacional</td></tr>
                    <tr><td>Edgar Yoel Barcenas (C)</td><td>MF</td><td>32</td><td>Mazatlán</td></tr>
                    <tr><td>Andrés Andrade</td><td>DF</td><td>27</td><td>LASK</td></tr>
                    <tr><td>José Córdoba</td><td>CB</td><td>25</td><td>Norwich</td></tr>
                    <tr><td>Adalberto Carrasquilla</td><td>MF</td><td>27</td><td>UNAM</td></tr>
                    <tr><td>Aníbal Godoy</td><td>DM</td><td>36</td><td>San Diego FC</td></tr>
                    <tr><td>César Blackman</td><td>RB</td><td>28</td><td>Slovan Bratislava</td></tr>
                    <tr><td>Ismael Díaz</td><td>MF</td><td>29</td><td>León</td></tr>
                    <tr><td>Tomás Rodríguez</td><td>ST</td><td>27</td><td>Saprissa</td></tr>
                    <tr><td>José Fajardo</td><td>FW</td><td>32</td><td>Univ Católica</td></tr>
                    <tr><td>Alberto Quintero</td><td>MF</td><td>38</td><td>Plaza Amador</td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇭🇷 克罗地亚核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th></tr>
                    <tr><td>Luka Modrić</td><td>CM</td><td>40</td><td>Milan</td></tr>
                    <tr><td>Dominik Livaković</td><td>GK</td><td>31</td><td>Dinamo Zagreb</td></tr>
                    <tr><td>Joško Gvardiol</td><td>CB</td><td>24</td><td>Man City</td></tr>
                    <tr><td>Mateo Kovačić</td><td>CM</td><td>32</td><td>Man City</td></tr>
                    <tr><td>Andrej Kramarić</td><td>FW</td><td>35</td><td>Hoffenheim</td></tr>
                    <tr><td>Ivan Perišić</td><td>LW</td><td>37</td><td>PSV</td></tr>
                    <tr><td>Martin Baturina</td><td>CM</td><td>23</td><td>Como</td></tr>
                    <tr><td>Petar Musa</td><td>ST</td><td>28</td><td>FC Dallas</td></tr>
                    <tr><td>Josip Stanišić</td><td>RB</td><td>26</td><td>Bayern</td></tr>
                    <tr><td>Mario Pašalić</td><td>CM</td><td>31</td><td>Atalanta</td></tr>
                    <tr><td>Ante Budimir</td><td>ST</td><td>34</td><td>Osasuna</td></tr>
                    <tr><td>Nikola Vlašić</td><td>AM</td><td>28</td><td>Torino</td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 克罗地亚关键年龄问题：莫德里奇(40)、佩里希奇(37)、克拉马里奇(35)、布迪米尔(34)——老将体能是本届比赛持续性隐患。</p>
    </div>

    <div class="section">
        <h2>主教练综合能力评估</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇵🇦 Thomas Christiansen</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>丹麦/西班牙</td></tr>
                    <tr><td>执教时长</td><td>2020年至今</td></tr>
                    <tr><td>战术哲学</td><td>防守组织+反击 (4-4-2/4-2-3-1)</td></tr>
                    <tr><td>世界杯成绩</td><td>2018执教巴拿马(小组淘汰)</td></tr>
                    <tr><td>综合等级</td><td><strong>B级 (5.5/10)</strong></td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇭🇷 Zlatko Dalić</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>克罗地亚</td></tr>
                    <tr><td>执教时长</td><td>2017年至今</td></tr>
                    <tr><td>战术哲学</td><td>中场控制+高位防线 (4-3-3/4-2-3-1)</td></tr>
                    <tr><td>世界杯成绩</td><td>2018亚军/2022季军</td></tr>
                    <tr><td>战术灵活性</td><td>7/10</td></tr>
                    <tr><td>大赛压力应对</td><td>9/10</td></tr>
                    <tr><td>综合等级</td><td><strong>A级 (8.0/10)</strong></td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 教练博弈：Dalić(A级) vs Christiansen(B级)。Dalić连续两届世界杯进四强的大赛履历对此役有绝对心理优势。差距≥1.5级，概率偏向克罗地亚~3%。</p>
    </div>

    <div class="section">
        <h2>教练视角</h2>
        <div class="coach-view">
            <h3>🔄 我是巴拿马主教练Christiansen——</h3>
            <p><strong>小组形势：</strong>首轮0-1负加纳，0分第6。此役对克罗地亚(0分)是生死战——输球基本出局。必须至少拿1分保持希望。</p>
            <p><strong>本场战略：保平争胜。</strong>理由：克罗地亚防线有速度短板(被英格兰打入4球)，我们的反击可以利用。但如果先丢球，翻盘难度极大。</p>
            <p><strong>针对性策略：</strong>用紧凑4-4-2双线压缩克罗地亚中场空间，限制莫德里奇拿球。反击找Córdoba的直传→Fajardo的速度突破Gvardiol身后。</p>
            <p><strong>B计划：</strong>先丢球→变阵4-2-4搏命，全力利用高空球(巴拿马对抗优势)；如70分钟后0-0→维持防守阵型求1分。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 我是克罗地亚主教练Zlatko Dalić——</h3>
            <p><strong>小组形势：</strong>首轮2-4负英格兰，净胜球-2恐成出线障碍。此役对巴拿马(0分)必须赢且最好多进球补充净胜球。如果输球就基本出局。</p>
            <p><strong>本场战略：必须赢，追求净胜球。</strong>理由：末轮对加纳(3分)是硬仗，本场是唯一"应该稳拿"的3分。必须拿下并确保净胜球不低于-1。</p>
            <p><strong>针对性策略：</strong>用莫德里奇+科瓦契奇中场双核控制节奏，巴图里纳作为前插点。边路佩里希奇传中→穆萨头球轰炸(巴拿马防空一般)。</p>
            <p><strong>B计划：</strong>如果半场0-0或落后→60分钟换上布迪米尔+弗拉希奇增加进攻点位；莫德里奇体力不足时→苏契奇替换保持跑动。</p>
        </div>
    </div>

    <div class="section">
        <h2>概率预测</h2>
        <table class="prob">
            <tr><th>巴拿马胜</th><th>平局</th><th>克罗地亚胜</th></tr>
            <tr><td>18%</td><td>25%</td><td class="win">57%</td></tr>
        </table>
        <p><strong>置信度梯级：中</strong>（差值32%）</p>
        <p><strong>信号强度标注：</strong></p>
        <ul>
            <li>世界杯历史(亚军+季军 vs 小组淘汰) → <span class="signal-strong">强信号 → 克罗地亚</span></li>
            <li>FIFA排名差 23位 → <span class="signal-mid">中等信号 → 克罗地亚</span></li>
            <li>克罗地亚首轮防守漏洞(4球失) → <span class="signal-mid">中等信号 → 可能进球多</span></li>
            <li>巴拿马世界杯8场0零封 → <span class="signal-mid">中等信号 → 克罗地亚至少1球</span></li>
            <li>Carrasquilla伤愈不确定 → <span class="signal-weak">弱信号 → 巴拿马</span></li>
        </ul>
    </div>

    <div class="section">
        <h2>比分预测</h2>
        <table class="score">
            <tr><th>类型</th><th>比分</th><th>概率</th></tr>
            <tr><td>最可能</td><td><strong>巴拿马 1-2 克罗地亚</strong></td><td>~18%</td></tr>
            <tr><td>备选1</td><td>巴拿马 0-2 克罗地亚</td><td>~17%</td></tr>
            <tr><td>备选2</td><td>巴拿马 1-1 克罗地亚</td><td>~15%</td></tr>
        </table>
        <p><strong>预期xG区间：巴拿马 0.5-0.9 / 克罗地亚 1.5-2.1 / 总xG 2.0-3.0</strong></p>
    </div>

    <div class="section conclusion">
        <h2>最终结论</h2>
        <p>这是H组的"生死战"——输家几乎出局。克罗地亚尽管首轮2-4告负，但面对的是世界#4英格兰且攻击端展现素质(Baturina/Musa各1球)。巴拿马防守组织尚可但缺乏进球能力(世界杯8场0零封+首轮无进球)。Dalić的淘汰赛经验(A级)在此类生死战中尤为珍贵——2018和2022两届进四强证明他有能力在最困难时刻调整球队。</p>
        <p>预计克罗地亚控制比赛节奏，莫德里奇组织进攻，巴拿马在下半场体能下降时被破门。巴拿马可能通过定位球或反击偷1球。</p>
        <p><strong>关键假设：</strong>克罗地亚老将(莫德里奇40/佩里希奇37)体能可支撑70分钟高强度；巴拿马Carrasquilla即使首发也非100%状态；Livaković恢复首轮神勇(7次扑救)。</p>
        <p><strong>置信度：中。</strong>不确定性来自双方首轮均失利后的心理压力和克罗地亚老将体能问题。</p>
        <p><strong>数据缺口：</strong>克罗地亚球员俱乐部近期状态数据缺乏；巴拿马对阵强队样本极少(仅加纳#73)；双方xG数据仅基于单场世界杯样本。</p>
    </div>
    """
}

# ============================================================
# MATCH 4: Colombia vs Congo DR
# ============================================================

MATCH4 = {
    "filename": "report-2026-06-22-colombia-congo-dr",
    "md_filename": "2026-06-22-colombia-congo-dr-prediction",
    "title": "哥伦比亚 vs 刚果(金)",
    "group": "H组 小组赛第2轮",
    "date": "2026-06-22",
    "time": "20:00 (当地时间)",
    "venue": "阿克伦体育场，瓜达拉哈拉 · 中立场地",
    "odds": "哥伦比亚胜 8/15 | 平局 10/3 | 刚果(金)胜 13/2",
    "fifa_ranks": "哥伦比亚 #13 vs 刚果(金) #46",
    "probability": "哥伦比亚胜 55% / 平局 27% / 刚果(金)胜 18%",
    "confidence": "中",
    "score_pred": "2-0",
    "score_prob": "约18%",
    "alt1": "1-0 (约17%)",
    "alt2": "1-1 (约16%)",
    "xG_range": "哥伦比亚 xG 1.3-1.8 / 刚果(金) xG 0.4-0.8 / 总 xG 1.7-2.6",

    "body_html": r"""
    <div class="section">
        <h2>近期状态（对手强度校准后）</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇨🇴 哥伦比亚</h3>
                <p><strong>Tier 1-2:</strong> 3-1 乌兹别克斯坦(#50) / 1-3 法国(#3) / 1-2 克罗地亚(#11) / 2-0 约旦(#63) / 3-1 哥斯达黎加(~#50)</p>
                <p>近5场: 3胜2负，首轮3-1轻取乌兹别克。路易斯·迪亚斯(Diaz)状态火热——首轮1球+整体突破威胁。面对法国/克罗地亚虽输但均仅负1球，对抗顶级球队展现出竞争力。</p>
            </div>
            <div class="col">
                <h3>🇨🇩 刚果(金)</h3>
                <p><strong>Tier 1-2:</strong> 1-1 葡萄牙(#5) / 1-2 智利(~#35) / 0-0 丹麦(#12)</p>
                <p>近5场: 2胜2平1负。首轮逼平葡萄牙是最大亮点——防守体系有效(仅失1球)。预选赛9场仅失5球——后防是球队最可靠资产。但攻击端近5场仅进3球，输出有限。</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>球员覆盖</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇨🇴 哥伦比亚核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>关键数据</th></tr>
                    <tr><td>Luis Díaz</td><td>LW</td><td>29</td><td>Bayern</td><td>首轮1球</td></tr>
                    <tr><td>James Rodríguez (C)</td><td>AM</td><td>34</td><td>Minnesota Utd</td><td>创造力核心</td></tr>
                    <tr><td>David Ospina</td><td>GK</td><td>37</td><td>Atlético Nacional</td><td>130出场</td></tr>
                    <tr><td>Daniel Muñoz</td><td>RB</td><td>30</td><td>Crystal Palace</td><td>首轮1球</td></tr>
                    <tr><td>Jefferson Lerma</td><td>DM</td><td>31</td><td>Crystal Palace</td><td>中场屏障</td></tr>
                    <tr><td>Davinson Sánchez</td><td>CB</td><td>30</td><td>Galatasaray</td><td>防守核心</td></tr>
                    <tr><td>Jhon Córdoba</td><td>ST</td><td>33</td><td>Krasnodar</td><td>中锋支点</td></tr>
                    <tr><td>Richard Ríos</td><td>CM</td><td>26</td><td>Benfica</td><td>中场B2B</td></tr>
                    <tr><td>Jhon Arias</td><td>RW</td><td>28</td><td>Palmeiras</td><td>右路进攻</td></tr>
                    <tr><td>Jaminton Campaz</td><td>FW</td><td>26</td><td>Rosario Central</td><td>首轮1球</td></tr>
                    <tr><td>Johan Mojica</td><td>LB</td><td>33</td><td>Mallorca</td><td>左路防守</td></tr>
                    <tr><td>Luis Suárez</td><td>FW</td><td>28</td><td>Sporting CP</td><td>锋线轮换</td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇨🇩 刚果(金)核心阵容</h3>
                <table class="players">
                    <tr><th>球员</th><th>位置</th><th>年龄</th><th>俱乐部</th><th>关键数据</th></tr>
                    <tr><td>Chancel Mbemba (C)</td><td>CB</td><td>31</td><td>Lille</td><td>109出场</td></tr>
                    <tr><td>Aaron Wan-Bissaka</td><td>RB</td><td>28</td><td>West Ham</td><td>1v1防守专家</td></tr>
                    <tr><td>Yoane Wissa</td><td>FW</td><td>29</td><td>Newcastle</td><td>首轮进球</td></tr>
                    <tr><td>Cédric Bakambu</td><td>ST</td><td>35</td><td>Real Betis</td><td>经验中锋</td></tr>
                    <tr><td>Lionel Mpasi</td><td>GK</td><td>31</td><td>Le Havre</td><td>首发门将</td></tr>
                    <tr><td>Arthur Masuaku</td><td>LB</td><td>32</td><td>Lens</td><td>左路防守</td></tr>
                    <tr><td>Théo Bongonda</td><td>RW</td><td>30</td><td>Spartak Moscow</td><td>边路威胁</td></tr>
                    <tr><td>Samuel Moutoussamy</td><td>CM</td><td>29</td><td>Atromitos</td><td>中场控制</td></tr>
                    <tr><td>Charles Pickel</td><td>CM</td><td>29</td><td>Espanyol</td><td>中场覆盖</td></tr>
                    <tr><td>Meschack Elia</td><td>LW</td><td>28</td><td>Alanyaspor</td><td>边路速度</td></tr>
                    <tr><td>Ngal'ayel Mukau</td><td>DM</td><td>21</td><td>Lille</td><td>年轻拦截者</td></tr>
                    <tr><td>Gaël Kakuta</td><td>AM</td><td>35</td><td>AEL</td><td>经验老将</td></tr>
                </table>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>主教练综合能力评估</h2>
        <div class="dual-col">
            <div class="col">
                <h3>🇨🇴 Néstor Lorenzo</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>阿根廷</td></tr>
                    <tr><td>执教时长</td><td>2022年至今</td></tr>
                    <tr><td>战术哲学</td><td>平衡攻守+边路驱动 (4-2-3-1)</td></tr>
                    <tr><td>世界杯成绩</td><td>首次执教世界杯</td></tr>
                    <tr><td>综合等级</td><td><strong>B级 (6.2/10)</strong></td></tr>
                </table>
            </div>
            <div class="col">
                <h3>🇨🇩 Sébastien Desabre</h3>
                <table class="coach">
                    <tr><td>国籍</td><td>法国</td></tr>
                    <tr><td>执教时长</td><td>2022年至今</td></tr>
                    <tr><td>战术哲学</td><td>防守组织+高效反击 (4-3-3)</td></tr>
                    <tr><td>世界杯成绩</td><td>首次执教世界杯(率队时隔50年晋级)</td></tr>
                    <tr><td>防守记录</td><td>9场预选赛仅失5球</td></tr>
                    <tr><td>综合等级</td><td><strong>B级 (5.8/10)</strong></td></tr>
                </table>
            </div>
        </div>
        <p class="note">⚠️ 教练博弈：两位首次执教世界杯的教练。Lorenzo的哥伦比亚进攻更丰富(迪亚斯+罗德里格斯+阿里亚斯)，Desabre的盾牌(预选赛9场仅失5球)已获检验(Vs葡萄牙)。战术风格：Lorenzo进攻型 vs Desabre防守反制型——后者对前者有天然克制属性。</p>
    </div>

    <div class="section">
        <h2>关键对位</h2>
        <table class="matchups">
            <tr><th>#</th><th>对位</th><th>分析</th></tr>
            <tr><td>1</td><td><strong>路易斯·迪亚斯 vs Aaron Wan-Bissaka</strong></td><td>这是本场最关键对位。迪亚斯(Bayern)1v1突破极强，首轮已有1球。Wan-Bissaka的1v1防守能力在英超顶级，但面对迪亚斯的速度+变向将经受严峻考验。此对位胜负直接决定哥伦比亚左路进攻效率。</td></tr>
            <tr><td>2</td><td><strong>詹姆斯·罗德里格斯 vs Charles Pickel</strong></td><td>J罗(34)虽然年龄增长但创造力未减，首轮多次送出威胁传球。Pickel需贴身限制J罗的拿球空间——如J罗自由发挥，哥伦比亚进攻将极具威胁。</td></tr>
            <tr><td>3</td><td><strong>Yoane Wissa vs Davinson Sánchez</strong></td><td>Wissa首轮攻破葡萄牙大门，速度+灵巧型前锋。Sánchez身材高大但转身速度一般——Wissa可能利用身后空间制造威胁。</td></tr>
        </table>
    </div>

    <div class="section">
        <h2>教练视角</h2>
        <div class="coach-view">
            <h3>🔄 我是哥伦比亚主教练Lorenzo——</h3>
            <p><strong>小组形势：</strong>首轮3-1胜乌兹别克，3分排第2。本场对刚果(金)取胜基本锁定晋级——积6分几乎无法被淘汰。但刚果(金)首轮逼平葡萄牙已证明自己不是软柿子。</p>
            <p><strong>本场战略：赢球即可，1-0也行。</strong>理由：刚果(金)防守严密(预选赛9场失5球)，不需要追求大比分。稳健拿下3分，为末轮对葡萄牙(#5)保留体能。</p>
            <p><strong>针对性策略：</strong>用迪亚斯+J罗的组合在左路制造过载，利用Wan-Bissaka可能参与进攻后的空当。同时Lerma+Ríos双后腰保护防线，防止刚果(金)快速反击(Wissa+Bakambu)。</p>
            <p><strong>B计划：</strong>如果70分钟仍0-0→上Campaz+Suárez增加进攻人数；迪亚斯被Wan-Bissaka限制→改打右路由Arias主攻。</p>
        </div>
        <div class="coach-view">
            <h3>🔄 我是刚果(金)主教练Desabre——</h3>
            <p><strong>小组形势：</strong>首轮1-1逼平葡萄牙，1分第5。再拿1分或3分都将大幅提升出线机会。防守体系已通过葡萄牙检验——继续坚持我们的比赛计划。</p>
            <p><strong>本场战略：保平争胜。</strong>理由：平局(积2分)加上末轮对乌兹别克斯坦(0分)有望拿3分=5分晋级。我们不需要冒险。</p>
            <p><strong>针对性策略：</strong>用Mbemba+Wan-Bissaka+Masuaku的防守三人组限制迪亚斯+J罗。反击找Wissa的速度走Sánchez身后。Bakambu作为支点接长传球。</p>
            <p><strong>B计划：</strong>先丢球→保持防守阵型不改(避免0-2崩盘)，65分钟后逐步增加进攻投入；如0-0到80分钟→坚决守平(1分宝贵)。</p>
        </div>
    </div>

    <div class="section">
        <h2>概率预测</h2>
        <table class="prob">
            <tr><th>哥伦比亚胜</th><th>平局</th><th>刚果(金)胜</th></tr>
            <tr><td class="win">55%</td><td>27%</td><td>18%</td></tr>
        </table>
        <p><strong>置信度梯级：中</strong>（差值28%）</p>
        <p><strong>信号强度标注：</strong></p>
        <ul>
            <li>FIFA排名差 33位 → <span class="signal-mid">中等信号 → 哥伦比亚</span></li>
            <li>刚果(金)逼平葡萄牙证明防守实力 → <span class="signal-strong">强信号 → 平局可能</span></li>
            <li>刚果(金)预选赛9场仅失5球 → <span class="signal-strong">强信号 → 低比分</span></li>
            <li>哥伦比亚攻击力(首轮3球) → <span class="signal-mid">中等信号 → 哥伦比亚</span></li>
            <li>防守反制风格克制进攻型 → <span class="signal-mid">中等信号 → 平局/刚果</span></li>
            <li>Luis Díaz状态火热 → <span class="signal-mid">中等信号 → 哥伦比亚</span></li>
        </ul>
    </div>

    <div class="section">
        <h2>比分预测</h2>
        <table class="score">
            <tr><th>类型</th><th>比分</th><th>概率</th></tr>
            <tr><td>最可能</td><td><strong>哥伦比亚 2-0 刚果(金)</strong></td><td>~18%</td></tr>
            <tr><td>备选1</td><td>哥伦比亚 1-0 刚果(金)</td><td>~17%</td></tr>
            <tr><td>备选2</td><td>哥伦比亚 1-1 刚果(金)</td><td>~16%</td></tr>
        </table>
        <p><strong>预期xG区间：哥伦比亚 1.3-1.8 / 刚果(金) 0.4-0.8 / 总xG 1.7-2.6</strong></p>
    </div>

    <div class="section conclusion">
        <h2>最终结论</h2>
        <p>这是H组一场攻防矛盾之战。哥伦比亚攻击力排名H组第2(首轮3球)，由路易斯·迪亚斯和J罗领衔。但刚果(金)的防守体系已在首轮逼平葡萄牙得到验证——9场预选赛仅失5球的数据说明Desabre的防守组织是球队最强武器。</p>
        <p>关键看点是迪亚斯 vs Wan-Bissaka的边路对决——如果Wan-Bissaka能限制迪亚斯，刚果(金)有极大可能逼平(甚至偷1球)。但哥伦比亚整体实力仍占优，预计通过某个定位球或J罗的精妙助攻打破僵局。</p>
        <p><strong>关键假设：</strong>Luis Díaz维持首轮状态；刚果(金)防守组织不被哥伦比亚早早进球打乱；比赛温度适中(瓜达拉哈拉6月较热可能影响体能)。</p>
        <p><strong>置信度：中。</strong>最大不确定性来自刚果(金)防守体系在背靠背面对强队时的持续性——连胜葡萄牙+哥伦比亚的防守任务量远超预选赛水平。</p>
        <p><strong>数据缺口：</strong>双方xG数据仅基于首轮单样本；刚果(金)俱乐部球员近5场评分缺失；哥伦比亚对非洲球队历史战绩缺失。</p>
    </div>
    """
}

# ============================================================
# HTML TEMPLATE
# ============================================================

CSS = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: #fff; color: #111; line-height: 1.6; }
    .container { max-width: 960px; margin: 0 auto; padding: 40px 24px; }
    header { border-bottom: 2px solid #0033A0; padding-bottom: 24px; margin-bottom: 32px; }
    h1 { font-size: 2rem; font-weight: 800; color: #0033A0; }
    .meta { color: #555; font-size: 0.9rem; margin-top: 8px; }
    .meta span { margin-right: 16px; }
    .section { margin-bottom: 32px; padding: 24px; border: 1px solid #000; border-radius: 4px; }
    .section h2 { font-size: 1.2rem; font-weight: 700; color: #0033A0; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #000; }
    .section h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
    .dual-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    @media (max-width: 640px) { .dual-col { grid-template-columns: 1fr; } }
    .col p { margin-bottom: 8px; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.85rem; }
    th, td { border: 1px solid #000; padding: 6px 10px; text-align: left; }
    th { background: #0033A0; color: #fff; font-weight: 600; }
    .standings tr:nth-child(even) td { background: #f0f4ff; }
    .prob td { text-align: center; font-size: 1.3rem; font-weight: 700; }
    .prob td.win { background: #0033A0; color: #fff; }
    .score td { text-align: center; }
    .matchups th { background: #000; }
    .coach-view { margin-bottom: 16px; padding: 16px; border-left: 3px solid #0033A0; background: #f4f7fd; }
    .coach-view h3 { color: #0033A0; }
    .note { font-size: 0.85rem; color: #c0392b; background: #fef5f5; padding: 10px 14px; border-left: 3px solid #c0392b; margin: 12px 0; }
    .signal-strong { color: #c0392b; font-weight: 700; }
    .signal-mid { color: #e67e22; font-weight: 600; }
    .signal-weak { color: #7f8c8d; }
    .conclusion { background: #f0f4ff; border-color: #0033A0; }
    .conclusion h2 { color: #0033A0; }
    footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #000; font-size: 0.8rem; color: #888; text-align: center; }
    .players td:first-child { font-weight: 600; }
    .coach td:first-child { font-weight: 600; width: 120px; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 2026世界杯预测 | H组</title>
<style>
{css}
</style>
</head>
<body>
<div class="container">
<header>
<h1>{title}</h1>
<p class="meta">
<span>📍 {venue}</span>
<span>🕐 {time}</span>
<span>📅 {date}</span>
</p>
<p class="meta">
<span>🏆 {group}</span>
<span>🏅 FIFA: {fifa_ranks}</span>
</p>
<p class="meta">
<span>💰 赔率: {odds}</span>
</p>
<p class="meta">数据更新时间：2026-06-22 12:00</p>
</header>

<div class="section">
<h2>H组积分形势（第1轮后）</h2>
{standings}
</div>

{body}

<footer>
<p>报告数据仅供参考，不构成投注建议</p>
</footer>
</div>
</body>
</html>"""


def to_markdown(match_data):
    """Convert match data to markdown for Obsidian"""
    d = match_data
    md = f"""# {d['title']} — 2026世界杯预测

## 比赛信息
- **比赛**: {d['title']}
- **时间**: {d['date']} {d['time']}
- **地点**: {d['venue']}
- **阶段**: {d['group']}
- **FIFA排名**: {d['fifa_ranks']}
- **赔率**: {d['odds']}
- **数据更新时间**: 2026-06-22 12:00

---

## H组积分形势（第1轮后）

| # | 球队 | 赛 | 胜 | 平 | 负 | 进球 | 失球 | 净胜 | 积分 |
|---|------|-----|-----|-----|-----|------|------|------|------|
| 1 | 英格兰 | 1 | 1 | 0 | 0 | 4 | 2 | +2 | **3** |
| 2 | 哥伦比亚 | 1 | 1 | 0 | 0 | 3 | 1 | +2 | **3** |
| 3 | 加纳 | 1 | 1 | 0 | 0 | 1 | 0 | +1 | **3** |
| 4 | 葡萄牙 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | **1** |
| 5 | 刚果(金) | 1 | 0 | 1 | 0 | 1 | 1 | 0 | **1** |
| 6 | 巴拿马 | 1 | 0 | 0 | 1 | 0 | 1 | -1 | **0** |
| 7 | 乌兹别克斯坦 | 1 | 0 | 0 | 1 | 1 | 3 | -2 | **0** |
| 8 | 克罗地亚 | 1 | 0 | 0 | 1 | 2 | 4 | -2 | **0** |

---

## 概率预测

| 主胜 | 平局 | 客胜 |
|------|------|------|
| **{d['probability']}** |

**置信度梯级**: {d['confidence']}

---

## 比分预测

| 类型 | 比分 | 概率 |
|------|------|------|
| 最可能 | **{d['score_pred']}** | {d['score_prob']} |
| 备选1 | {d['alt1']} | — |
| 备选2 | {d['alt2']} | — |

**预期xG区间**: {d['xG_range']}

---

*报告数据仅供参考，不构成投注建议*
"""
    return md


def generate():
    matches = [MATCH1, MATCH2, MATCH3, MATCH4]

    for m in matches:
        # HTML
        html_path = os.path.join(REPORTS_DIR, m["filename"] + ".html")
        html_content = HTML_TEMPLATE.format(
            title=m["title"],
            venue=m["venue"],
            time=m["time"],
            date=m["date"],
            group=m["group"],
            fifa_ranks=m["fifa_ranks"],
            odds=m["odds"],
            standings=GROUP_STANDINGS,
            body=m["body_html"],
            css=CSS,
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ HTML: {html_path}")

        # Markdown for Obsidian
        md_content = to_markdown(m)
        md_path = os.path.join(OBSIDIAN_DIR, m["md_filename"] + ".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ MD: {md_path}")

    print("\n🎉 All 4 reports generated!")


if __name__ == "__main__":
    generate()
