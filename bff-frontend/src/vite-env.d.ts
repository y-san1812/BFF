/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Full API base including `/api/v1`. Required for staging/production builds. */
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare module "*.jsx" {
  import type { ComponentType } from "react";
  const component: ComponentType<any>;
  export default component;
}

declare module "*.js" {
  const content: any;
  export default content;
}
