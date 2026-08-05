import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';

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

const shadow = '12px 12px 0 rgba(12,12,12,.18)';
const border = `5px solid ${C.ink}`;

const Grid: React.FC<{dark?: boolean}> = ({dark}) => (
  <AbsoluteFill style={{
    backgroundColor: dark ? C.ink : C.paper,
    backgroundImage: dark
      ? 'linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px)'
      : 'linear-gradient(rgba(12,12,12,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(12,12,12,.07) 1px, transparent 1px)',
    backgroundSize: '84px 84px',
  }} />
);

const Footer: React.FC<{index: number; dark?: boolean}> = ({index, dark}) => (
  <div style={{position: 'absolute', left: 76, right: 76, bottom: 54, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontFamily, color: dark ? 'rgba(255,255,255,.68)' : C.gray, fontSize: 28, fontWeight: 900}}>
    <span>人味 Agent / HUMAN-AGENT</span>
    <span>{String(index).padStart(2, '0')} / 07</span>
  </div>
);

const Eyebrow: React.FC<{children: React.ReactNode; dark?: boolean}> = ({children, dark}) => (
  <div style={{fontSize: 30, fontWeight: 900, color: dark ? C.lime : C.red, marginBottom: 26}}>{children}</div>
);

const Page: React.FC<{children: React.ReactNode; background?: string; dark?: boolean; index: number}> = ({children, background, dark, index}) => (
  <AbsoluteFill style={{fontFamily, backgroundColor: background ?? (dark ? C.ink : C.paper), color: dark ? C.white : C.ink, overflow: 'hidden'}}>
    {!background && <Grid dark={dark} />}
    <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 18, backgroundColor: C.red}} />
    <div style={{position: 'absolute', inset: '70px 76px 150px'}}>{children}</div>
    <Footer index={index} dark={dark} />
  </AbsoluteFill>
);

export const HumanAgentCover: React.FC = () => (
  <Page index={1}>
    <Eyebrow>OPEN-SOURCE SKILL / v0.2 PREVIEW</Eyebrow>
    <div style={{display: 'grid', gridTemplateColumns: '1.2fr .8fr', gap: 28, alignItems: 'start'}}>
      <div>
        <div style={{fontSize: 168, lineHeight: .87, fontWeight: 900, letterSpacing: 0}}>人味<br />Agent</div>
        <div style={{marginTop: 48, fontSize: 55, lineHeight: 1.15, fontWeight: 900}}>让 AI 先判断<br /><span style={{backgroundColor: C.red, color: C.white, padding: '4px 14px'}}>该怎么回应</span></div>
        <div style={{marginTop: 22, fontSize: 54, lineHeight: 1.15, fontWeight: 900}}>再决定<br /><span style={{backgroundColor: C.lime, padding: '4px 14px'}}>该怎么说</span></div>
      </div>
      <div style={{backgroundColor: C.ink, color: C.white, border, padding: '30px 26px', boxShadow: shadow}}>
        <div style={{fontSize: 28, color: C.lime, fontWeight: 900}}>DYNAMIC HUMAN LAYER</div>
        <div style={{marginTop: 32, display: 'grid', gap: 14}}>
          {[
            ['场景', '聊天 / 写作 / 项目'],
            ['边界', '要不要建议'],
            ['动作', '接住 / 追问 / 执行'],
            ['证据', '事实 / 推断 / 未知'],
          ].map(([label, value], i) => (
            <div key={label} style={{borderTop: `2px solid ${i ? '#444' : C.lime}`, paddingTop: 16}}>
              <div style={{fontSize: 23, color: '#9A9A9A', fontWeight: 900}}>{label}</div>
              <div style={{fontSize: 26, lineHeight: 1.35, fontWeight: 900, marginTop: 8}}>{value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, top: 820, borderTop: border, borderBottom: border, padding: '24px 28px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: C.white}}>
      <span style={{fontSize: 28, color: C.gray, fontWeight: 900}}>不是固定人设</span>
      <strong style={{fontSize: 38}}>逐轮选择回应动作</strong>
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, top: 980}}>
      <div style={{fontSize: 30, fontWeight: 900, marginBottom: 18}}>一套同时处理“人感”和“可靠性”的响应策略层</div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14}}>
        {[
          ['01', '动态回应选择', C.lime],
          ['02', '语义与写作保真', C.yellow],
          ['03', '证据校准', C.cyan],
          ['04', '第一性原理', C.white],
          ['05', '对抗性收尾', C.red],
          ['06', '跨模型适配', C.ink],
        ].map(([no, title, bg]) => (
          <div key={title} style={{minHeight: 120, padding: '20px 18px', backgroundColor: bg, color: bg === C.ink || bg === C.red || bg === C.cyan ? C.white : C.ink, border, boxSizing: 'border-box'}}>
            <div style={{fontSize: 23, opacity: .7, fontWeight: 900}}>{no}</div>
            <div style={{fontSize: 26, lineHeight: 1.25, fontWeight: 900, marginTop: 12}}>{title}</div>
          </div>
        ))}
      </div>
    </div>
  </Page>
);

const PainPage: React.FC = () => (
  <Page index={2} dark>
    <Eyebrow dark>为什么需要它</Eyebrow>
    <div style={{fontSize: 86, lineHeight: 1.02, fontWeight: 900}}>AI 答对了，<br /><span style={{color: C.lime}}>也可能没回到点上。</span></div>
    <div style={{marginTop: 70, display: 'grid', gap: 22}}>
      {[
        ['你只想被听见', '它开始分析、建议、列清单', C.red],
        ['你只想轻改一句', '它把你的声音全部换掉', C.yellow],
        ['资料和代码没看', '它已经给出唯一结论', C.cyan],
      ].map(([need, wrong, color], i) => (
        <div key={need} style={{display: 'grid', gridTemplateColumns: '92px 1fr', border: `4px solid ${color}`, backgroundColor: '#171717'}}>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: color, color: color === C.yellow ? C.ink : C.white, fontSize: 42, fontWeight: 900}}>0{i + 1}</div>
          <div style={{padding: '28px 30px'}}>
            <div style={{fontSize: 29, color: '#9A9A9A', fontWeight: 900}}>{need}</div>
            <div style={{fontSize: 39, lineHeight: 1.25, fontWeight: 900, marginTop: 12}}>{wrong}</div>
          </div>
        </div>
      ))}
    </div>
    <div style={{marginTop: 70, borderTop: `4px solid ${C.lime}`, borderBottom: `4px solid ${C.lime}`, padding: '28px 0', fontSize: 42, lineHeight: 1.3, fontWeight: 900}}>
      真正的问题：在错误的时刻，<span style={{color: C.lime}}>选择了错误的回应动作。</span>
    </div>
  </Page>
);

const DynamicPage: React.FC = () => (
  <Page index={3} background={C.cyan}>
    <Eyebrow dark>核心创新 / 动态人感层</Eyebrow>
    <div style={{fontSize: 88, lineHeight: 1.0, fontWeight: 900, color: C.white}}>先选回应动作。<br /><span style={{color: C.lime}}>再决定语气。</span></div>
    <div style={{marginTop: 68, display: 'grid', gridTemplateColumns: '1fr 110px 1fr', alignItems: 'stretch'}}>
      <div style={{backgroundColor: C.white, border, color: C.ink, padding: 30, boxShadow: shadow}}>
        <div style={{fontSize: 26, color: C.gray, fontWeight: 900}}>INPUT</div>
        <div style={{fontSize: 43, lineHeight: 1.35, fontWeight: 900, marginTop: 40}}>“我今天很难受。<br />不要建议。”</div>
      </div>
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 66, fontWeight: 900}}>→</div>
      <div style={{backgroundColor: C.ink, border, color: C.white, padding: 30, boxShadow: shadow}}>
        <div style={{fontSize: 26, color: C.lime, fontWeight: 900}}>RESPONSE CONTRACT</div>
        <div style={{marginTop: 34, display: 'grid', gap: 15}}>
          {['情绪场景', '不要分析', '低介入', '短回应'].map((word, i) => <div key={word} style={{backgroundColor: [C.cyan, C.red, C.yellow, C.blue][i], color: i === 2 ? C.ink : C.white, padding: '14px 16px', fontSize: 28, fontWeight: 900}}>{word}</div>)}
        </div>
      </div>
    </div>
    <div style={{marginTop: 54, display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 10}}>
      {['回答', '接住', '追问', '质疑', '留白'].map((word, i) => <div key={word} style={{border, padding: '24px 8px', textAlign: 'center', backgroundColor: i === 1 ? C.lime : C.white, color: C.ink, fontSize: 30, fontWeight: 900}}>{i === 1 ? '✓ ' : ''}{word}</div>)}
    </div>
    <div style={{marginTop: 48, backgroundColor: C.ink, color: C.white, border, padding: '30px 34px'}}>
      <div style={{fontSize: 25, color: C.lime, fontWeight: 900}}>OUTPUT</div>
      <div style={{fontSize: 42, lineHeight: 1.3, fontWeight: 900, marginTop: 14}}>听到了。今天确实很难受。</div>
    </div>
    <div style={{marginTop: 36, fontSize: 34, lineHeight: 1.4, fontWeight: 900}}>每一轮重新判断，不把“温柔”做成固定人设。</div>
  </Page>
);

const WritingPage: React.FC = () => (
  <Page index={4} background={C.yellow}>
    <Eyebrow>写作保真</Eyebrow>
    <div style={{fontSize: 94, lineHeight: .98, fontWeight: 900}}>轻改，<br /><span style={{backgroundColor: C.ink, color: C.white, padding: '0 14px'}}>不换掉你的声音。</span></div>
    <div style={{marginTop: 58, display: 'grid', gridTemplateColumns: '1fr 70px 1fr', alignItems: 'stretch'}}>
      <div style={{backgroundColor: C.white, border, padding: 28, boxShadow: shadow}}>
        <div style={{fontSize: 25, color: C.gray, fontWeight: 900}}>你的原句</div>
        <div style={{fontSize: 36, lineHeight: 1.45, fontWeight: 900, marginTop: 34}}>“我最近有点空，<br />也说不清自己在等什么。”</div>
      </div>
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 52, fontWeight: 900}}>→</div>
      <div style={{backgroundColor: C.ink, color: C.white, border, padding: 28, boxShadow: shadow}}>
        <div style={{fontSize: 25, color: C.lime, fontWeight: 900}}>保留犹豫感</div>
        <div style={{fontSize: 36, lineHeight: 1.45, fontWeight: 900, marginTop: 34}}>“最近有点空。<br />也不知道自己在等什么。”</div>
      </div>
    </div>
    <div style={{marginTop: 54, fontSize: 31, fontWeight: 900}}>保护三个表达不变量：</div>
    <div style={{marginTop: 22, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14}}>
      {[
        ['语义', '不增加结论'],
        ['强度', '不替你释怀'],
        ['节奏', '不抹平犹豫'],
      ].map(([title, desc], i) => <div key={title} style={{backgroundColor: i === 1 ? C.lime : C.white, border, padding: '28px 22px', minHeight: 170}}><div style={{fontSize: 43, fontWeight: 900}}>{title}</div><div style={{fontSize: 27, fontWeight: 800, marginTop: 22}}>{desc}</div></div>)}
    </div>
    <div style={{marginTop: 44, backgroundColor: C.red, color: C.white, border, padding: '26px 30px', fontSize: 38, lineHeight: 1.3, fontWeight: 900}}>只降低表达阻力，不替用户完成思想。</div>
    <div style={{marginTop: 36, backgroundColor: C.white, color: C.ink, border, padding: '24px 28px'}}>
      <div style={{fontSize: 27, color: C.gray, fontWeight: 900}}>改写验收三问</div>
      <div style={{marginTop: 20, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14, fontSize: 25, lineHeight: 1.35, fontWeight: 900}}>
        <span>✓ 有没有新增意思</span><span>✓ 情绪有没有变弱</span><span>✓ 还像不像本人</span>
      </div>
    </div>
  </Page>
);

const ReliabilityPage: React.FC = () => (
  <Page index={5}>
    <Eyebrow>可靠性与来源校准</Eyebrow>
    <div style={{fontSize: 90, lineHeight: 1.0, fontWeight: 900}}>资料没看，<br /><span style={{color: C.red}}>不装确定。</span></div>
    <div style={{marginTop: 68, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
      {[
        ['已确认', '有文件、工具或一手来源支持', C.ink, C.white],
        ['合理推断', '标明推断，不伪装成事实', C.cyan, C.white],
        ['未知项', '缺什么证据，就说缺什么', C.yellow, C.ink],
        ['对口来源', 'API 查官方，论文查原文', C.lime, C.ink],
      ].map(([title, desc, bg, color]) => <div key={title} style={{backgroundColor: bg, color, border, padding: 28, minHeight: 210}}><div style={{fontSize: 38, fontWeight: 900}}>{title}</div><div style={{fontSize: 29, lineHeight: 1.35, fontWeight: 700, marginTop: 20}}>{desc}</div></div>)}
    </div>
    <div style={{marginTop: 56, border, backgroundColor: C.white, boxShadow: shadow}}>
      {[
        ['实时事实', '联网核验当前价格、版本、法律'],
        ['代码判断', '先看代码、日志与复现'],
        ['资料检索', '优先官方文档与论文原文'],
      ].map(([kind, action], i) => <div key={kind} style={{display: 'grid', gridTemplateColumns: '190px 1fr', gap: 24, padding: '28px 30px', borderTop: i ? `3px solid ${C.ink}` : 'none', fontSize: 29}}><strong>{kind}</strong><span style={{color: C.cyan, fontWeight: 900}}>{action}</span></div>)}
    </div>
    <div style={{marginTop: 44, fontSize: 38, lineHeight: 1.35, fontWeight: 900}}>减少的不是“不知道”，<br />是<span style={{backgroundColor: C.red, color: C.white, padding: '2px 10px'}}>没证据的确定感</span>。</div>
  </Page>
);

const ProjectPage: React.FC = () => (
  <Page index={6} dark>
    <Eyebrow dark>做项目时</Eyebrow>
    <div style={{fontSize: 86, lineHeight: 1.0, fontWeight: 900}}>先拆因果链，<br /><span style={{color: C.lime}}>再主动推翻自己。</span></div>
    <div style={{marginTop: 66, display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 10}}>
      {['输入', '状态', '依赖', '输出', '不变量'].map((word, i) => <div key={word} style={{backgroundColor: i === 2 ? C.red : i === 4 ? C.lime : '#202020', color: i === 4 ? C.ink : C.white, border: `3px solid ${i === 2 ? C.red : i === 4 ? C.lime : '#555'}`, minHeight: 150, padding: '24px 14px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}><span style={{fontSize: 24, color: i === 4 ? C.ink : C.gray}}>0{i + 1}</span><strong style={{fontSize: 30}}>{word}</strong></div>)}
    </div>
    <div style={{marginTop: 58, backgroundColor: '#181818', border: `4px solid ${C.cyan}`, padding: 30}}>
      <div style={{fontSize: 28, color: C.cyan, fontWeight: 900}}>FIRST PRINCIPLES</div>
      <div style={{fontSize: 38, lineHeight: 1.4, fontWeight: 900, marginTop: 22}}>从系统真正拥有的输入、状态和约束开始，不凭熟悉感猜根因。</div>
    </div>
    <div style={{marginTop: 28, backgroundColor: C.yellow, color: C.ink, border, padding: 30}}>
      <div style={{fontSize: 28, color: C.red, fontWeight: 900}}>ADVERSARIAL FINISH</div>
      <div style={{fontSize: 38, lineHeight: 1.4, fontWeight: 900, marginTop: 22}}>结论写完，再找反例；修复完成，再跑回归和边界检查。</div>
    </div>
    <div style={{marginTop: 52, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14}}>
      {['原问题消失', '回归覆盖原因', '邻近边界正常'].map((word) => <div key={word} style={{border: `4px solid ${C.lime}`, padding: '28px 18px', fontSize: 28, lineHeight: 1.3, fontWeight: 900, textAlign: 'center'}}>✓ {word}</div>)}
    </div>
    <div style={{marginTop: 42, borderTop: `4px solid ${C.lime}`, borderBottom: `4px solid ${C.lime}`, padding: '26px 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
      <span style={{fontSize: 27, color: C.gray, fontWeight: 900}}>DONE GATE</span>
      <strong style={{fontSize: 35}}>修复 + 测试 + 边界检查</strong>
    </div>
  </Page>
);

const CtaPage: React.FC = () => (
  <Page index={7} background={C.red}>
    <Eyebrow dark>OPEN SOURCE / 欢迎测试</Eyebrow>
    <div style={{fontSize: 138, lineHeight: .9, fontWeight: 900, color: C.white}}>人味<br />Agent</div>
    <div style={{marginTop: 44, fontSize: 56, lineHeight: 1.15, fontWeight: 900}}>少一点套话。<br /><span style={{color: C.lime}}>多一点判断、分寸和证据。</span></div>
    <div style={{marginTop: 64, display: 'flex', flexWrap: 'wrap', gap: 12}}>
      {['Codex', 'Claude Code', 'Gemini CLI', 'Kimi Code', 'ChatGPT adapter'].map((word, i) => <span key={word} style={{backgroundColor: i === 4 ? C.ink : C.white, color: i === 4 ? C.white : C.ink, border: `3px solid ${C.ink}`, padding: '14px 20px', fontSize: 27, fontWeight: 900}}>{word}</span>)}
    </div>
    <div style={{marginTop: 78, backgroundColor: C.white, color: C.ink, border, padding: '36px 34px', boxShadow: shadow}}>
      <div style={{fontSize: 25, color: C.gray, fontWeight: 900}}>GITHUB</div>
      <div style={{fontSize: 36, lineHeight: 1.3, fontWeight: 900, marginTop: 16}}>github.com/FMStupid173/human-agent</div>
    </div>
    <div style={{marginTop: 54, backgroundColor: C.lime, color: C.ink, border, padding: '32px 34px'}}>
      <div style={{fontSize: 42, lineHeight: 1.3, fontWeight: 900}}>拿一条你真的会问 AI 的问题试一下。</div>
      <div style={{fontSize: 29, lineHeight: 1.45, fontWeight: 800, marginTop: 20}}>最想收到的反馈：它哪里仍然很 AI，哪里判断错了。</div>
    </div>
  </Page>
);

const slides = [HumanAgentCover, PainPage, DynamicPage, WritingPage, ReliabilityPage, ProjectPage, CtaPage];

export const HumanAgentXhsCarousel: React.FC = () => {
  const frame = useCurrentFrame();
  const Slide = slides[Math.min(slides.length - 1, Math.floor(frame))];
  return <Slide />;
};
