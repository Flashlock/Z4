/// <reference types="vite/client" />

interface PantheonHitlBootstrap {
  focusedBreakpointId?: string;
  queueLength?: number;
}

interface PantheonBootstrap {
  instanceId: string;
  hubBaseUrl: string;
  hubPort: number;
  proxyBasePath: string;
  mfeSession: string;
  hitl?: PantheonHitlBootstrap;
}

interface Window {
  __PANTHEON__?: PantheonBootstrap;
}
