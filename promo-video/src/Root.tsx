import React from 'react';
import {Composition} from 'remotion';
import {HumanAgentPromo} from './HumanAgentPromo';
import {HumanAgentCover, HumanAgentXhsCarousel} from './HumanAgentSocial';

export const Root: React.FC = () => (
  <>
    <Composition
      id="HumanAgentPromo"
      component={HumanAgentPromo}
      durationInFrames={900}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="HumanAgentCover"
      component={HumanAgentCover}
      durationInFrames={1}
      fps={1}
      width={1242}
      height={1660}
    />
    <Composition
      id="HumanAgentXhsCarousel"
      component={HumanAgentXhsCarousel}
      durationInFrames={7}
      fps={1}
      width={1242}
      height={1660}
    />
  </>
);
