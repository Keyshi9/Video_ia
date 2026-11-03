import React from "react"; import { Composition, registerRoot } from "remotion"; import { BridgeShort, BRIDGE_FRAMES } from "../../videos/bastille_post/Bridge";
const Root: React.FC = () => <Composition id="Bastille" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />; registerRoot(Root);
