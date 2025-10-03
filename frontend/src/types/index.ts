export interface BrandInput {
  name: string;
  mission: string;
  values: string;
  audience: string;
  sector: string;
}

export interface UXKit {
  palette: {
    primary: string;
    secondary: string;
    neutral: string[];
  };
  typography: {
    family: string;
    importUrl: string;
  };
  tokens: {
    spacing: Record<string, string>;
    radii: Record<string, string>;
    shadows: Record<string, string>;
    opacity: Record<string, string>;
  };
  explanation: string;
  exports: {
    css: string;
    json: any;
    figma: any;
  };
}