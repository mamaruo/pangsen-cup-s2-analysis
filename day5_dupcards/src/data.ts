export type EvType = "DBNO" | "Kill" | "Revive";

export interface Ev {
  ts: number; // 秒，相对比赛开始
  type: EvType;
  attacker: string; // 游戏内名
  acct?: string | null;
  victim: string;
  weapon?: string | null; // damageCauserName
  reason?: string | null;
}

export interface DupVictim {
  name: string;
  events: Ev[];
}

export interface PlayerStat {
  zh: string;
  ingame: string;
  kills: number; // 总击杀(不去重)
  dupKills: number; // 其中重复击杀
}

export interface MatchCard {
  title: string;
  datetime: string; // 如 "9-2 21:40"
  map: string;
  win: boolean;
  players: [PlayerStat, PlayerStat];
  scorePublished: number; // 胖森公布分数(不扣除重复)
  scoreCorrect: number; // 理论正确分数(去重)
  note: string;
  dupVictims: DupVictim[];
}

const AID = {
  xihan: "account.eb9b15d4b5a4464f9c9466fb9d260a54",
  douzi: "account.0948de9e482b4d65abd9362281a04f3e",
  xiaohu: "account.60e729fc9ed741ee92b3d7fd4c88f9ba",
  dong: "account.0a851679df5b4d91b4b831aa4dbfa302",
};

export const CARDS: MatchCard[] = [  {
    title: "胖森杯S2 E组第2轮",
    datetime: "9-2 21:40",
    map: "艾伦格",
    win: true,
    players: [
      { zh: "兮涵", ingame: "III7722II", kills: 12, dupKills: 0 },
      { zh: "豆子", ingame: "OVOVOOOV", kills: 5, dupKills: 2 },
    ],
    scorePublished: 68,
    scoreCorrect: 60,
    note: "豆子对Wanza1_-、Like1u的第二次击杀与兮涵重复，不计分，故理论分数为60。",
    dupVictims: [
      {
        name: "Wanza1_-",
        events: [
          { ts: 727.957, type: "DBNO", attacker: "III7722II", acct: AID.xihan, victim: "Wanza1_-", weapon: "WeapAUG_C", reason: "PelvisShot" },
          { ts: 737.068, type: "Kill", attacker: "III7722II", acct: AID.xihan, victim: "Wanza1_-", weapon: "WeapAUG_C", reason: "PelvisShot" },
          { ts: 1360.351, type: "Kill", attacker: "OVOVOOOV", acct: AID.douzi, victim: "Wanza1_-", weapon: "WeapM249_C", reason: "TorsoShot" },
        ],
      },
      {
        name: "Like1u",
        events: [
          { ts: 722.443, type: "DBNO", attacker: "III7722II", acct: AID.xihan, victim: "Like1u", weapon: "WeapKar98k_C", reason: "HeadShot" },
          { ts: 742.461, type: "Kill", attacker: "III7722II", acct: AID.xihan, victim: "Like1u", weapon: "WeapKar98k_C", reason: "HeadShot" },
          { ts: 1225.546, type: "DBNO", attacker: "OVOVOOOV", acct: AID.douzi, victim: "Like1u", weapon: "WeapM249_C", reason: "HeadShot" },
          { ts: 1242.602, type: "Kill", attacker: "OVOVOOOV", acct: AID.douzi, victim: "Like1u", weapon: "WeapM249_C", reason: "HeadShot" },
        ],
      },
    ],
  },
  {
    title: "胖森杯S2 E组第2轮",
    datetime: "9-2 22:13",
    map: "荣都",
    win: true,
    players: [
      { zh: "小虎", ingame: "7Bebebe_", kills: 4, dupKills: 0 },
      { zh: "东东", ingame: "January_BiG", kills: 14, dupKills: 1 },
    ],
    scorePublished: 72,
    scoreCorrect: 68,
    note: "东东对Cupid_LLL的第二次击杀（破片手榴弹）与第一次重复，不计分，故理论分数为68。",
    dupVictims: [
      {
        name: "Cupid_LLL",
        events: [
          { ts: 309.304, type: "DBNO", attacker: "January_BiG", acct: AID.dong, victim: "Cupid_LLL", weapon: "WeapMk12_C", reason: "TorsoShot" },
          { ts: 318.469, type: "Kill", attacker: "January_BiG", acct: AID.dong, victim: "Cupid_LLL", weapon: "WeapMk12_C", reason: "TorsoShot" },
          { ts: 667.018, type: "DBNO", attacker: "January_BiG", acct: AID.dong, victim: "Cupid_LLL", weapon: "ProjGrenade_C", reason: "NonSpecific" },
          { ts: 674.318, type: "Kill", attacker: "January_BiG", acct: AID.dong, victim: "Cupid_LLL", weapon: "ProjGrenade_C", reason: "NonSpecific" },
        ],
      },    ],
  },
];

const WEAPON_CN: Record<string, string> = {
  "ProjGrenade_C": "破片手榴弹",
  "ProjMolotov_C": "燃烧瓶",
  "WeapMilkCrate_C": "闪光弹",
};

export function weaponLabel(code?: string | null): string | null {
  if (!code) return null;
  if (WEAPON_CN[code]) return WEAPON_CN[code];
  if (code.startsWith("Melee")) return "近战武器";
  return code.replace("Weap", "").replace("_C", "").replace(/_/g, " ");
}

const ICON_BASE = "/icons";

const ICON_FIX: Record<string, string> = {
  FamasG2: "FAMASG2",
  Grenade: "Grenade",
  Molotov: "Molotov",
};

export function weaponIconUrl(code?: string | null): string | null {
  if (!code) return null;
  const inner = code.startsWith("Weap")
    ? code.slice(4).replace("_C", "")
    : code.replace(/^Proj/, "").replace("_C", "");
  const file = ICON_FIX[inner] ?? inner;
  return `${ICON_BASE}/weapon/${file}.png`;
}

export function killfeedIconUrl(ev: Ev): string {
  const headshot = ev.reason === "HeadShot";
  if (ev.type === "DBNO")
    return `${ICON_BASE}/killfeed/${headshot ? "Headshot_DBNO" : "DBNO"}.png`;
  return `${ICON_BASE}/killfeed/${headshot ? "Headshot" : "Death"}.png`;
}

/** 游戏内名中间部分打码：III7722II -> III***II */
export function maskName(name: string): string {
  if (name.length <= 5) return name;
  return name.slice(0, 3) + "***" + name.slice(-2);
}

/** 毫秒时间 -> { m, s, ms }；如 1242.602 -> 20:42.602 */
export function gameClock(ts: number) {
  const total = Math.floor(ts);
  const m = Math.floor(total / 60);
  const s = total % 60;
  const ms = Math.round((ts - total) * 1000);
  const pad = (n: number, w = 2) => String(n).padStart(w, "0");
  return { main: `${pad(m)}:${pad(s)}`, ms: pad(ms, 3) };
}
