# 胖森杯S2 选手对局「狙击/撞车」调查报告

> 生成 2026-09-06(v4) · 数据：85 场已确认杯赛对局(8-29~9-5, UTC 11:00-16:00, steam 服务器)全部遥测 + 184 名重点账号 14 天比赛历史 + 6,376 场比赛详情
> 结论先行：**存在明显的、有组织迹象的"跟随杯赛日程撞车"现象**；但针对单一选手的精准狙击、以及行为层面的恶意证据（追击(双方法验证)、火箭筒、击杀后退游）基本不成立。可疑对局的回放链接与选手账号↔使用人对照见附录 B/C。

## 一、研究口径

- 杯赛对局全集 = 7 份日报中的 85 个 matchId（7 组选手搭档、14 个账号，另有官方填充位 1 组 2 账号出现 73 场，按工作人员排除）。
- 对局内其余 7,443 个账号为"同场者"，其中 429 个出现 ≥2 场（排除填充位）。
- 基线：meet_study 抽样的 443 名随机活跃玩家（同口径 14 天历史，均值 148 场），与 85 场杯赛的相遇均值仅 **0.02 场**（最多 2 场）。
- 暴露量检验：每名嫌疑人的期望撞入次数 = 0.00029（随机队列每场杯赛时段比赛的撞入率）× 该账号杯赛时段(UTC 11-16)内实际场次，泊松检验。

## 二、指标结论

### 1. 出现频率 —— 显著异常 ✅
- 随机基线下 85 场里出现 ≥2 次的期望人数 ≈ 74（泊松均匀假设），≥3 次期望 ≈ 0.01 人；实际 429 人 ≥2 次、**33 人 ≥3 次**。
- 按个人暴露量检验：**116 人 p<1e-5**，全体嫌疑人 p 值总和 = 0.0045（即随机下几乎不可能出现任何一个，实际几十个）。
- 最极端的 28 人：14 天内在杯赛时段只打了 ≤6 场普通对局，却有 ≥2 场是杯赛对局——**只在杯赛直播时段上线**。

#### 1.1 是否只狙击某一选手 —— 多数不是
- 16 人两次撞上同一组选手（二项 p≈0.02~0.05，个体证据弱）。
- 头部嫌疑人的撞入对象普遍横跨 3~6 组选手，更符合"跟随杯赛日程（时间+地图）"而非"跟定某个人"。
- 例外：Dragonproud_sky 与 66-666-6-66（两个不同账号）在不同对局中分别团灭了**同一组**选手（ooluckyooo&iiiiLuckyOooo 组）。

### 2. 落地跳点距离 —— 修复落点检测后基本持平，仅 3 个例外 ⚠️
(注：v1-v3 报告的落点数据存在检测 bug(载具移动被误判为空中、速度阈值单位错误)，本节及指标 3/9 均为修复后重算结果)

- 嫌疑人(n≥2)落点距选手双人组：中位 1664m、<200m 占 9.6%；普通同场者：中位 1616m、<200m 占 8.3%——**总体几乎持平**，v2 中"轻度偏近"的结论主要由 bug 造成，予以撤回。
- 但个别"落在选手跳点上"的出场依然醒目：XX-STAR-XX1(`a933c9cd`) 落点距选手 **28m**、i11bbi(`b78ee504`) **87m**、GB-zazhong(`c6542a66`) **148m**——三人均在该场击杀了选手(前两人团灭双人组)。

### 3. 追击/贴近行为 —— 三种模式判定：单模式弱信号，但存在值得复核的整队合围 ⚠️

**模式A 延迟接近**(选手驻留≥120s → 直播延迟120s后从>400m贴近至≤350m,排除驻留前已在路上)：嫌疑人 13/719=**1.81%** vs 对照 78/4687=**1.66%** —— 无区分度。

**模式B 贴身滞留**(存活≥180s 期间与选手距离<250m 的时间占比≥50%,期间未击杀选手,窗口截止到选手组第一人死亡,排除终局圈强制靠近)：嫌疑人 39/401=**9.7%** vs 对照 179/2733=**6.5%** —— 约 1.5 倍。

**模式C 长途奔袭**(落点距选手≥2km,1200s 内抵达<300m,路径直率≥0.55 且实际移动≥1.5km)：嫌疑人 37/871=**4.2%** vs 对照 211/6540=**3.2%** —— 约 1.3 倍,但**高度聚集**：37 例集中在 15 场,其中 6 场出现 3~5 名嫌疑人同场奔袭同一组选手：

| 对局 | 奔袭者 | 目标 | 起步距离 |
|---|---|---|---|
| `1c577902` | Elder_LaoOu-_, Elder_laohu_-, LuciferTUJI, QiuGe_MXKL, VoiD_X_AiM (5人) | dsdwfnygsaew&TOPM249-___- 组 | 2.4~4.7km |
| `217ad582` | XX-STAR-XX1, Relieved_Qinss, Relieved_Baooo, ShuiZuanDaKong, ghW6wtFhNS (5人) | 明柒柒&kk 组 | 2.6~3.6km |
| `46676089` | Fuck02468, May_Xuc_Than, ONGGIAXD, Shuxiansheng- (4人) | BAOBAONO1_&czczzsodjjd222 组 | 2.7~2.9km |
| `99b73b1a` | GTX3310, PINK_SOYES, MairooMaichiX, XxStunxX (4人) | dsdwfnygsaew&TOPM249-___- 组 | 3.1~3.2km |
| `c21cb548` | MCC-BanMeng, Mr-Rxsm, ZQuanH9 (3人) | 汐月(CandyBB--_)&xs(weirdo_im) 组 | 3.3~4.4km |
| `c892be8c` | FIND666, lajiaochaorou43, oison-biting- (3人) | HelloKittyOK666 (Shen) | 2.5km |

其中 `217ad582` 场 XX-STAR-XX1 奔袭抵达后于 1550s 击杀选手;`c21cb548` 场 MCC-BanMeng 抵达后于 1240s 击杀 CandyBB--_——**奔袭→击杀的完整链条**各有一次,建议优先录像复核这 6 场。

**关于 DogeEarth/YiShi_PT 的两场**(用户指认,复核属实但未达强门槛)：
- `c21cb548`：落地后 606s 存活窗口内 **37% 时间处于选手双人组 250m 内**,最终在距选手约 200m 处被击杀,全程 0 击杀 0 对选手伤害;同场 MCC-BanMeng 等 3 人奔袭抵达并击杀选手。
- `09f40150`：落点距选手 2614m,路径游走 4km+ 后多次接近选手至 250m 内(约占 18% 时间),全程未与选手接战。
- 其 7 场撞入中无一场击杀选手,行为画像为"反复在选手周边出没但不接战",与模式B/C 的随机基线差异不大,单独不足以定罪。

### 4. 多次击杀选手 —— 有，但多为当场团灭 ⚠️
- 156 次选手击杀来自 127 人；27 人杀 ≥2 名（基本是同一场内团灭双人组）。
- 跨对局杀选手者仅 1 人：**XX-STAR-XX1**（2 场 3 杀，其中一场 3.5 分钟内团灭 7Bebebe_&January_BiG 组）。GB-zazhong 单场杀 3 人次。

### 5. 偏好拾取火箭筒 —— 不成立 ❌
- 85 场共 308 个角色捡过 PanzerFaust（铁拳），无任何嫌疑人集中度；无 Mortar/其他筒械偏好。

### 6. 击杀/选手阵亡后短时间内退游 —— 不成立 ❌
- 0 例"击杀选手后 300s 内退出"；0 例"选手阵亡后 300s 内退出的存活者"（222 个提前退出者全部与选手阵亡无时序关联）。
- 仅有孤立个案：ntcag 在杯赛对局内 64s 退出；YICCCCCC 在两场不同杯赛对局中均于 ~65-70s 退出。

### 7. 频繁进游戏即退（撞车失败重试）—— 基本不成立 ❌
- 以 deathType=logout 口径：基线 2.1e-5/人次。36 个 n≥3 嫌疑人中 4 人有 logout 场次（Fish-super 3 场，但存活 691-818s，非秒退）。
- 嫌疑人全部正常对局（14 天 36~1137 场），**不依赖"排队-秒退"式撞车**，而是正常游戏时跟随日程上线。

### 8. 击杀选手后改名 —— 5 例改名，1 例高度可疑 ⚠️
| 杯赛期间用名 | 现用名 | 撞入次数 | p 值 |
|---|---|---|---|
| DogeEarth(4) → YiShi_PT(3) | YiShi_PT | 7 | ≈0 (p<1e-16) |
| CrissBZ → i11bbi | i11bbi | 2 | 5.4e-5 |
| Lux_Ghost → PinMing-G | PinMing-G | 2 | 1.7e-5 |
| WJ41Ny3 → IJ7Z | IJ7Z | 2 | 2.0e-5 |
| 308860 ↔ MrYan_-（反复改） | MrYan_- | 3 | 1.2e-4 |
| （填充位 CandyBB-_- → Il1IlllIIlll10oO 等，属工作人员） | | 73 | 排除 |

### 9. 排除指标：落点人群 + 早期交火 + 非选手跳点 ⚠️（用于洗白，非指控）

口径：若某嫌疑人在某场的出场满足——落点距选手双人组 ≥500m（跳点不是选手的跳点）、落点 300m 内有 ≥10 名其他敌人（全体落点人群分布的 p88，中位数仅 4 人）、且落地后 180s 内即与他人交火——则该场出场判定为"普通热门点刚枪"，从嫌疑中**排除**。

- 排除模式占比：嫌疑人 207/885 = **23.4%**，普通同场者 1397/7186 = **19.4%**——嫌疑人略高但接近，该指标只用于洗白、不构成新指控。
- 429 名多次撞入者中 **29 人全部出场均可由此解释**，从名单剔除。
- 12 场可疑对局的涉案出场中，被排除的有：ntcag、YICCCCCC(`c6542a66`,落点 6.4km 外且开局即退)、XX-STAR-XX1(`217ad582`,3.7km 外的出场;其 `a933c9cd` 28m 落点出场**不被排除**)、33322daohaosiDM(`8dc6f63c`)、Dragonproud_sky(`039ca015`,落点 2.0km,靠旋转接战击杀选手,出场解释为正常转点但击杀事实保留)。

### 10. 可疑对局前后的匹配行为 —— 3 例等待空档 + 2 例罕见退出 ⚠️

对 12 场可疑对局的 22 名涉案账号，在其可疑对局 ±6h 窗口内建对局时间线（间隔按玩家实际参与结束时刻计算），与随机对照（51,295 场窗口内对局）比较：

| 信号 | 嫌疑人案例 | 随机基线 |
|---|---|---|
| ★进杯赛局前长时间等待（间隔≥10min） | **Yazhe-KP 11min**（`804abae9` 前）、**66-666-6-66 15min**（`b1dfe084` 前）、**GB-zazhong 13min**（`c6542a66` 前） | 嫌疑人全部间隔中仅 6.4% ≥12min |
| ★窗口内中途退出(logout) | **ZKI-OKOLAJ** 1 场（246s，`e654ffe5` 当日） | logout<200s：**0/51,295** |
| ★窗口内自杀(<200s) | **ntcag** 1 场（135s，`c6542a66` 当日） | suicide<200s：37/51,295 = 0.07% |
| 落地 2-3 分钟即死 | 多人有（如 i11bbi 窗口内 23/52） | 本身常见（17.7%）；须对比账号自身基础率——i11bbi 整体 185/927=20%，属跳伞刚枪打法，**不构成信号** |

要点：
- 3 例"等待后进杯赛局"中，66-666-6-66 与 GB-zazhong 的窗口内其他间隔均正常，唯独进杯赛局前出现 13~15 分钟空档，与"等上一组选手死完再排队"的假设一致；但也可能是偶发，不足以单独定罪。
- 66-666-6-66 全天仅 6 场、0 次 early-death（整体 0/33），是"小心谨慎型"玩家——其 0m 落点+拳击+雷团灭组合与其整体打法反差大。
- 其余涉案账号在窗口内均维持正常连续对局（间隔中位 174s），无"打完就跑"或"反复排队秒退"。

## 三、重点账号清单

| 账号ID | 用名 | 撞入 | 关键行为(修复落点后) |
|---|---|---|---|
| account.a7fd529a382140079ed5fc8018f81474 | DogeEarth→YiShi_PT | 7 | 杯赛时段仅 36 场普通局；75% 跟随杯赛地图；中途改名；p<1e-16；c21cb548/09f40150 反复贴身选手 0 交战 |
| account.1d6ab648d3ce4ac5896cd757848de5fe | XX-STAR-XX1 | 2 | a933c9cd 落点 28m 团灭一组(211s/233s)；217ad582 奔袭 2.7km 后 1550s 击杀选手；跨场共 3 杀 |
| account.a89c7a68afda4b1697e36ce6c48f7e85 | lv_556 | 4 | 10 杀；8-29 连撞 3 场(与 7nnx 组队)；p=8e-8 |
| account.ff55e6ca9e414ddfa9ea522a9ec416ed | 7nnx | 3 | lv_556 队友，9 杀 |
| account.e0b89bdf75d44102a3333064a33b5e40 | GB-zazhong | 3 | c6542a66 落点 148m、全程 100% 时间在选手 250m 内，3 杀团灭一组；进杯赛局前 13min 空档 |
| account.a4a71ad6b561406d8733917bb63af2c7 | 66-666-6-66 | 2 | b1dfe084 奔袭 3.3km(+540s 抵达)后 766s 拳击+雷团灭 Cui71&04NB 组；进杯赛局前 15min 空档；全天 0 早死 |
| account.0debc61a3cb64563a294a29cd300fa61 | Yazhe-KP | 2 | 804abae9 击杀选手；进杯赛局前 11min 空档 |
| Cool_Shark / Cool_iKun_- / Cool_LiuxIN / Cool_M1porridge（4 人小队） | | 各3 | 同时出现 3 场；e654ffe5 两人同时击杀 Shen&SpaceMan 组双人 |
| 9cckaka / LookMyMM / Tomorrow-ii(→iii，改名) 小队 | | 各3 | 同队 3 场 |
| 其余 p<1e-5 名单（29 人已由排除指标洗白） | 见 `exposure_test.json` | | |

## 四、综合判断

1. **撞车不是随机的**：频率超出基线 3~30 个数量级（按个体检验），且存在"只在杯赛时段上线"、"跟随杯赛地图轮换"（DogeEarth 75%）、"固定小队整队反复出现"（至少 12 个 2~4 人团伙）等组织化特征。这更像**观众/黑子按直播日程蹲点撞车**，规模约 100~150 个账号。
2. **针对单一选手的定向狙击证据不足**：撞入对象普遍分散；仅"ooluckyooo&iiiiLuckyOooo 组"被 3 个不同账号分别团灭，值得关注但样本小。
3. **行为层证据：单模式弱、组合模式值得复核**。三种追击/贴近模式单独看均只有 1.3~1.5 倍的弱升高（模式A 无区分度），无火箭筒偏好、无击杀后退游、无秒退重试；落点人群排除指标下嫌疑人 23.4% vs 对照 19.4%，29 人可完全洗白。但**组合起来看有三条具体的"奔袭→击杀"链和整队合围**：(a) `217ad582`（明柒柒&kk 组）5 人从 2.6~3.6km 外奔袭合围，XX-STAR-XX1 抵达后击杀选手——他另在 `a933c9cd` 28m 落点团灭一组，是全场唯一跨场杀选手者；(b) `e654ffe5`（Shen&SpaceMan 组）SnD-1990/ZKI-OKOLAJ 奔袭合围+Cool_* 双人同时击杀+ZKI-OKOLAJ 当日一场 246s logout（基线 0/51,295）；(c) `c21cb548`（汐月&xs 组）3 人奔袭、MCC-BanMeng 抵达后击杀选手、DogeEarth 全程贴身 0 交战。另有 3 例进杯赛局前 11~15 分钟等待空档（Yazhe-KP、66-666-6-66、GB-zazhong）与 ntcag 杯赛当日自杀（基线 0.07%）。多数撞车者的对局内表现与普通玩家无异。
4. 建议核查方向（按优先级）：① `217ad582` 与 `a933c9cd`（XX-STAR-XX1 两次杀选手+5 人合围）；② `c21cb548`、`e654ffe5`（奔袭合围+击杀链）；③ `1c577902`、`99b73b1a`、`46676089`（整队 4~5 人奔袭同一组选手）；④ 3 例等待空档时段与直播内容比对；⑤ Dragonproud_sky 与 66-666-6-66 的组队历史关联。全部 12+2 场对局的嫌疑人视角回放链接见附录 B。

## 五、局限

- 基线率(0.00029)由 443 人随机队列估计，按小时条件化但未按地图/MMR 细分；同好玩家自然聚集可使尾部概率上浮，但不足以解释 116 人 p<1e-5。
- "同场"≠恶意：固定小队可能只是爱看比赛的重度粉丝；本报告的判定应结合录像证据。
- 嫌疑人历史窗口为 8-23~9-6（API 14 天保留期），早于 8-29 的杯赛对局未在本数据集内。

## 六、复现

```
python sniper_study/extract_features.py   # 85场遥测→features/
python sniper_study/fetch_top_matches.py  # n>=3嫌疑人比赛详情
# 分析脚本见会话记录；中间产物:
#   appearances.json / suspects.json / exposure_test.json / pair_conc.json
#   behavior.json / landing.json / quit_analysis.json / suspect_histories.json
#   crowd_combat.json / exclusion.json(排除指标) / pursuit2.json(追击v3) / timeline_flags.json(前后局)
```

## 附录B 可疑对局明细(嫌疑人视角回放链接,共13场)

| 对局 | 时间 | 服/图 | 嫌疑人(该场用名) | 嫌疑人回放 | 选手(使用人) | 选手回放 | 可疑点 |
|---|---|---|---|---|---|---|---|
| `039ca015` | 9-1 19:44 | AS/米拉玛 | Dragonproud_sky | [Dragonproud_sky](https://pubg.plus/en/replay?matches=039ca015-162b-486d-a0e2-ec7158782145&player=Dragonproud_sky) | Boliang(3Bbuff)<br>iL1u(DayDayOuO) | [Boliang](https://pubg.plus/en/replay?matches=039ca015-162b-486d-a0e2-ec7158782145&player=3Bbuff)·[iL1u](https://pubg.plus/en/replay?matches=039ca015-162b-486d-a0e2-ec7158782145&player=DayDayOuO) | 落点2.0km(旋转接战),888s/1015s团灭本组双人(狙击枪+机枪) |
| `804abae9` | 8-30 19:58 | AS/米拉玛 | Yazhe-KP | [Yazhe-KP](https://pubg.plus/en/replay?matches=804abae9-30e8-4acc-bf84-9c8f237c4081&player=Yazhe-KP) | PeeKk1ng(4WM_ASQ0926)<br>SuiX1ngKK(Cue4fizAQRA) | [PeeKk1ng](https://pubg.plus/en/replay?matches=804abae9-30e8-4acc-bf84-9c8f237c4081&player=4WM_ASQ0926)·[SuiX1ngKK](https://pubg.plus/en/replay?matches=804abae9-30e8-4acc-bf84-9c8f237c4081&player=Cue4fizAQRA) | 落点741m,549s击杀选手;进杯赛局前11min等待空档 |
| `a933c9cd` | 9-1 22:04 | SEA/米拉玛 | XX-STAR-XX1 | [XX-STAR-XX1](https://pubg.plus/en/replay?matches=a933c9cd-093b-4ab6-bddd-7519297125b8&player=XX-STAR-XX1) | Axidd(7Bebebe_)<br>Solo9(January_BiG) | [Axidd](https://pubg.plus/en/replay?matches=a933c9cd-093b-4ab6-bddd-7519297125b8&player=7Bebebe_)·[Solo9](https://pubg.plus/en/replay?matches=a933c9cd-093b-4ab6-bddd-7519297125b8&player=January_BiG) | 落点距选手28m,211s/233s团灭本组双人(ACE32) |
| `217ad582` | 9-1 21:35 | SEA/米拉玛 | XX-STAR-XX1、Relieved_Qinss、Relieved_Baooo、ShuiZuanDaKong、ghW6wtFhNS | [XX-STAR-XX1](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=XX-STAR-XX1)、[Relieved_Qinss](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=Relieved_Qinss)、[Relieved_Baooo](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=Relieved_Baooo)、[ShuiZuanDaKong](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=ShuiZuanDaKong)、[ghW6wtFhNS](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=ghW6wtFhNS) | 明柒柒(III7722II)<br>kk(OVOVOOOV) | [明柒柒](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=III7722II)·[kk](https://pubg.plus/en/replay?matches=217ad582-f008-48c6-989d-2485d85a5dd4&player=OVOVOOOV) | 5人从2.6~3.6km奔袭合围明柒柒&kk组;XX-STAR-XX1抵达后1550s击杀选手(跨场第3杀) |
| `b1dfe084` | 8-31 23:20 | SEA/米拉玛 | 66-666-6-66 | [66-666-6-66](https://pubg.plus/en/replay?matches=b1dfe084-f6e2-4594-8302-65a355083ed5&player=66-666-6-66) | Cui71(GOD_98-)<br>04NB(DZ-HeZi-88330) | [Cui71](https://pubg.plus/en/replay?matches=b1dfe084-f6e2-4594-8302-65a355083ed5&player=GOD_98-)·[04NB](https://pubg.plus/en/replay?matches=b1dfe084-f6e2-4594-8302-65a355083ed5&player=DZ-HeZi-88330) | 奔袭3.3km(+540s抵达)后766s拳击+雷团灭本组双人;进杯赛局前15min等待空档 |
| `c6542a66` | 8-31 22:21 | SEA/米拉玛 | GB-zazhong、ntcag、YICCCCCC | [GB-zazhong](https://pubg.plus/en/replay?matches=c6542a66-269a-45ff-a453-f4958987c8bb&player=GB-zazhong)、[ntcag](https://pubg.plus/en/replay?matches=c6542a66-269a-45ff-a453-f4958987c8bb&player=ntcag)、[YICCCCCC](https://pubg.plus/en/replay?matches=c6542a66-269a-45ff-a453-f4958987c8bb&player=YICCCCCC) | 11ovo(76i2_-)<br>陈(BigHead_XxHD) | [11ovo](https://pubg.plus/en/replay?matches=c6542a66-269a-45ff-a453-f4958987c8bb&player=76i2_-)·[陈](https://pubg.plus/en/replay?matches=c6542a66-269a-45ff-a453-f4958987c8bb&player=BigHead_XxHD) | GB-zazhong落点148m、全程100%时间在选手250m内,3杀团灭;进杯赛局前13min空档;ntcag/YICCCCCC开局约60s即退 |
| `d2c0cfd7` | 8-29 20:16 | AS/米拉玛 | TianYi1947 | [TianYi1947](https://pubg.plus/en/replay?matches=d2c0cfd7-bb86-42b5-98b9-04691caaeb75&player=TianYi1947) | Lilghost(CandyBB--_)<br>Wenbo(weirdo_im) | [Lilghost](https://pubg.plus/en/replay?matches=d2c0cfd7-bb86-42b5-98b9-04691caaeb75&player=CandyBB--_)·[Wenbo](https://pubg.plus/en/replay?matches=d2c0cfd7-bb86-42b5-98b9-04691caaeb75&player=weirdo_im) | 奔袭3.2km(+1140s抵达)后1522s团灭本组双人 |
| `e654ffe5` | 9-1 22:10 | SEA/米拉玛 | Cool_Shark、Cool_iKun_-、SnD-1990、ZKI-OKOLAJ | [Cool_Shark](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=Cool_Shark)、[Cool_iKun_-](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=Cool_iKun_-)、[SnD-1990](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=SnD-1990)、[ZKI-OKOLAJ](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=ZKI-OKOLAJ) | Shen(MICKEYMOUSEOK666)<br>SpaceMan(HelloKittyOK666) | [Shen](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=MICKEYMOUSEOK666)·[SpaceMan](https://pubg.plus/en/replay?matches=e654ffe5-cf35-4b0a-9f2e-02f736310ce3&player=HelloKittyOK666) | Cool_Shark+Cool_iKun_同时击杀双人(1390s);SnD-1990/ZKI-OKOLAJ奔袭2.6km合围;ZKI-OKOLAJ当日一场246s logout(基线0/51295) |
| `34a286ba` | 9-5 21:15 | SEA/泰戈 | NAATIAH、ShuiJ1aoDaWang- | [NAATIAH](https://pubg.plus/en/replay?matches=34a286ba-86f6-45d5-9846-b4d5cea7c0d6&player=NAATIAH)、[ShuiJ1aoDaWang-](https://pubg.plus/en/replay?matches=34a286ba-86f6-45d5-9846-b4d5cea7c0d6&player=ShuiJ1aoDaWang-) | 不知名(yin-0710)<br>走马(qwertyuiop_50541) | [不知名](https://pubg.plus/en/replay?matches=34a286ba-86f6-45d5-9846-b4d5cea7c0d6&player=yin-0710)·[走马](https://pubg.plus/en/replay?matches=34a286ba-86f6-45d5-9846-b4d5cea7c0d6&player=qwertyuiop_50541) | NAATIAH 1304s击杀选手;同队4人多次接近选手78~325m |
| `7274cc8c` | 8-29 23:40 | SEA/米拉玛 | KhaoJee、ohmyo31 | [KhaoJee](https://pubg.plus/en/replay?matches=7274cc8c-90f8-494e-ad5b-2c076681752d&player=KhaoJee)、[ohmyo31](https://pubg.plus/en/replay?matches=7274cc8c-90f8-494e-ad5b-2c076681752d&player=ohmyo31) | MMing(4WM_ASQ0926)<br>i26v6(Cue4fizAQRA) | [MMing](https://pubg.plus/en/replay?matches=7274cc8c-90f8-494e-ad5b-2c076681752d&player=4WM_ASQ0926)·[i26v6](https://pubg.plus/en/replay?matches=7274cc8c-90f8-494e-ad5b-2c076681752d&player=Cue4fizAQRA) | 延迟接近驻留选手(122~144m);贴身时间占比35% |
| `b78ee504` | 9-2 19:09 | AS/艾伦格 | i11bbi | [i11bbi](https://pubg.plus/en/replay?matches=b78ee504-aa98-4a35-b46b-d00a7ca54cff&player=i11bbi) | Dec12th(MICKEYMOUSEOK666)<br>SuZe(HelloKittyOK666) | [Dec12th](https://pubg.plus/en/replay?matches=b78ee504-aa98-4a35-b46b-d00a7ca54cff&player=MICKEYMOUSEOK666)·[SuZe](https://pubg.plus/en/replay?matches=b78ee504-aa98-4a35-b46b-d00a7ca54cff&player=HelloKittyOK666) | 落点距选手87m、全程100%时间贴身,303s团灭本组双人;i11bbi系CrissBZ杯赛期间改名 |
| `c21cb548` | 8-31 20:28 | AS/米拉玛 | DogeEarth、MCC-BanMeng、ZQuanH9、Mr-Rxsm | [DogeEarth](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=DogeEarth)、[MCC-BanMeng](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=MCC-BanMeng)、[ZQuanH9](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=ZQuanH9)、[Mr-Rxsm](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=Mr-Rxsm) | 汐月(CandyBB--_)<br>xs(weirdo_im) | [汐月](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=CandyBB--_)·[xs](https://pubg.plus/en/replay?matches=c21cb548-8db9-4b97-bb12-7cc009917a3d&player=weirdo_im) | DogeEarth落地后37%时间贴身选手250m内、0交战;MCC-BanMeng/ZQuanH9/Mr-Rxsm奔袭3.3~4.4km抵达,MCC-BanMeng 1240s击杀CandyBB--_ |
| `09f40150` | 8-31 22:51 | SEA/米拉玛 | DogeEarth | [DogeEarth](https://pubg.plus/en/replay?matches=09f40150-5bb8-4f1a-8d8f-187f309f59a2&player=DogeEarth) | 意识DT(94db)<br>700(MMMWMMMMMMMMMMMW) | [意识DT](https://pubg.plus/en/replay?matches=09f40150-5bb8-4f1a-8d8f-187f309f59a2&player=94db)·[700](https://pubg.plus/en/replay?matches=09f40150-5bb8-4f1a-8d8f-187f309f59a2&player=MMMWMMMMMMMMMMMW) | 落点距选手2614m,游走4km+多次接近至250m内(占18%时间),全程未与选手接战;该场为意识DT&700组 |

## 附录C 全部85场对局的选手账号↔使用人对照

| # | 对局ID | 时间 | 服 | 地图 | 使用人1 | 当日账号1 | 使用人2 | 当日账号2 | API地图 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `47794c27` | 8-29 19:03 | AS | 艾伦格 | 狗子 | GOD_98- | 99 | DZ-HeZi-88330 | Baltic_Main |
| 2 | `32da2c7c` | 8-29 19:42 | AS | 米拉玛 | OneDragon | 2iDD- | HaoSkr | Meiguibb | Desert_Main |
| 3 | `d2c0cfd7` | 8-29 20:16 | AS | 米拉玛 | Lilghost | CandyBB--_ | Wenbo | weirdo_im | Desert_Main |
| 4 | `0818a15f` | 8-29 20:48 | AS | 米拉玛 | Rain | 94db | Shan | MMMWMMMMMMMMMMMW | Desert_Main |
| 5 | `83490382` | 8-29 21:05 | AS | 米拉玛 | MMing | 4WM_ASQ0926 | i26v6 | Cue4fizAQRA | Desert_Main |
| 6 | `e607b483` | 8-29 21:26 | AS | 米拉玛 | VX30 | 76i2_- | 小飞 | BigHead_XxHD | Desert_Main |
| 7 | `42293dbc` | 8-29 22:09 | SEA | 米拉玛 | VX30 | 76i2_- | 小飞 | BigHead_XxHD | Desert_Main |
| 8 | `32aff732` | 8-29 22:41 | SEA | 米拉玛 | OneDragon | 2iDD- | HaoSkr | Meiguibb | Desert_Main |
| 9 | `010551bc` | 8-29 23:16 | SEA | 米拉玛 | Rain | 94db | Shan | MMMWMMMMMMMMMMMW | Desert_Main |
| 10 | `7274cc8c` | 8-29 23:40 | SEA | 米拉玛 | MMing | 4WM_ASQ0926 | i26v6 | Cue4fizAQRA | Desert_Main |
| 11 | `c36be949` | 8-30 00:12 | SEA | 米拉玛 | Lilghost | CandyBB--_ | Wenbo | weirdo_im | Desert_Main |
| 12 | `0aba02a0` | 8-30 00:27 | SEA | 艾伦格 | 狗子 | GOD_98- | 99 | DZ-HeZi-88330 | Baltic_Main |
| 13 | `c07ac45a` | 8-30 19:01 | AS | 米拉玛 | Chue | BigHead_XxHD | HangZai | 76i2_- | Desert_Main |
| 14 | `ff87e7a7` | 8-30 19:23 | AS | 米拉玛 | xiaohaixxxx | GOD_98- | CRAZY112 | DZ-HeZi-88330 | Desert_Main |
| 15 | `804abae9` | 8-30 19:58 | AS | 米拉玛 | PeeKk1ng | 4WM_ASQ0926 | SuiX1ngKK | Cue4fizAQRA | Desert_Main |
| 16 | `c01e2e0f` | 8-30 20:33 | AS | 米拉玛 | Yuyu | MMMWMMMMMMMMMMMW | Jing | 94db | Desert_Main |
| 17 | `38b5a9c8` | 8-30 20:50 | AS | 艾伦格 | 鬼狙 | Meiguibb | AI | 2iDD- | Baltic_Main |
| 18 | `36e0f19b` | 8-30 21:06 | SEA | 米拉玛 | 鬼狙 | Meiguibb | AI | 2iDD- | Desert_Main |
| 19 | `e8bda60e` | 8-30 21:18 | SEA | 米拉玛 | Yuyu | MMMWMMMMMMMMMMMW | Jing | 94db | Desert_Main |
| 20 | `4f13fa3b` | 8-30 21:50 | AS | 艾伦格 | JiaoYang | CandyBB--_ | LongSkr | weirdo_im | Baltic_Main |
| 21 | `8c648f1f` | 8-30 21:58 | SEA | 米拉玛 | Chue | BigHead_XxHD | HangZai | 76i2_- | Desert_Main |
| 22 | `86f3169d` | 8-30 22:32 | SEA | 米拉玛 | xiaohaixxxx | GOD_98- | CRAZY112 | DZ-HeZi-88330 | Desert_Main |
| 23 | `51c92165` | 8-30 22:39 | SEA | 米拉玛 | PeeKk1ng | 4WM_ASQ0926 | SuiX1ngKK | Cue4fizAQRA | Desert_Main |
| 24 | `47e3db29` | 8-30 23:02 | SEA | 米拉玛 | JiaoYang | CandyBB--_ | LongSkr | weirdo_im | Desert_Main |
| 25 | `9886329e` | 8-31 19:01 | AS | 米拉玛 | HSmm | 4WM_ASQ0926 | WINDah | Cue4fizAQRA | Desert_Main |
| 26 | `f887ba76` | 8-31 19:11 | AS | 米拉玛 | Cui71 | GOD_98- | 04NB | DZ-HeZi-88330 | Desert_Main |
| 27 | `f4f36acf` | 8-31 19:40 | AS | 米拉玛 | 11ovo | 76i2_- | 陈 | BigHead_XxHD | Desert_Main |
| 28 | `92f57d3f` | 8-31 19:50 | AS | 米拉玛 | DJinRong | 2iDD- | roll | Meiguibb | Desert_Main |
| 29 | `513ebf4f` | 8-31 19:56 | AS | 米拉玛 | 意识DT | 94db | 700 | MMMWMMMMMMMMMMMW | Desert_Main |
| 30 | `c21cb548` | 8-31 20:28 | AS | 米拉玛 | 汐月 | CandyBB--_ | xs | weirdo_im | Desert_Main |
| 31 | `edb48bf2` | 8-31 20:55 | SEA | 荣都 | DJinRong | 2iDD- | roll | Meiguibb | Neon_Main |
| 32 | `155c4e31` | 8-31 21:25 | SEA | 米拉玛 | HSmm | 4WM_ASQ0926 | WINDah | Cue4fizAQRA | Desert_Main |
| 33 | `5b5a2387` | 8-31 22:08 | SEA | 米拉玛 | 汐月 | CandyBB--_ | xs | weirdo_im | Desert_Main |
| 34 | `c6542a66` | 8-31 22:21 | SEA | 米拉玛 | 11ovo | 76i2_- | 陈 | BigHead_XxHD | Desert_Main |
| 35 | `09f40150` | 8-31 22:51 | SEA | 米拉玛 | 意识DT | 94db | 700 | MMMWMMMMMMMMMMMW | Desert_Main |
| 36 | `b1dfe084` | 8-31 23:20 | SEA | 米拉玛 | Cui71 | GOD_98- | 04NB | DZ-HeZi-88330 | Desert_Main |
| 37 | `1607076a` | 8-31 23:36 | SEA | 荣都 | DJinRong | 2iDD- | roll | Meiguibb | Neon_Main |
| 38 | `7b4af720` | 9-1 19:01 | AS | 米拉玛 | KeyS | WanM87342 | Xnan | Aixinzuimei | Desert_Main |
| 39 | `e5eaf37a` | 9-1 19:30 | AS | 米拉玛 | Axidd | 7Bebebe_ | Solo9 | January_BiG | Desert_Main |
| 40 | `039ca015` | 9-1 19:44 | AS | 米拉玛 | Boliang | 3Bbuff | iL1u | DayDayOuO | Desert_Main |
| 41 | `35679c02` | 9-1 20:03 | AS | 米拉玛 | 明柒柒 | III7722II | kk | OVOVOOOV | Desert_Main |
| 42 | `8dc6f63c` | 9-1 20:15 | AS | 米拉玛 | Shen | MICKEYMOUSEOK666 | SpaceMan | HelloKittyOK666 | Desert_Main |
| 43 | `1df6617d` | 9-1 20:30 | AS | 米拉玛 | 马平 | dsdwfnygsaew | Xbei | TOPM249-___- | Desert_Main |
| 44 | `b6dfc346` | 9-1 21:04 | SEA | 米拉玛 | Boliang | 3Bbuff | iL1u | DayDayOuO | Desert_Main |
| 45 | `217ad582` | 9-1 21:35 | SEA | 米拉玛 | 明柒柒 | III7722II | kk | OVOVOOOV | Desert_Main |
| 46 | `a933c9cd` | 9-1 22:04 | SEA | 米拉玛 | Axidd | 7Bebebe_ | Solo9 | January_BiG | Desert_Main |
| 47 | `e654ffe5` | 9-1 22:10 | SEA | 米拉玛 | Shen | MICKEYMOUSEOK666 | SpaceMan | HelloKittyOK666 | Desert_Main |
| 48 | `bf3dfe2f` | 9-1 22:37 | SEA | 米拉玛 | KeyS | WanM87342 | Xnan | Aixinzuimei | Desert_Main |
| 49 | `99b73b1a` | 9-1 22:48 | SEA | 米拉玛 | 马平 | dsdwfnygsaew | Xbei | TOPM249-___- | Desert_Main |
| 50 | `89c96bcc` | 9-2 19:01 | AS | 艾伦格 | Xihan | III7722II | DouZiVv | OVOVOOOV | Baltic_Main |
| 51 | `b78ee504` | 9-2 19:09 | AS | 艾伦格 | Dec12th | MICKEYMOUSEOK666 | SuZe | HelloKittyOK666 | Baltic_Main |
| 52 | `510d960a` | 9-2 19:19 | AS | 艾伦格 | pd | 3Bbuff | lunlun | DayDayOuO | Baltic_Main |
| 53 | `e17eebd5` | 9-2 19:50 | AS | 艾伦格 | 大能 | dsdwfnygsaew | 爱国 | TOPM249-___- | Baltic_Main |
| 54 | `9742a9b3` | 9-2 20:13 | AS | 艾伦格 | XiaoHuxxXX | 7Bebebe_ | Dong | January_BiG | Baltic_Main |
| 55 | `286b37d5` | 9-2 20:23 | AS | 泰戈 | tiantian | WanM87342 | xwudd | Aixinzuimei | Tiger_Main |
| 56 | `997ef53e` | 9-2 20:46 | SEA | 荣都 | Dec12th | MICKEYMOUSEOK666 | SuZe | HelloKittyOK666 | Neon_Main |
| 57 | `1c577902` | 9-2 21:19 | SEA | 荣都 | 大能 | dsdwfnygsaew | 爱国 | TOPM249-___- | Neon_Main |
| 58 | `a3f7dcd7` | 9-2 21:40 | SEA | 艾伦格 | Xihan | III7722II | DouZiVv | OVOVOOOV | Baltic_Main |
| 59 | `a5559d48` | 9-2 22:13 | SEA | 荣都 | XiaoHuxxXX | 7Bebebe_ | Dong | January_BiG | Neon_Main |
| 60 | `f08ed8d1` | 9-2 22:42 | SEA | 艾伦格 | tiantian | WanM87342 | xwudd | Aixinzuimei | Baltic_Main |
| 61 | `9269da01` | 9-2 22:59 | SEA | 荣都 | pd | 3Bbuff | lunlun | DayDayOuO | Neon_Main |
| 62 | `aa679aba` | 9-3 19:00 | AS | 艾伦格 | tte | III7722II | nan | OVOVOOOV | Baltic_Main |
| 63 | `c892be8c` | 9-3 19:20 | AS | 艾伦格 | 沐白(MuBai) | MICKEYMOUSEOK666 | 新一(XinYi) | HelloKittyOK666 | Baltic_Main |
| 64 | `55492d77` | 9-3 19:49 | AS | 艾伦格 | 不知名 | 3Bbuff | 走马 | DayDayOuO | Baltic_Main |
| 65 | `61a06e4b` | 9-3 20:00 | AS | 艾伦格 | KKong | BAOBAONO1_ | 小白 | czczzsodjjd222 | Baltic_Main |
| 66 | `dc69b071` | 9-3 20:29 | AS | 艾伦格 | fffeng | 7Bebebe_ | 03 | January_BiG | Baltic_Main |
| 67 | `fa807f95` | 9-3 20:57 | AS | 艾伦格 | 阔澜 | dsdwfnygsaew | 苏宇 | TOPM249-___- | Baltic_Main |
| 68 | `3ca46262` | 9-3 21:14 | SEA | 泰戈 | 不知名 | 3Bbuff | 走马 | DayDayOuO | Tiger_Main |
| 69 | `c6df7c8e` | 9-3 21:23 | SEA | 艾伦格 | 沐白(MuBai) | MICKEYMOUSEOK666 | 新一(XinYi) | HelloKittyOK666 | Baltic_Main |
| 70 | `71d39b1c` | 9-3 21:39 | SEA | 艾伦格 | tte | III7722II | nan | OVOVOOOV | Baltic_Main |
| 71 | `6ef77937` | 9-3 21:51 | SEA | 艾伦格 | fffeng | 7Bebebe_ | 03 | January_BiG | Baltic_Main |
| 72 | `704d9fe4` | 9-3 22:19 | SEA | 艾伦格 | 阔澜 | dsdwfnygsaew | 苏宇 | TOPM249-___- | Baltic_Main |
| 73 | `46676089` | 9-3 22:28 | SEA | 艾伦格 | KKong | BAOBAONO1_ | 小白 | czczzsodjjd222 | Baltic_Main |
| 74 | `72d100ec` | 9-5 19:01 | AS | 泰戈 | 不知名 | yin-0710 | 走马 | qwertyuiop_50541 | Tiger_Main |
| 75 | `22cf23cf` | 9-5 19:12 | AS | 艾伦格 | OneDragon | dadenniluancuan1 | HaoSkr | YINYILINGZHU | Baltic_Main |
| 76 | `3969fcc3` | 9-5 19:20 | AS | 艾伦格 | 明柒柒 | iiiiLuckyOooo | kk | ooluckyooo | Baltic_Main |
| 77 | `8b0e091e` | 9-5 19:45 | AS | 艾伦格 | Shen | WANGZHEGUILAIOVO | SpaceMan | xiaogegeyimie | Baltic_Main |
| 78 | `a646f99f` | 9-5 19:58 | AS | 艾伦格 | Rain | PSBGJSWD1122 | Shan | xiangjinjuesai | Baltic_Main |
| 79 | `ff7afdc5` | 9-5 20:31 | AS | 艾伦格 | Boliang | 5Bbuff | iL1u | daydayday_- | Baltic_Main |
| 80 | `22d89b2d` | 9-5 20:44 | SEA | 艾伦格 | OneDragon | dadenniluancuan1 | HaoSkr | YINYILINGZHU | Baltic_Main |
| 81 | `34a286ba` | 9-5 21:15 | SEA | 泰戈 | 不知名 | yin-0710 | 走马 | qwertyuiop_50541 | Tiger_Main |
| 82 | `035ece50` | 9-5 21:40 | SEA | 荣都 | Shen | WANGZHEGUILAIOVO | SpaceMan | xiaogegeyimie | Neon_Main |
| 83 | `d78d7be1` | 9-5 22:11 | SEA | 荣都 | Boliang | 5Bbuff | iL1u | daydayday_- | Neon_Main |
| 84 | `4421c8f7` | 9-5 22:44 | SEA | 荣都 | Rain | PSBGJSWD1122 | Shan | xiangjinjuesai | Neon_Main |
| 85 | `c8e4cff0` | 9-5 23:06 | SEA | 艾伦格 | 明柒柒 | iiiiLuckyOooo | kk | ooluckyooo | Baltic_Main |
