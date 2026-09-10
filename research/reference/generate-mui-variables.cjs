const { createTheme, extendTheme } = require('@mui/material/styles');
const merge = require('lodash/merge');

const DEFAULT_COLOR_SCHEME = {
  palette: {
    mode: 'dark',
    primary: { main: '#00a4dc' },
    secondary: { main: '#aa5cc3' },
    background: { default: '#101010', paper: '#202020' },
    action: { selectedOpacity: 0.2 },
    starIcon: { main: '#f2b01e' },
    error: { main: '#c62828' }
  }
};
const DEFAULT_THEME_OPTIONS = {
  typography: {
    fontFamily: '"Noto Sans", sans-serif',
    button: { textTransform: 'none' },
    h1: { fontSize: '1.8rem' }, h2: { fontSize: '1.5rem' }, h3: { fontSize: '1.17rem' }
  }
};
const defaultMuiTheme = extendTheme({ colorSchemes: { dark: true, light: true } });
const build = (o) => merge({}, o.palette?.mode === 'light' ? defaultMuiTheme.colorSchemes.light : defaultMuiTheme.colorSchemes.dark, DEFAULT_COLOR_SCHEME, o);

const light = merge({}, DEFAULT_COLOR_SCHEME, { palette: { mode:'light', background:{default:'#f2f2f2',paper:'#e8e8e8'}, AppBar:{defaultBg:'#e8e8e8'} }});
const purplehaze = build({ palette:{ background:{paper:'#000420'}, primary:{main:'#48c3c8'}, secondary:{main:'#ff77f1'}, AppBar:{defaultBg:'#000420'} }});
const blueradiance = build({ palette:{ background:{paper:'#011432'}, AppBar:{defaultBg:'#011432'} }});
const wmc = build({ palette:{ background:{paper:'#0c2450'}, AppBar:{defaultBg:'#0c2450'} }});
const appletv = build({ palette:{ mode:'light', background:{default:'#d5e9f2',paper:'#fff'}, AppBar:{defaultBg:'#bcbcbc'} }});

const THEME = createTheme({
  cssVariables: { cssVarPrefix: 'jf', colorSchemeSelector: '[data-theme="%s"]', disableCssColorScheme: true },
  defaultColorScheme: 'dark',
  ...DEFAULT_THEME_OPTIONS,
  colorSchemes: { appletv, blueradiance, dark: DEFAULT_COLOR_SCHEME, light, purplehaze, wmc }
});

const sheets = THEME.generateStyleSheets();
let out = '';
for (const s of sheets) {
  for (const [sel, decls] of Object.entries(s)) {
    out += `${sel} {\n`;
    for (const [k, v] of Object.entries(decls)) out += `  ${k}: ${v};\n`;
    out += `}\n\n`;
  }
}
console.log(out);
