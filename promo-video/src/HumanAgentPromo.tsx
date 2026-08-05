import React from 'react';
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const fontFamily = 'Microsoft YaHei, PingFang SC, Noto Sans SC, sans-serif';

const C = {
  ink: '#0C0C0C',
  paper: '#F4F0E6',
  white: '#FFFFFF',
  red: '#FF4B36',
  cyan: '#00A7A0',
  lime: '#C9FF35',
  yellow: '#FFD447',
  blue: '#3478F6',
  gray: '#716F68',
  line: '#B9B5AA',
};

const FPS = 30;
const CUTS = [86, 226, 287, 481, 610, 725, 816];
const hardShadow = '10px 10px 0 rgba(12,12,12,.16)';
const lightShadow = '10px 10px 0 rgba(201,255,53,.13)';

const rise = (frame: number, delay = 0, stiffness = 190) =>
  spring({frame: frame - delay, fps: FPS, config: {damping: 18, stiffness}});

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

const Label: React.FC<{children: React.ReactNode; dark?: boolean}> = ({children, dark}) => (
  <div style={{fontSize: 26, fontWeight: 900, color: dark ? C.lime : C.red, marginBottom: 18}}>{children}</div>
);

const GridBackground: React.FC<{dark?: boolean}> = ({dark}) => (
  <AbsoluteFill
    style={{
      backgroundColor: dark ? C.ink : C.paper,
      backgroundImage: dark
        ? 'linear-gradient(rgba(255,255,255,.055) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.055) 1px, transparent 1px)'
        : 'linear-gradient(rgba(12,12,12,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(12,12,12,.07) 1px, transparent 1px)',
      backgroundSize: '72px 72px',
    }}
  />
);

const FrameChrome: React.FC = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, 899], [0, 100], clamp);
  const inverse = (frame >= 226 && frame < 287) || (frame >= 481 && frame < 610) || frame >= 816;
  const chromeColor = inverse ? 'rgba(255,255,255,.72)' : C.gray;
  return (
    <>
      <div style={{position: 'absolute', top: 0, left: 0, width: `${width}%`, height: 16, backgroundColor: C.red, zIndex: 60}} />
      <div style={{position: 'absolute', left: 56, right: 56, bottom: 42, display: 'flex', justifyContent: 'space-between', fontFamily, fontSize: 26, fontWeight: 900, color: chromeColor, zIndex: 60}}>
        <span>人味 Agent / HUMAN-AGENT</span>
        <span>{String(Math.min(30, Math.floor(frame / 30) + 1)).padStart(2, '0')} / 30 SEC</span>
      </div>
    </>
  );
};

const captions = [
  [3, 87, 'AI 回答得很快，却经常没回到点上。'],
  [86, 145, '你只想被听见，它开始说教；'],
  [145, 226, '代码和资料没看，它已经给出结论。'],
  [226, 287, '所以我做了人味 Agent。'],
  [287, 360, '动态人感层先判断场景、边界和介入程度，'],
  [360, 481, '再选择回答、追问、质疑，还是留白。'],
  [481, 610, '做项目时，它从输入、状态、依赖、输出和不变量拆问题；'],
  [610, 725, '给结论前，再找能推翻自己的证据，跑完验证才收尾。'],
  [725, 816, '它会把已确认、合理推断和未知分开，'],
  [816, 899, '让回答少一点套话，多一点判断和证据。'],
] as const;

const Caption: React.FC = () => {
  const frame = useCurrentFrame();
  const active = captions.find(([start, end]) => frame >= start && frame < end);
  if (!active) return null;
  const [start, end, text] = active;
  const enter = interpolate(frame, [start, start + 5], [0, 1], clamp);
  const leave = interpolate(frame, [end - 5, end], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: 56, right: 56, bottom: 98, minHeight: 112, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px 32px', boxSizing: 'border-box', backgroundColor: C.ink, color: C.white, border: `4px solid ${C.white}`, fontFamily, fontSize: 38, lineHeight: 1.35, fontWeight: 800, textAlign: 'center', opacity: Math.min(enter, leave), zIndex: 55}}>
      {text}
    </div>
  );
};

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const a = rise(f);
  const b = rise(f, 9);
  const c = rise(f, 21);
  const ticker = interpolate(f, [0, 86], [0, -520], clamp);
  return (
    <AbsoluteFill style={{fontFamily, overflow: 'hidden'}}>
      <GridBackground />
      <div style={{position: 'absolute', left: 56, top: 74, right: 56}}>
        <Label>01 / 痛点不是“说得不漂亮”</Label>
        <div style={{fontSize: 104, lineHeight: 1.03, fontWeight: 900, transform: `translateY(${(1 - a) * 70}px)`, opacity: a}}>AI 回答很快</div>
        <div style={{marginTop: 14, display: 'flex', alignItems: 'center', gap: 22, transform: `translateX(${(1 - b) * 90}px)`, opacity: b}}>
          <span style={{padding: '10px 22px', backgroundColor: C.red, color: C.white, fontSize: 50, fontWeight: 900}}>但是</span>
          <span style={{fontSize: 92, fontWeight: 900}}>没回到点上</span>
        </div>
        <div style={{marginTop: 46, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, opacity: c}}>
          {[
            ['你想被听见', '它开始说教'],
            ['你只要轻改', '它重写全文'],
            ['证据还没看', '它已经确定'],
          ].map(([top, bottom], index) => (
            <div key={top} style={{border: `3px solid ${C.ink}`, backgroundColor: index === 1 ? C.yellow : C.white, padding: '24px 20px', minHeight: 172, boxShadow: hardShadow}}>
              <div style={{fontSize: 26, color: C.gray, fontWeight: 700}}>{top}</div>
              <div style={{fontSize: 35, lineHeight: 1.18, fontWeight: 900, marginTop: 16}}>{bottom}</div>
            </div>
          ))}
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, top: 1000, display: 'flex', gap: 18, transform: `translateX(${ticker}px) rotate(-3deg)`, whiteSpace: 'nowrap'}}>
        {['套话', '过度解释', '客服腔', '虚假确定', '语义漂移', '错误介入', '套话', '过度解释'].map((word, i) => (
          <span key={`${word}-${i}`} style={{padding: '18px 30px', backgroundColor: i % 2 ? C.cyan : C.ink, color: C.white, fontSize: 38, fontWeight: 900}}>{word}</span>
        ))}
      </div>
      <div style={{position: 'absolute', left: 56, right: 56, top: 1220, borderTop: `5px solid ${C.ink}`, paddingTop: 30, fontSize: 34, lineHeight: 1.4, fontWeight: 700}}>真正的问题：AI 在错误的时刻，选择了错误的回应动作。</div>
      <div style={{position: 'absolute', left: 56, right: 56, top: 1405, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', border: `4px solid ${C.ink}`, backgroundColor: C.white}}>
        {[
          ['01', '先判断场景'],
          ['02', '再选择动作'],
          ['03', '最后组织语言'],
        ].map(([no, text], i) => (
          <div key={no} style={{padding: '24px 18px', minHeight: 135, borderLeft: i ? `3px solid ${C.ink}` : 'none', backgroundColor: i === 1 ? C.lime : C.white}}>
            <div style={{fontSize: 26, color: C.gray, fontWeight: 900}}>{no}</div>
            <div style={{fontSize: 28, lineHeight: 1.25, fontWeight: 900, marginTop: 14}}>{text}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Bubble: React.FC<{side: 'user' | 'ai'; children: React.ReactNode; delay: number; bad?: boolean}> = ({side, children, delay, bad}) => {
  const f = useCurrentFrame();
  const a = rise(f, delay);
  return (
    <div style={{alignSelf: side === 'user' ? 'flex-end' : 'flex-start', maxWidth: '88%', padding: '20px 24px', backgroundColor: side === 'user' ? C.blue : C.white, color: side === 'user' ? C.white : C.ink, border: `3px solid ${bad ? C.red : C.ink}`, boxShadow: '7px 7px 0 rgba(12,12,12,.14)', fontSize: 30, lineHeight: 1.35, fontWeight: 700, opacity: a, transform: `translateY(${(1 - a) * 28}px)`}}>{children}</div>
  );
};

const PainCases: React.FC = () => {
  const f = useCurrentFrame();
  const stamp = rise(f, 32, 230);
  return (
    <AbsoluteFill style={{fontFamily, backgroundColor: C.white, padding: '68px 56px 250px', boxSizing: 'border-box', overflow: 'hidden'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: 28}}>
        <div><Label>02 / 两个高频失败现场</Label><div style={{fontSize: 58, fontWeight: 900}}>语气没错，动作错了。</div></div>
        <div style={{fontSize: 26, fontWeight: 900, backgroundColor: C.lime, padding: '12px 18px'}}>WRONG ACT × 2</div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18, height: 1280}}>
        <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.paper, padding: 22, display: 'flex', flexDirection: 'column', gap: 18, position: 'relative'}}>
          <div style={{fontSize: 28, fontWeight: 900, color: C.gray}}>CHAT / 情绪边界</div>
          <Bubble side="user" delay={3}>我今天很难受。<br />不要建议。</Bubble>
          <Bubble side="ai" delay={13} bad>我完全理解。你可以深呼吸、喝水、列一个清单……</Bubble>
          <div style={{marginTop: 'auto', backgroundColor: C.red, color: C.white, padding: '18px 20px', fontSize: 28, fontWeight: 900}}>用户要“接住”<br />AI 却选择“解决”</div>
        </div>
        <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.ink, color: C.white, padding: 22, display: 'flex', flexDirection: 'column', gap: 18, position: 'relative'}}>
          <div style={{fontSize: 28, fontWeight: 900, color: C.lime}}>DEBUG / 证据边界</div>
          <div style={{fontFamily: 'Consolas, monospace', backgroundColor: '#181818', border: '2px solid #525252', padding: 20, fontSize: 28, lineHeight: 1.5}}>
            <span style={{color: C.red}}>TypeError:</span><br />undefined<br /><br /><span style={{color: C.gray}}>// no stack<br />// no code<br />// no repro</span>
          </div>
          <div style={{backgroundColor: C.white, color: C.ink, padding: '22px 20px', fontSize: 28, lineHeight: 1.35, fontWeight: 800}}>“唯一根因是对象未初始化。”</div>
          <div style={{marginTop: 'auto', backgroundColor: C.yellow, color: C.ink, padding: '18px 20px', fontSize: 28, fontWeight: 900}}>证据不足<br />结论却写满</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 340, top: 680, transform: `rotate(-10deg) scale(${stamp})`, border: `10px solid ${C.red}`, color: C.red, padding: '18px 30px', fontSize: 58, fontWeight: 900, backgroundColor: 'rgba(255,255,255,.9)'}}>没回到点上</div>
    </AbsoluteFill>
  );
};

const BrandReveal: React.FC = () => {
  const f = useCurrentFrame();
  const a = rise(f, 0, 250);
  return (
    <AbsoluteFill style={{fontFamily, backgroundColor: C.ink, color: C.white, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 56, border: `5px solid ${C.lime}`}} />
      <div style={{position: 'absolute', left: 82, top: 150, fontSize: 34, color: C.lime, fontWeight: 900}}>OPEN-SOURCE RESPONSE POLICY</div>
      <div style={{position: 'absolute', left: 72, top: 360, fontSize: 146, lineHeight: 0.95, fontWeight: 900, opacity: a, transform: `scale(${0.88 + a * 0.12})`}}>人味<br />Agent</div>
      <div style={{position: 'absolute', left: 76, top: 760, fontSize: 40, lineHeight: 1.45, fontWeight: 700}}>先决定该做什么。<br /><span style={{color: C.lime}}>再决定该怎么说。</span></div>
      <div style={{position: 'absolute', left: 78, right: 78, top: 1060, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14}}>
        {[
          ['01', '动态人感', C.lime],
          ['02', '语义保真', C.white],
          ['03', '证据校准', C.red],
          ['04', '第一性原理', C.white],
          ['05', '对抗收尾', C.cyan],
          ['06', '跨模型适配', C.lime],
        ].map(([no, word, bg], i) => (
          <div key={word} style={{backgroundColor: bg, color: bg === C.red || bg === C.cyan ? C.white : C.ink, padding: '20px 22px', fontSize: 28, fontWeight: 900, display: 'flex', justifyContent: 'space-between', boxShadow: i % 2 ? 'none' : lightShadow, opacity: rise(f, 10 + i * 4)}}>
            <span>{word}</span><span style={{opacity: .55}}>{no}</span>
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 78, right: 78, top: 1435, borderTop: `4px solid ${C.lime}`, borderBottom: `4px solid ${C.lime}`, padding: '26px 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <span style={{fontSize: 28, color: '#A9A9A9', fontWeight: 900}}>不是固定人设</span>
        <span style={{fontSize: 52, color: C.white, fontWeight: 900}}>逐轮选择回应动作</span>
      </div>
    </AbsoluteFill>
  );
};

const RouterRow: React.FC<{label: string; value: string; delay: number; color: string}> = ({label, value, delay, color}) => {
  const f = useCurrentFrame();
  const a = rise(f, delay);
  return (
    <div style={{display: 'grid', gridTemplateColumns: '150px 1fr', alignItems: 'center', gap: 18, opacity: a, transform: `translateX(${(1 - a) * -40}px)`}}>
      <div style={{fontSize: 26, color: C.gray, fontWeight: 800}}>{label}</div>
      <div style={{padding: '15px 20px', backgroundColor: color, color: color === C.yellow || color === C.lime ? C.ink : C.white, fontSize: 30, fontWeight: 900}}>{value}</div>
    </div>
  );
};

const DynamicRouter: React.FC = () => {
  const f = useCurrentFrame();
  const selected = rise(f, 72, 240);
  const arrow = interpolate(f, [18, 80], [0, 100], clamp);
  return (
    <AbsoluteFill style={{fontFamily, padding: '66px 56px 250px', boxSizing: 'border-box', overflow: 'hidden'}}>
      <GridBackground />
      <div style={{position: 'relative'}}>
        <Label>03 / 核心创新：动态人感层</Label>
        <div style={{fontSize: 58, lineHeight: 1.12, fontWeight: 900}}>把当前对话，先编译成一份“回应契约”。</div>
        <div style={{marginTop: 36, display: 'grid', gridTemplateColumns: '300px 1fr', gap: 22}}>
          <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.white, padding: 22, minHeight: 600, boxShadow: hardShadow}}>
            <div style={{fontSize: 28, color: C.gray, fontWeight: 900}}>INPUT</div>
            <div style={{marginTop: 42, fontSize: 36, lineHeight: 1.35, fontWeight: 900}}>“我今天很难受。”</div>
            <div style={{marginTop: 24, backgroundColor: C.red, color: C.white, padding: '16px 18px', fontSize: 27, lineHeight: 1.35, fontWeight: 900}}>不要分析<br />不要建议</div>
            <div style={{marginTop: 44, fontSize: 28, lineHeight: 1.4, color: C.gray}}>当前消息优先<br />覆盖默认友好模板</div>
          </div>
          <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.paper, padding: 22, minHeight: 600, boxShadow: hardShadow}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}><div style={{fontSize: 27, color: C.gray, fontWeight: 900}}>DYNAMIC HUMAN LAYER</div><div style={{width: 18, height: 18, backgroundColor: C.cyan, transform: `scale(${0.7 + selected * 0.5})`}} /></div>
            <div style={{marginTop: 30, display: 'flex', flexDirection: 'column', gap: 16}}>
              <RouterRow label="场景" value="情绪 / personal" delay={8} color={C.cyan} />
              <RouterRow label="边界" value="不要建议" delay={18} color={C.red} />
              <RouterRow label="介入程度" value="低" delay={28} color={C.yellow} />
              <RouterRow label="证据风险" value="低" delay={38} color={C.blue} />
            </div>
            <div style={{marginTop: 34, height: 10, backgroundColor: '#D6D1C5'}}><div style={{width: `${arrow}%`, height: '100%', backgroundColor: C.ink}} /></div>
          </div>
        </div>
        <div style={{marginTop: 20, display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 10}}>
          {['回答', '接住', '追问', '质疑', '留白'].map((word, i) => {
            const active = i === 1;
            return <div key={word} style={{padding: '20px 8px', textAlign: 'center', border: `3px solid ${C.ink}`, backgroundColor: active ? C.lime : C.white, fontSize: 29, fontWeight: 900, transform: active ? `scale(${0.94 + selected * 0.08})` : 'none'}}>{active ? '✓ ' : ''}{word}</div>;
          })}
        </div>
        <div style={{marginTop: 20, display: 'grid', gridTemplateColumns: '180px 1fr', border: `4px solid ${C.ink}`, backgroundColor: C.ink, color: C.white}}>
          <div style={{padding: 20, color: C.lime, fontSize: 27, fontWeight: 900}}>OUTPUT</div>
          <div style={{padding: 20, borderLeft: `2px solid ${C.gray}`, fontSize: 31, fontWeight: 800}}>听到了。今天确实很难受。</div>
        </div>
        <div style={{marginTop: 18, display: 'grid', gridTemplateColumns: '1fr 44px 1fr 44px 1fr', alignItems: 'stretch'}}>
          {[
            ['读边界', '不要建议'],
            ['选动作', '接住'],
            ['控剂量', '一句就够'],
          ].map(([title, value], i) => (
            <React.Fragment key={title}>
              {i > 0 && <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34, fontWeight: 900}}>→</div>}
              <div style={{border: `3px solid ${C.ink}`, backgroundColor: i === 1 ? C.lime : C.white, padding: '22px 16px', minHeight: 160}}>
                <div style={{fontSize: 25, color: C.gray, fontWeight: 900}}>{title}</div>
                <div style={{fontSize: 27, lineHeight: 1.25, fontWeight: 900, marginTop: 16}}>{value}</div>
              </div>
            </React.Fragment>
          ))}
        </div>
        <div style={{marginTop: 18, border: `4px solid ${C.ink}`, backgroundColor: C.ink, color: C.white, padding: '22px 24px'}}>
          <div style={{fontSize: 26, color: C.lime, fontWeight: 900}}>DEFAULT POLICY OVERRIDDEN</div>
          <div style={{marginTop: 15, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 18, fontSize: 28, fontWeight: 900}}>
            <span style={{color: C.gray, textDecoration: 'line-through'}}>解释 + 建议 + 清单</span>
            <span style={{color: C.red}}>→</span>
            <span>短回应 + 不介入</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const FirstPrinciples: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{fontFamily, backgroundColor: C.ink, color: C.white, padding: '66px 56px 250px', boxSizing: 'border-box', overflow: 'hidden'}}>
      <Label dark>04 / 做项目：先建立因果链</Label>
      <div style={{fontSize: 60, fontWeight: 900}}>第一性原理，不等于推倒重来。</div>
      <div style={{marginTop: 22, fontSize: 31, color: '#BDBDBD'}}>从系统真正拥有的输入、状态和约束开始。</div>
      <div style={{marginTop: 54, display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 10}}>
        {['输入', '状态', '依赖', '输出', '不变量'].map((word, i) => {
          const a = rise(f, 8 + i * 8);
          return <div key={word} style={{height: 210, backgroundColor: i === 4 ? C.lime : i === 2 ? C.red : '#202020', color: i === 4 ? C.ink : C.white, border: '2px solid #5A5A5A', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '20px 14px', boxSizing: 'border-box', opacity: a, transform: `translateY(${(1 - a) * 50}px)`}}><span style={{fontSize: 25, color: i === 4 ? C.ink : C.gray}}>0{i + 1}</span><strong style={{fontSize: 30}}>{word}</strong></div>;
        })}
      </div>
      <div style={{marginTop: 34, border: '3px solid #565656', backgroundColor: '#151515', padding: 24, fontFamily: 'Consolas, monospace', fontSize: 27, lineHeight: 1.6}}>
        <span style={{color: C.cyan}}>observed:</span> 页面偶尔显示旧数据<br />
        <span style={{color: C.yellow}}>unknown:</span> 前端 / 接口 / 数据库 / 缓存<br />
        <span style={{color: C.lime}}>next:</span> 找一条能切开边界的证据
      </div>
      <div style={{marginTop: 32, display: 'flex', gap: 14}}>
        {['先看代码', '再提假设', '用证据区分'].map((word, i) => <div key={word} style={{flex: 1, backgroundColor: i === 2 ? C.blue : C.white, color: i === 2 ? C.white : C.ink, padding: '20px 12px', fontSize: 26, textAlign: 'center', fontWeight: 900}}>{word}</div>)}
      </div>
      <div style={{marginTop: 38, border: '3px solid #565656', backgroundColor: '#161616', padding: 24, boxShadow: lightShadow}}>
        <div style={{fontSize: 27, color: C.gray, fontWeight: 900, marginBottom: 20}}>EVIDENCE PATH / 用一条证据切开边界</div>
        {[
          ['01', '网络响应', '接口是否已经返回新数据', C.cyan],
          ['02', '页面状态', '旧值是否仍留在前端状态里', C.yellow],
          ['03', '最小复现', '固定输入后错误能否稳定出现', C.lime],
        ].map(([no, title, desc, color]) => (
          <div key={no} style={{display: 'grid', gridTemplateColumns: '58px 190px 1fr', alignItems: 'center', gap: 14, borderTop: '2px solid #3E3E3E', padding: '18px 0'}}>
            <span style={{color, fontSize: 26, fontWeight: 900}}>{no}</span>
            <strong style={{fontSize: 26}}>{title}</strong>
            <span style={{fontSize: 27, color: '#C8C8C8'}}>{desc}</span>
          </div>
        ))}
      </div>
      <div style={{marginTop: 28, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12}}>
        {[
          ['OBSERVE', '先看实际状态', C.cyan],
          ['SPLIT', '切开因果边界', C.yellow],
          ['VERIFY', '运行最小验证', C.lime],
        ].map(([title, desc, color]) => (
          <div key={title} style={{border: `3px solid ${color}`, minHeight: 160, padding: '20px 16px'}}>
            <div style={{fontSize: 27, color, fontWeight: 900}}>{title}</div>
            <div style={{fontSize: 27, lineHeight: 1.3, marginTop: 18}}>{desc}</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const AdversarialFinish: React.FC = () => {
  const f = useCurrentFrame();
  const strike = rise(f, 24, 240);
  const pass = rise(f, 60, 220);
  return (
    <AbsoluteFill style={{fontFamily, backgroundColor: C.yellow, padding: '66px 56px 250px', boxSizing: 'border-box', overflow: 'hidden'}}>
      <Label>05 / 对抗性审查：专门找自己哪里错</Label>
      <div style={{fontSize: 60, lineHeight: 1.12, fontWeight: 900}}>结论写完，不等于任务完成。</div>
      <div style={{marginTop: 42, display: 'grid', gridTemplateColumns: '1fr 90px 1fr', gap: 14, alignItems: 'stretch'}}>
        <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.white, padding: 24, boxShadow: hardShadow}}>
          <div style={{fontSize: 27, color: C.gray, fontWeight: 900}}>CURRENT HYPOTHESIS</div>
          <div style={{fontSize: 35, lineHeight: 1.3, fontWeight: 900, marginTop: 30}}>“旧数据一定是缓存。”</div>
          <div style={{height: 8, backgroundColor: C.red, marginTop: 42, transformOrigin: 'left', transform: `scaleX(${strike})`}} />
        </div>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 58, fontWeight: 900}}>VS</div>
        <div style={{border: `4px solid ${C.ink}`, backgroundColor: C.ink, color: C.white, padding: 24, boxShadow: hardShadow}}>
          <div style={{fontSize: 27, color: C.lime, fontWeight: 900}}>FALSIFYING EVIDENCE</div>
          <div style={{fontSize: 31, lineHeight: 1.35, fontWeight: 800, marginTop: 30}}>接口返回新数据，页面仍显示旧值。</div>
          <div style={{fontSize: 28, color: C.yellow, marginTop: 28}}>→ 先查前端状态与竞态</div>
        </div>
      </div>
      <div style={{marginTop: 34, backgroundColor: C.white, border: `4px solid ${C.ink}`, padding: 24}}>
        <div style={{fontSize: 27, fontWeight: 900, marginBottom: 18}}>完成前的三道门</div>
        {['原问题真的消失', '回归测试覆盖原因', '邻近边界没有被破坏'].map((word, i) => <div key={word} style={{display: 'flex', gap: 18, alignItems: 'center', borderTop: `2px solid ${C.line}`, padding: '18px 0', fontSize: 29, fontWeight: 800, opacity: rise(f, 38 + i * 10)}}><span style={{width: 38, height: 38, backgroundColor: C.lime, border: `3px solid ${C.ink}`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center'}}>✓</span>{word}</div>)}
      </div>
      <div style={{marginTop: 30, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12}}>
        {[
          ['反例', '什么证据会推翻我？'],
          ['回归', '原问题是否真的消失？'],
          ['边界', '相邻功能有没有被破坏？'],
        ].map(([title, desc], i) => (
          <div key={title} style={{border: `4px solid ${C.ink}`, backgroundColor: i === 1 ? C.ink : C.white, color: i === 1 ? C.white : C.ink, minHeight: 190, padding: '22px 16px'}}>
            <div style={{fontSize: 30, fontWeight: 900, color: i === 1 ? C.lime : C.red}}>{title}</div>
            <div style={{fontSize: 26, lineHeight: 1.35, fontWeight: 800, marginTop: 18}}>{desc}</div>
          </div>
        ))}
      </div>
      <div style={{marginTop: 26, border: `4px solid ${C.ink}`, backgroundColor: C.white, padding: '18px 20px', display: 'grid', gridTemplateColumns: '140px 1fr 180px', alignItems: 'center', gap: 18}}>
        <span style={{fontSize: 26, color: C.gray, fontWeight: 900}}>DONE GATE</span>
        <span style={{fontSize: 27, fontWeight: 900}}>修复 + 测试 + 边界检查</span>
        <span style={{fontSize: 28, color: C.cyan, fontWeight: 900}}>全部通过</span>
      </div>
      <div style={{position: 'absolute', right: 55, top: 1450, transform: `rotate(-6deg) scale(${pass})`, backgroundColor: C.red, color: C.white, padding: '18px 28px', fontSize: 48, fontWeight: 900}}>验证后才收尾</div>
    </AbsoluteFill>
  );
};

const Reliability: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{fontFamily, padding: '66px 56px 250px', boxSizing: 'border-box', backgroundColor: C.white, overflow: 'hidden'}}>
      <Label>06 / 可靠性机制</Label>
      <div style={{fontSize: 68, lineHeight: 1.08, fontWeight: 900}}>把确定程度<br />写在答案里。</div>
      <div style={{marginTop: 34, backgroundColor: C.cyan, color: C.white, display: 'inline-block', padding: '14px 20px', fontSize: 34, fontWeight: 900}}>事实、推断、未知，一眼分开</div>
      <div style={{marginTop: 42, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14}}>
        {[
          ['已确认', '有文件、工具或一手来源支持', C.ink, C.white],
          ['合理推断', '标明推断，不装成事实', C.cyan, C.white],
          ['未知项', '缺什么证据，就说缺什么', C.yellow, C.ink],
          ['对口来源', 'API 查官方，论文查原文', C.lime, C.ink],
        ].map(([title, desc, bg, color], i) => <div key={title} style={{backgroundColor: bg, color, minHeight: 190, padding: 20, opacity: rise(f, i * 8), transform: `translateY(${(1 - rise(f, i * 8)) * 30}px)`}}><div style={{fontSize: 34, fontWeight: 900}}>{title}</div><div style={{fontSize: 27, lineHeight: 1.35, marginTop: 18}}>{desc}</div></div>)}
      </div>
      <div style={{position: 'absolute', left: 56, right: 56, top: 890, bottom: 270, border: `4px solid ${C.ink}`, display: 'grid', gridTemplateRows: 'repeat(4,1fr)', boxShadow: hardShadow}}>
        {[
          ['实时事实', '价格、版本、法律', '必须联网核验'],
          ['代码判断', '代码、日志、复现', '先看证据再定位'],
          ['资料检索', 'API、论文、标准', '优先官方与原文'],
          ['证据不足', '未知就是未知', '不拿语气冒充确定'],
        ].map(([kind, scope, action], i) => (
          <div key={kind} style={{display: 'grid', gridTemplateColumns: '160px 1fr 250px', alignItems: 'center', gap: 16, padding: '0 22px', borderTop: i ? `3px solid ${C.ink}` : 'none', backgroundColor: i % 2 ? C.paper : C.white}}>
            <strong style={{fontSize: 27}}>{kind}</strong>
            <span style={{fontSize: 27, color: C.gray}}>{scope}</span>
            <span style={{fontSize: 27, fontWeight: 900, color: i === 3 ? C.red : C.cyan}}>{action}</span>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const CTA: React.FC = () => {
  const f = useCurrentFrame();
  const a = rise(f, 0, 240);
  return (
    <AbsoluteFill style={{fontFamily, backgroundColor: C.red, color: C.white, padding: '66px 56px 250px', boxSizing: 'border-box', overflow: 'hidden'}}>
      <div style={{fontSize: 27, fontWeight: 900}}>OPEN SOURCE / v0.2 PREVIEW</div>
      <div style={{marginTop: 70, fontSize: 122, lineHeight: 0.94, fontWeight: 900, transform: `translateX(${(1 - a) * -80}px)`, opacity: a}}>少一点<br />套话。</div>
      <div style={{marginTop: 18, fontSize: 104, lineHeight: 1.0, fontWeight: 900, color: C.lime, transform: `translateX(${(1 - a) * 80}px)`, opacity: a}}>多一点判断<br />和证据。</div>
      <div style={{marginTop: 54, display: 'flex', flexWrap: 'wrap', gap: 10}}>
        {['Codex', 'Claude Code', 'Gemini', 'Kimi', 'ChatGPT adapter'].map((word, i) => <span key={word} style={{backgroundColor: i === 4 ? C.ink : C.white, color: i === 4 ? C.white : C.ink, padding: '12px 18px', fontSize: 27, fontWeight: 900}}>{word}</span>)}
      </div>
      <div style={{position: 'absolute', left: 56, right: 56, top: 865, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12}}>
        {[
          ['判断场景', '动态人感层'],
          ['检查证据', '减少可避免幻觉'],
          ['推翻自己', '对抗性收尾'],
        ].map(([title, desc], i) => (
          <div key={title} style={{minHeight: 220, border: `4px solid ${C.ink}`, backgroundColor: i === 1 ? C.lime : C.white, color: C.ink, padding: '24px 18px', boxShadow: hardShadow}}>
            <div style={{fontSize: 56, fontWeight: 900, lineHeight: 1}}>0{i + 1}</div>
            <div style={{fontSize: 28, fontWeight: 900, marginTop: 24}}>{title}</div>
            <div style={{fontSize: 25, fontWeight: 800, marginTop: 12}}>{desc}</div>
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 56, right: 56, top: 1260, backgroundColor: C.white, color: C.ink, border: `5px solid ${C.ink}`, padding: '26px 24px', boxShadow: hardShadow}}>
        <div style={{fontSize: 26, color: C.gray, fontWeight: 900}}>人味 Agent</div>
        <div style={{fontSize: 30, fontWeight: 900, marginTop: 12}}>github.com/FMStupid173/human-agent</div>
      </div>
    </AbsoluteFill>
  );
};

const Wipe: React.FC<{color: string}> = ({color}) => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 3, 6], [-110, 0, 110], clamp);
  return <AbsoluteFill style={{backgroundColor: color, transform: `translateX(${x}%) skewX(-8deg)`, zIndex: 50}} />;
};

export const HumanAgentPromo: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: C.paper}}>
    <Audio src={staticFile('voiceover.mp3')} volume={1.55} />
    <Audio src={staticFile('soundbed.mp3')} volume={0.30} />

    <Sequence from={0} durationInFrames={86}><Hook /></Sequence>
    <Sequence from={86} durationInFrames={140}><PainCases /></Sequence>
    <Sequence from={226} durationInFrames={61}><BrandReveal /></Sequence>
    <Sequence from={287} durationInFrames={194}><DynamicRouter /></Sequence>
    <Sequence from={481} durationInFrames={129}><FirstPrinciples /></Sequence>
    <Sequence from={610} durationInFrames={115}><AdversarialFinish /></Sequence>
    <Sequence from={725} durationInFrames={91}><Reliability /></Sequence>
    <Sequence from={816} durationInFrames={84}><CTA /></Sequence>

    {CUTS.map((cut, index) => (
      <Sequence key={cut} from={cut - 3} durationInFrames={6}>
        <Wipe color={[C.red, C.lime, C.cyan, C.yellow, C.blue, C.red, C.lime][index]} />
      </Sequence>
    ))}
    <Caption />
    <FrameChrome />
  </AbsoluteFill>
);
