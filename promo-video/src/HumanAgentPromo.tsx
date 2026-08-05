import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
const fontFamily = 'Microsoft YaHei, PingFang SC, Noto Sans SC, sans-serif';

const C = {
  ink: '#101010',
  paper: '#F6F3EC',
  red: '#FF4D38',
  cyan: '#1AA7A1',
  yellow: '#F2C94C',
  white: '#FFFFFF',
  muted: '#6A6862',
  line: '#C8C4BA',
};

const stage: React.CSSProperties = {
  fontFamily,
  color: C.ink,
  padding: '150px 78px 130px',
  boxSizing: 'border-box',
  overflow: 'hidden',
};

const pop = (frame: number, fps: number, delay = 0) =>
  spring({frame: frame - delay, fps, config: {damping: 16, stiffness: 150}});

const Kicker: React.FC<{children: React.ReactNode; color?: string}> = ({children, color = C.red}) => (
  <div style={{fontSize: 28, fontWeight: 800, color, letterSpacing: 0, marginBottom: 30}}>{children}</div>
);

const Footer: React.FC<{index: string}> = ({index}) => (
  <div style={{position: 'absolute', left: 78, right: 78, bottom: 74, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: 24, fontWeight: 700, color: C.muted}}>
    <span>人味 Agent / open source</span>
    <span>{index}</span>
  </div>
);

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = pop(f, fps);
  const b = pop(f, fps, 18);
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.paper}}>
      <div style={{position: 'absolute', top: 96, left: 78, fontSize: 28, fontWeight: 800}}>我做了一个开源 Skill</div>
      <div style={{marginTop: 250, transform: `translateY(${(1 - a) * 80}px)`, opacity: a, fontSize: 116, lineHeight: 1.08, fontWeight: 900, letterSpacing: 0}}>
        AI 回答很快，<br />
        <span style={{color: C.red}}>却没回到点上。</span>
      </div>
      <div style={{marginTop: 70, transform: `translateY(${(1 - b) * 40}px)`, opacity: b, fontSize: 42, lineHeight: 1.5, fontWeight: 500}}>
        套话、过度解释、没证据也很确定。
      </div>
      <div style={{position: 'absolute', right: -80, bottom: 270, width: 430, height: 430, borderRadius: 215, backgroundColor: C.yellow, transform: `scale(${0.7 + a * 0.3})`}} />
      <Footer index="01 / 07" />
    </AbsoluteFill>
  );
};

const Pain: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = pop(f, fps);
  const b = pop(f, fps, 25);
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.white}}>
      <Kicker>同一句“我今天很难受”</Kicker>
      <div style={{fontSize: 66, lineHeight: 1.15, fontWeight: 900, marginBottom: 70}}>很多 AI 会立刻开始解决你。</div>
      <div style={{opacity: a, transform: `translateX(${(1 - a) * 80}px)`, border: `3px solid ${C.line}`, padding: '38px 40px', fontSize: 34, lineHeight: 1.6, backgroundColor: C.paper}}>
        “我完全理解你的感受。你可以先深呼吸、喝水、写日记……”
      </div>
      <div style={{margin: '42px 0', height: 3, backgroundColor: C.ink, transformOrigin: 'left', transform: `scaleX(${b})`}} />
      <div style={{opacity: b, fontSize: 33, color: C.muted}}>问题不只在语气。它选错了回应动作。</div>
      <Footer index="02 / 07" />
    </AbsoluteFill>
  );
};

const BetterResponse: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = pop(f, fps, 4);
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.ink, color: C.white}}>
      <Kicker color={C.yellow}>人味 Agent</Kicker>
      <div style={{marginTop: 200, fontSize: 55, color: '#B8B5AE'}}>用户说：不要分析，也不要建议。</div>
      <div style={{marginTop: 100, fontSize: 102, lineHeight: 1.15, fontWeight: 900, opacity: a, transform: `translateY(${(1 - a) * 60}px)`}}>
        听到了。
        <br />今天确实很难受。
      </div>
      <div style={{marginTop: 100, fontSize: 32, color: '#B8B5AE'}}>接住就够了，不多做一步。</div>
      <Footer index="03 / 07" />
    </AbsoluteFill>
  );
};

const Chip: React.FC<{label: string; value: string; delay: number}> = ({label, value, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = pop(f, fps, delay);
  return (
    <div style={{opacity: a, transform: `translateY(${(1 - a) * 36}px)`, borderTop: `2px solid ${C.ink}`, padding: '30px 0 34px', display: 'grid', gridTemplateColumns: '260px 1fr', fontSize: 36}}>
      <span style={{color: C.muted}}>{label}</span><strong>{value}</strong>
    </div>
  );
};

const DynamicLayer: React.FC = () => (
  <AbsoluteFill style={{...stage, backgroundColor: C.paper}}>
    <Kicker>核心创新 / Dynamic Human Layer</Kicker>
    <div style={{fontSize: 72, lineHeight: 1.15, fontWeight: 900, marginBottom: 70}}>先判断这一刻需要什么。</div>
    <Chip label="场景" value="聊天 / 写作 / coding / research" delay={6} />
    <Chip label="边界" value="回答 / 接住 / 追问 / 质疑 / 留白" delay={16} />
    <Chip label="力度" value="直接程度 / 温度 / 信息密度 / 介入程度" delay={26} />
    <div style={{marginTop: 45, padding: '28px 34px', backgroundColor: C.cyan, color: C.white, fontSize: 35, fontWeight: 800}}>再决定怎么说。</div>
    <Footer index="04 / 07" />
  </AbsoluteFill>
);

const Reliability: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const x = pop(f, fps, 15);
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.white}}>
      <Kicker>coding + research</Kicker>
      <div style={{fontSize: 70, lineHeight: 1.16, fontWeight: 900}}>没看代码，<span style={{color: C.red}}>不猜唯一根因。</span></div>
      <div style={{fontSize: 70, lineHeight: 1.16, fontWeight: 900, marginTop: 44}}>没核来源，<span style={{color: C.cyan}}>不冒充最新事实。</span></div>
      <div style={{marginTop: 105, display: 'flex', gap: 18, flexWrap: 'wrap', opacity: x}}>
        {['已确认', '合理推断', '未知项', '对口来源'].map((t, i) => <span key={t} style={{padding: '18px 26px', border: `2px solid ${i === 3 ? C.cyan : C.ink}`, fontSize: 30, fontWeight: 800}}>{t}</span>)}
      </div>
      <div style={{marginTop: 70, fontSize: 31, color: C.muted, lineHeight: 1.55}}>它不能消灭幻觉，但会堵住一部分“证据不够却说得很满”的路径。</div>
      <Footer index="05 / 07" />
    </AbsoluteFill>
  );
};

const ProjectWork: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.yellow}}>
      <Kicker color={C.ink}>做项目也要有因果链</Kicker>
      <div style={{fontSize: 72, lineHeight: 1.12, fontWeight: 900}}>第一性原理拆解，<br />对抗性审查收尾。</div>
      <div style={{marginTop: 86, display: 'flex', flexDirection: 'column', gap: 22}}>
        {['输入 → 状态 → 依赖 → 输出 → 不变量', '什么证据能推翻当前判断？', '原问题、回归和邻近边界真的通过了吗？'].map((t, i) => {
          const a = pop(f, fps, 10 + i * 14);
          return <div key={t} style={{opacity: a, transform: `translateX(${(1 - a) * 50}px)`, backgroundColor: i === 1 ? C.ink : C.white, color: i === 1 ? C.white : C.ink, padding: '30px 32px', fontSize: 32, lineHeight: 1.4, fontWeight: 700}}>{t}</div>;
        })}
      </div>
      <Footer index="06 / 07" />
    </AbsoluteFill>
  );
};

const CTA: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = pop(f, fps);
  return (
    <AbsoluteFill style={{...stage, backgroundColor: C.red, color: C.white}}>
      <div style={{fontSize: 29, fontWeight: 800}}>Codex · Claude Code · Gemini · Kimi · ChatGPT adapter</div>
      <div style={{marginTop: 250, fontSize: 126, lineHeight: 1.0, fontWeight: 900, opacity: a, transform: `scale(${0.92 + a * 0.08})`}}>人味<br />Agent</div>
      <div style={{marginTop: 70, fontSize: 41, lineHeight: 1.5, fontWeight: 600}}>少一点表演。<br />多一点判断和证据。</div>
      <div style={{position: 'absolute', left: 78, right: 78, bottom: 160, padding: '28px 30px', backgroundColor: C.white, color: C.ink, fontSize: 31, fontWeight: 800}}>github.com/FMStupid173/human-agent</div>
      <Footer index="OPEN SOURCE / PREVIEW" />
    </AbsoluteFill>
  );
};

const Transition: React.FC<{at: number}> = ({at}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at - 8, at, at + 8], [0, 1, 0], {easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: C.ink, transform: `translateX(${(1 - p) * 1080}px)`, zIndex: 20}} />;
};

export const HumanAgentPromo: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: C.paper}}>
    <Sequence from={0} durationInFrames={90}><Hook /></Sequence>
    <Sequence from={90} durationInFrames={110}><Pain /></Sequence>
    <Sequence from={200} durationInFrames={110}><BetterResponse /></Sequence>
    <Sequence from={310} durationInFrames={155}><DynamicLayer /></Sequence>
    <Sequence from={465} durationInFrames={150}><Reliability /></Sequence>
    <Sequence from={615} durationInFrames={165}><ProjectWork /></Sequence>
    <Sequence from={780} durationInFrames={120}><CTA /></Sequence>
    {[90, 200, 310, 465, 615, 780].map((at) => <Transition key={at} at={at} />)}
  </AbsoluteFill>
);
