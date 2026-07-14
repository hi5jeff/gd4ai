// gd4.ai i18n — embedded in index.html
const I18N = {
  zh: {
    logo: 'gd4.ai',
    subtitle: '说出你想做什么，给你一套能直接跑通的 AI 工具方案',
    placeholder: '例如：我想做一个电商网站',
    btn: '推荐方案',
    loading: 'AI 正在从组件库检索并组合方案（约 10~20 秒）…',
    footer: 'gd4.ai · 所有推荐均来自人工核实的组件库，命令可直接复制使用',
    serverError: '服务暂时不可用，请稍后重试。',
    justNow: '刚刚',
    copy: '复制',
    copied: '已复制✓',
    noResult: '库里暂时没有和这个需求精确匹配、经过验证的方案。我们已记录你的需求，会优先补充。',
    nearMatch: '下面是最接近的内容（非精确匹配，仅供参考）：',
    searchFallback: 'AI 编排暂时不可用，以下是检索到的最相关内容：',
    chips: ['🛒 做电商网站', '📸 人像提示词', '💰 省 Token', '🎮 游戏动画', '🎨 平面设计', '🏠 室内装修'],
    chipValues: ['做一个电商网站', '生成美女人像图的提示词', '省token的方法', '游戏开发的动画怎么做', '设计一张海报', '室内装修效果图'],
    sectionPlan: '📦 完整方案：',
    sectionComponents: '🧩 需要的组件',
    sectionSingle: '🧩 推荐组件',
    sectionPrompts: '✨ 可直接复制的提示词',
    sectionSteps: '🛠 操作步骤',
    sectionPrompt: '💬 复制这条提示词开始',
    sectionPitfalls: '⚠️ 常见坑',
    sectionSource: '来源 ↗',
    badgeOptional: '（可选）',
    diff: { beginner: '新手友好', intermediate: '需要动手', advanced: '进阶' },
    installNote: '说明：',
    needPrepare: '需要准备：',
    firstPrompt: '第一条提示词：',
    verify: '验证：',
    security: '⚠ 安全：',
    typeLabels: { mcp: 'MCP', skill: 'Skill', prompt: 'Prompt', tool: 'Tool', role: 'Role', plugin: 'Plugin', workflow: 'Workflow' },
  },
  en: {
    logo: 'gd4.ai',
    subtitle: 'Tell us what you want to build, we give you a ready-to-run AI tool stack',
    placeholder: 'e.g. I want to build an e-commerce site',
    btn: 'Get Recommendations',
    loading: 'AI is searching our component library and composing a plan (~10–20s)…',
    footer: 'gd4.ai · All recommendations are verified and sourced from our curated library',
    serverError: 'Service temporarily unavailable. Please try again later.',
    justNow: 'Just now',
    copy: 'Copy',
    copied: 'Copied ✓',
    noResult: 'We don\'t have a verified solution for this exact need yet. Your request has been logged and will be prioritized for curation.',
    nearMatch: 'Here are the closest matches (not exact, for reference):',
    searchFallback: 'AI orchestration is temporarily unavailable. Here are the closest matches from our library:',
    chips: ['🛒 E-commerce', '📸 Portrait Prompts', '💰 Save Tokens', '🎮 Game Animation', '🎨 Graphic Design', '🏠 Interior Design'],
    chipValues: ['build an e-commerce site', 'generate beautiful portrait photo prompts', 'save tokens in claude code', 'game animation development tools', 'design a poster', 'interior design rendering'],
    sectionPlan: '📦 Complete Plan: ',
    sectionComponents: '🧩 Components',
    sectionSingle: '🧩 Recommended Components',
    sectionPrompts: '✨ Ready-to-Copy Prompts',
    sectionSteps: '🛠 Steps',
    sectionPrompt: '💬 Copy this prompt to start',
    sectionPitfalls: '⚠️ Common Pitfalls',
    sectionSource: 'Source ↗',
    badgeOptional: ' (optional)',
    diff: { beginner: 'Beginner', intermediate: 'Intermediate', advanced: 'Advanced' },
    installNote: 'Note: ',
    needPrepare: 'Prerequisites: ',
    firstPrompt: 'First prompt: ',
    verify: 'Verify: ',
    security: '⚠ Security: ',
    typeLabels: { mcp: 'MCP', skill: 'Skill', prompt: 'Prompt', tool: 'Tool', role: 'Role', plugin: 'Plugin', workflow: 'Workflow' },
  },
};

let _lang = 'zh';
function setLang(l) { _lang = l; localStorage.setItem('gd4ai-lang', l); }
function t(key) { return (I18N[_lang][key] || I18N.zh[key] || key); }
function td(key) { return (I18N[_lang].diff || I18N.zh.diff)[key] || key; }
function tt(key) { return (I18N[_lang].typeLabels || I18N.zh.typeLabels)[key] || key.toUpperCase(); }

function detectLang() {
  const saved = localStorage.getItem('gd4ai-lang');
  if (saved) return saved;
  // Browser Accept-Language
  const nav = (navigator.language || '').toLowerCase();
  if (nav.startsWith('zh')) return 'zh';
  if (nav.startsWith('en')) return 'en';
  return 'zh';
}