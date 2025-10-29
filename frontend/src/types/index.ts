export interface BrandInput {
  name: string
  mission: string
  values: string
  audience: string
  sector: string
}

export interface UXKit {
  palette: { primary: string; secondary: string; neutral: string[] }
  typography: { family: string; importUrl: string }
  tokens: any
  explanation: string
  exports: any
}
