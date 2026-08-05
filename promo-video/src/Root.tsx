import React from 'react';
import {Composition} from 'remotion';
import {HumanAgentPromo} from './HumanAgentPromo';

export const Root: React.FC = () => (
  <Composition
    id="HumanAgentPromo"
    component={HumanAgentPromo}
    durationInFrames={900}
    fps={30}
    width={1080}
    height={1920}
  />
);
