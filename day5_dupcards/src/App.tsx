import { useEffect, useRef, useState } from "react";
import { toPng } from "html-to-image";
import {
  CARDS,
  weaponLabel,
  weaponIconUrl,
  killfeedIconUrl,
  maskName,
  gameClock,
  type MatchCard,
  type Ev,
} from "@/data";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

const DESIGN_W = 1080;
const DESIGN_H = 1920;

function useScale() {
  const ref = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.35);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const ro = new ResizeObserver(() => {
      setScale(el.clientWidth / DESIGN_W);
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return { ref, scale };
}

function ScaledCard({ children, maxW = 420 }: { children: React.ReactNode; maxW?: number }) {
  const { ref, scale } = useScale();
  return (
    <div ref={ref} className="w-full" style={{ maxWidth: maxW }}>
      <div
        style={{
          width: DESIGN_W,
          height: DESIGN_H,
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          marginBottom: (scale - 1) * DESIGN_H,
        }}
      >
        {children}
      </div>
    </div>
  );
}

function attackerDisplay(ev: Ev): React.ReactNode {
  if (!ev.acct) return <span className="font-semibold">{ev.attacker}</span>;
  const zh =
    ev.acct === "account.eb9b15d4b5a4464f9c9466fb9d260a54" ? "兮涵"
    : ev.acct === "account.0948de9e482b4d65abd9362281a04f3e" ? "豆子"
    : ev.acct === "account.60e729fc9ed741ee92b3d7fd4c88f9ba" ? "小虎"
    : "东东";
  return (
    <span className="whitespace-nowrap">
      <span className="font-black text-amber-700">{zh}</span>
      <span className="font-semibold text-[28px] text-zinc-600">({maskName(ev.attacker)})</span>
    </span>
  );
}

function TimeView({ ts }: { ts: number }) {
  const { main, ms } = gameClock(ts);
  return (
    <span className="font-mono tabular-nums font-bold text-zinc-800 shrink-0">
      <span className="text-[34px]">{main}</span>
      <span className="text-[27px] text-zinc-600">.{ms}</span>
    </span>
  );
}

function EventRow({ ev }: { ev: Ev }) {
  const wIcon = weaponIconUrl(ev.weapon);
  const wLabel = weaponLabel(ev.weapon);
  const isThrowable = !!ev.weapon && !ev.weapon.startsWith("Weap");
  return (
    <div className="flex-1 min-h-[60px] max-h-[112px] flex items-center gap-3 rounded-xl bg-muted px-5">
      <TimeView ts={ev.ts} />
      <span className="text-[34px] leading-none truncate min-w-0">{attackerDisplay(ev)}</span>
      <span className="bg-zinc-900 rounded-lg px-2 py-1.5 flex items-center gap-1.5 shrink-0">
        {wIcon && !isThrowable && (
          <img
            src={wIcon}
            alt={wLabel ?? ""}
            className="h-[40px] w-[54px] object-contain"
            style={{ transform: "scaleX(-1)" }}
          />
        )}
        {wIcon && isThrowable && (
          <img
            src={wIcon}
            alt={wLabel ?? ""}
            className="h-[38px] w-[38px] object-contain"
            style={{ filter: "brightness-0 invert", transform: "scaleX(-1)" }}
          />
        )}
        <img src={killfeedIconUrl(ev)} alt={ev.type} className="h-[38px] w-[38px] object-contain" />
      </span>
      <span className="text-[34px] font-bold leading-none whitespace-nowrap">{ev.victim}</span>
    </div>
  );
}

function PlayerPanel({ p }: { p: MatchCard["players"][0] }) {
  return (
    <Card className="flex-1 rounded-3xl border-2">
      <CardHeader className="px-7 pt-6 gap-1">
        <CardTitle className="text-[44px] font-black">{p.zh}</CardTitle>
        <CardDescription className="text-[28px] font-mono font-semibold text-zinc-600">
          {maskName(p.ingame)}
        </CardDescription>
      </CardHeader>
      <CardContent className="px-7 pb-6 pt-2">
        <Separator className="mb-5" />
        <div className="flex items-center justify-between">
          <span className="text-[30px] font-semibold">
            击杀<span className="text-[46px] font-black align-middle">{p.kills}</span>
          </span>
          <Badge
            variant={p.dupKills > 0 ? "destructive" : "secondary"}
            className={cn("text-[28px] px-4 py-1 rounded-xl", p.dupKills === 0 && "text-zinc-700")}
          >
            重复{p.dupKills}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}

function ReportCard({ card }: { card: MatchCard }) {
  return (
    <div
      className="bg-zinc-200 p-3"
      style={{ width: DESIGN_W, height: DESIGN_H, boxSizing: "border-box" }}
    >
      <Card className="h-full w-full rounded-[2.2rem] border-2 shadow-none flex flex-col">
        <CardHeader className="pl-[60px] pr-[180px] pt-[60px] gap-4">
          <div className="flex items-center gap-5">
            <CardTitle className="text-[64px] font-black leading-none tracking-wide">
              {card.title}
            </CardTitle>
            {card.win && (
              <Badge className="px-3 py-1 rounded-2xl">
                <img src="/icons/chicken.png" alt="吃鸡" className="h-[52px] w-auto" />
              </Badge>
            )}
          </div>
          <CardDescription className="flex items-center gap-4 text-[32px]">
            <span className="font-mono font-bold text-zinc-800">{card.datetime}</span>
            <Badge variant="outline" className="text-[30px] px-4 py-0.5 rounded-xl font-semibold text-zinc-800">
              {card.map}
            </Badge>
          </CardDescription>
        </CardHeader>

        <CardContent className="pl-[60px] pr-[180px] pb-[56px] pt-2 flex-1 min-h-0 flex flex-col gap-6">
          {/* 选手数据 */}
          <div className="flex gap-5">
            {card.players.map((p) => (
              <PlayerPanel key={p.ingame} p={p} />
            ))}
          </div>

          {/* 分数对比 */}
          <Card className="rounded-3xl border-2">
            <CardHeader className="px-8 pt-6 pb-1 flex-row items-center justify-between">
              <CardTitle className="text-[34px] font-bold">分数对比</CardTitle>
              <span className="text-[32px] font-bold">差{card.scorePublished - card.scoreCorrect}分</span>
            </CardHeader>
            <CardContent className="px-8 pb-8 pt-2 flex items-end gap-10">
              <div>
                <div className="text-[30px] font-bold text-orange-700">胖森公布分数</div>
                <div className="text-[96px] font-black leading-none text-orange-600">
                  {card.scorePublished}
                </div>
              </div>
              <div className="pb-5 text-[36px] font-black text-zinc-800">vs</div>
              <div>
                <div className="text-[30px] font-bold text-emerald-700">不计重复淘汰</div>
                <div className="text-[96px] font-black leading-none text-emerald-600">
                  {card.scoreCorrect}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 重复击杀记录 */}
          <div className="flex-1 min-h-0 flex flex-col gap-4">
            <h2 className="text-[42px] font-black leading-none shrink-0">相关记录</h2>
            <div className="flex-1 min-h-0 flex flex-col gap-5">
              {card.dupVictims.map((v) => (
                <Card
                  key={v.name}
                  className="rounded-3xl border-2 min-h-0 flex flex-col overflow-hidden"
                  style={{ flexGrow: v.events.length, flexBasis: 0 }}
                >
                  <CardHeader className="px-7 pt-5 pb-0 flex-row items-center gap-4 shrink-0">
                    <CardTitle className="text-[36px] font-black">{v.name}</CardTitle>
                    <Badge variant="secondary" className="text-[26px] px-3.5 py-1 rounded-lg text-zinc-800 font-semibold">
                      重复目标
                    </Badge>
                  </CardHeader>
                  <CardContent className="px-7 py-4 flex-1 min-h-0 flex flex-col justify-evenly gap-2">
                    {v.events.map((ev, i) => (
                      <EventRow key={i} ev={ev} />
                    ))}
                  </CardContent>
                </Card>
              ))}
            </div>
            <Card className="rounded-3xl border-2 shrink-0">
              <CardContent className="px-8 py-4 text-[30px] leading-relaxed font-medium text-zinc-800">
                <span className="font-black text-zinc-900">说明　</span>
                {card.note}
              </CardContent>
            </Card>
          </div>

          <div className="text-[26px] font-medium text-zinc-600 shrink-0">
            数据来源于PUBG官方API
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function App() {
  const params = new URLSearchParams(window.location.search);
  const maxW = Number(params.get("w") ?? 420);
  const bare = params.has("bare");
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const [saving, setSaving] = useState(false);

  async function saveCard(i: number) {
    const el = cardRefs.current[i];
    if (!el) return;
    setSaving(true);
    try {
      const c = CARDS[i];
      const dataUrl = await toPng(el, { pixelRatio: 2, backgroundColor: "#f4f4f5" });
      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = `${c.title}_${c.datetime}_${c.map}.png`.replace(/:/g, "-");
      a.click();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-300 flex flex-col items-center">
      {!bare && (
        <div className="sticky top-0 z-10 w-full bg-zinc-900 text-white px-6 py-3 flex items-center justify-center gap-5">
          <span className="text-lg font-semibold">胖森杯Day5 · 重复击杀报告卡</span>
          <Button onClick={() => saveCard(0)} disabled={saving} className="text-base">
            {saving ? "生成中…" : "保存卡片1（21:40艾伦格）"}
          </Button>
          <Button onClick={() => saveCard(1)} disabled={saving} className="text-base">
            保存卡片2（22:13荣都）
          </Button>
        </div>
      )}
      <div className="py-8 flex flex-col items-center gap-10">
        {CARDS.map((c, i) => (
          <ScaledCard key={i} maxW={maxW}>
            <div
              ref={(el) => {
                cardRefs.current[i] = el;
              }}
            >
              <ReportCard card={c} />
            </div>
          </ScaledCard>
        ))}
      </div>
    </div>
  );
}
