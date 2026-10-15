import pdfplumber,re,html
from pathlib import Path
with pdfplumber.open('output/pdf/仇江涛_前端开发.pdf') as d:
    lines=[line for p in d.pages for line in p.extract_text().splitlines()]
replacements=[('Ant Design Vue','Ant Design'),('Vue Test Utils','React Testing Library'),('vue-i18n','react-i18next'),('Vue2/Vue3 全家桶生态','React 生态'),('Vue 3','React 18'),('Vue 2','React'),('Vue/TypeScript','React/TypeScript'),('Vuex','Redux'),('Pinia','Redux Toolkit'),('Element Plus','Ant Design'),('基于 i18n + react-i18next','基于 i18next + react-i18next'),('所有图表组件继承自同一基类','所有图表组件复用统一的图表封装')]
sections={'基本信息','教育背景','工作经历','项目经验','技能特长','自我评价'}
projects={'智能合同审查与条款比对系统','信托业务中台管理系统（微前端架构升级 + AI 智能模块）','维信金科金融仪表盘（实时监控大屏）','维信卡卡贷 App','跨境云仓·全球供应链协同平台','前端流程编排引擎'}
parts=[]; buf=[]
def flush():
    if buf:
        s=''.join(buf)
        for a,b in replacements:s=s.replace(a,b)
        cls='tech' if s.startswith('技术栈：') else ''
        parts.append('<p class="'+cls+'">'+html.escape(s)+'</p>');buf.clear()
for line in lines:
    if line=='Web前端开发' or '\ue6b1' in line or '\ue656' in line or line=='计算机科学与技术专业，本科':continue
    if line in sections or line in projects:
        flush(); tag='h2' if line in sections else 'h3';parts.append(f'<{tag}>{html.escape(line)}</{tag}>')
    elif line in {'项目简介：','核心职责：'}:
        flush();parts.append('<h4>'+line+'</h4>')
    elif re.match(r'^\d+\.',line) or line.startswith('技术栈：') or re.match(r'^20\d\d\.\d\d -',line) or line.startswith(('姓 名：','求职岗位：','邮 箱：')):
        flush();buf.append(line)
    else:buf.append(line)
flush()
body='\n'.join(parts)
assert not re.search(r'Vue|vue|Pinia|Element Plus',body)
source='''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><title>仇江涛 - React 前端开发工程师</title><style>
@page {size:A4;margin:14mm 14mm;} body{font-family:"PingFang SC","Arial",sans-serif;color:#243548;font-size:10pt;line-height:1.48;margin:0;} h1{font-size:24pt;color:#0b3b5f;margin:0 0 3mm;} .subtitle{color:#456780;margin-bottom:5mm;} h2{font-size:14pt;color:#0b3b5f;border-bottom:1px solid #9bafbf;padding-bottom:1.3mm;margin:5mm 0 2mm;break-after:avoid;} h3{font-size:11.5pt;color:#0b3b5f;margin:4mm 0 1.5mm;break-after:avoid;} h4{font-size:10pt;margin:2mm 0 1mm;break-after:avoid;} p{margin:0 0 2mm;orphans:2;widows:2;} .tech{background:#eef3f7;padding:2mm 3mm;font-size:9.4pt;break-inside:avoid;}
</style><body><h1>仇江涛</h1><div class="subtitle">资深前端开发工程师 · React</div>'''+body+'</body></html>'
Path('前端开发工程师-仇江涛-React完整版.html').write_text(source)
