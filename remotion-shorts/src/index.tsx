import React from "react";
import { Composition, registerRoot } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
import { BridgeShort as RevolutionShort, BRIDGE_FRAMES as REV_FRAMES } from "./videos/revolution/Bridge";
import { BridgeShort as BastilleShort, BRIDGE_FRAMES as BASTILLE_FRAMES } from "./videos/bastille/Bridge";

const Root: React.FC = () => (
  <>
    <Composition id="BridgeShort" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Revolution" component={RevolutionShort} durationInFrames={REV_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Bastille" component={BastilleShort} durationInFrames={BASTILLE_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
registerRoot(Root);
