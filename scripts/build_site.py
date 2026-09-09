#!/usr/bin/env python3
"""Render checked-in static pages from one shell, shared cards and HTML fragments."""
from pathlib import Path
from html import escape
import argparse
import base64
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://yossefseit.github.io'
CV = '/Yossef_Mohammed_Ali_CV.pdf'
GITHUB = 'https://github.com/yossefseit'
ICONS = {
 'overview':'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'projects':'<path d="M3 7h7l2 2h9v11H3Z"/><path d="M3 7V4h7l2 3"/>',
 'infrastructure':'<rect x="8" y="2" width="8" height="6" rx="1"/><path d="M12 8v5M4 13h16M4 13v3m8-3v3m8-3v3"/><rect x="1" y="16" width="6" height="5" rx="1"/><rect x="9" y="16" width="6" height="5" rx="1"/><rect x="17" y="16" width="6" height="5" rx="1"/>',
 'experience':'<rect x="3" y="6" width="18" height="15" rx="2"/><path d="M8 6V3h8v3M3 12h18m-11-2v4h4v-4"/>',
 'skills':'<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-14-2 16"/>',
 'about':'<circle cx="12" cy="7" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7L22 6"/>',
 'download':'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
 'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'external':'<path d="M14 3h7v7m-1-6-9 9M10 4H4v16h16v-6"/>',
 'search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
 'theme':'<circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/>',
 'menu':'<path d="M3 6h18M3 12h18M3 18h18"/>',
 'github':'<path d="M9 20c-5 1-5-3-7-3m14 6v-4a4 4 0 0 0-1-3c4-.5 6-2 6-6 0-2-1-3-2-4 .2-1 .2-3-.3-4-2 0-4 1-5 2a14 14 0 0 0-4 0C8 3 6 2 4 2c-.5 1-.5 3 0 4-1 1-2 2-2 4 0 4 2 5.5 6 6-.8 1-1 2-1 3v4"/>',
 'cloud':'<path d="M6 19a5 5 0 0 1-1-10 7 7 0 0 1 13-2 6 6 0 0 1 0 12Z"/>',
 'reliability':'<path d="M12 2 3 6v6c0 5 9 10 9 10s9-5 9-10V6ZM7 12l3 3 7-7"/>',
 'systems':'<rect x="3" y="2" width="18" height="8" rx="2"/><rect x="3" y="14" width="18" height="8" rx="2"/><path d="M7 6h.01M7 18h.01m5-12h5m-5 12h5"/>',
}
def icon(name):
 return f'<svg class="icon" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'
def ext(url,label,cls=''):
 return f'<a href="{escape(url)}" class="{cls}">{label}{icon("external")}</a>'
PROJECTS = [
 dict(slug='egypt-salary-calculator',name='Egypt Salary Calculator',category='01 / Application delivery',problem='Make gross-to-net salary calculations transparent, then ship a tested static application through GitHub Pages.',stack=['React','TypeScript','GitHub Pages','GitHub Actions'],status='57 tests passing; GitHub Pages deployment configured',image='salary-calculator.webp',alt='Local Egypt Salary Calculator application showing salary inputs and a calculated breakdown',pipeline='https://github.com/yossefseit/egypt-salary-calculator/blob/main/.github/workflows/deploy-pages.yml',pipeline_label='Pipeline config'),
 dict(slug='azure-secure-hub-spoke',name='Secure Azure Hub-and-Spoke Lab',category='02 / Network architecture',problem='Define segmented Azure networks and private Blob access with explicit routing, DNS and lifecycle controls.',stack=['Azure networking','Bicep','Private Link','Bash'],status='Lab: CI validated; Azure deployment pending',image='hub-card.svg',alt='Hub peered with separate application and data spokes; direct cross-spoke transit is blocked',pipeline='https://github.com/yossefseit/azure-secure-hub-spoke/actions/runs/30944553717'),
 dict(slug='azure-governance-automation',name='Azure Governance Automation Lab',category='03 / Governance as code',problem='Make subscription guardrails repeatable through audit-first policy, scoped access, budgets and protected cleanup.',stack=['Azure Policy','RBAC','Bicep','PowerShell'],status='Lab: CI validated; Azure deployment pending',image='governance-card.svg',alt='Azure subscription with policy, access, budget and resource-lock controls',pipeline='https://github.com/yossefseit/azure-governance-automation/actions/runs/31267342614')
]
def project_cards():
 cards=[]
 for i,p in enumerate(PROJECTS):
  stack=''.join(f'<span>{escape(s)}</span>' for s in p['stack'])
  cards.append(f'''<article class="project-card{' project-featured' if i==0 else ''}">
  <div class="project-art"><img src="/assets/{p['image']}" width="960" height="500" {'fetchpriority="high"' if i==0 else 'loading="lazy"'} alt="{p['alt']}"></div>
  <div class="project-content"><p class="eyebrow">{p['category']}</p><h3>{p['name']}</h3><p>{p['problem']}</p><div class="stack">{stack}</div><span class="status">{p['status']}</span>
  <div class="project-links"><a href="/projects/{p['slug']}/">Case study {icon('arrow')}</a>{ext(GITHUB+'/'+p['slug'],'Code')}{ext(p['pipeline'],p.get('pipeline_label','Pipeline evidence'))}</div></div></article>''')
 return '<div class="project-grid">'+''.join(cards)+'</div>'
NAV=[('overview','Overview','/'),('projects','Projects','/projects/'),('infrastructure','Infrastructure','/infrastructure/'),('experience','Experience','/experience/'),('skills','Skills','/skills/'),('about','About & contact','/about/')]
PAGES=[
 ('/', 'overview','Overview','Yossef Mohammed Ali | Cloud Infrastructure & DevOps','Cloud Infrastructure & DevOps Engineer in Cairo. Explore Azure application delivery, Bicep networking and governance labs, and IT infrastructure experience.','overview.html','og-cover.png'),
 ('/projects/','projects','Projects','Selected projects | Yossef Mohammed Ali','Explore Egypt Salary Calculator, Azure networking and governance labs, with source code, architecture decisions and dated pipeline evidence.','projects.html','og-cover.png'),
 ('/infrastructure/','infrastructure','Infrastructure','Infrastructure | Yossef Mohammed Ali','Inspect the portfolio delivery architecture and personal cloud and identity labs, with readable topology diagrams and clear deployment boundaries.','infrastructure.html','og-cover.png'),
 ('/experience/','experience','Experience','Experience & training | Yossef Mohammed Ali','Professional infrastructure experience at Electrolux, Aegis and El Mostafa, alongside ongoing DevOps training, completed academy programs and education.','experience.html','og-cover.png'),
 ('/skills/','skills','Skills','Skills & engineering practice | Yossef Mohammed Ali','Cloud, automation, delivery, systems and reliability skills: Azure project work, enterprise infrastructure operations and ongoing AWS, Terraform and Kubernetes learning.','skills.html','og-cover.png'),
 ('/about/','about','About & contact','About & contact | Yossef Mohammed Ali','Meet Yossef Mohammed Ali, a Cairo-based infrastructure professional building cloud delivery skills. Connect by email, LinkedIn or GitHub, or download the CV.','about.html','og-cover.png'),
 ('/projects/egypt-salary-calculator/','projects','Salary calculator','Egypt Salary Calculator | Yossef Mohammed Ali','A React and TypeScript salary calculator configured for GitHub Pages, with 57 verified tests and clearly dated historical App Service evidence.','salary.html','salary-social.png'),
 ('/projects/azure-secure-hub-spoke/','projects','Hub-and-spoke lab','Secure Azure Hub-and-Spoke Lab | Yossef Mohammed Ali','A Bicep lab for segmented Azure networks, private Blob access and guarded lifecycle scripts. CI validated; Azure deployment and runtime validation pending.','hub.html','hub-social.png'),
 ('/projects/azure-governance-automation/','projects','Governance lab','Azure Governance Automation Lab | Yossef Mohammed Ali','Audit-first subscription governance in Bicep: Azure Policy, RBAC, budgets and locks with guarded lifecycle scripts. CI validated; Azure deployment pending.','governance.html','governance-social.png'),
 ('/projects/samba-ad-dc-lab/','projects','Samba identity lab','Samba AD DC Lab | Yossef Mohammed Ali','An isolated Ubuntu Samba identity lab with guarded Bash stages for DNS, Kerberos, signed time and backup. CI validated; runtime and recovery evidence pending.','samba.html','samba-social.png'),
]
JSON_LD=json.dumps({'@context':'https://schema.org','@graph':[{'@type':'Person','@id':ORIGIN+'/#person','name':'Yossef Mohammed Ali','url':ORIGIN+'/','jobTitle':'IT Infrastructure Analyst','worksFor':{'@type':'Organization','name':'Electrolux Group'},'description':'Cloud Infrastructure & DevOps Engineer with professional IT infrastructure experience and personal Azure automation projects.','alumniOf':{'@type':'CollegeOrUniversity','name':'El Shorouk Academy'},'knowsAbout':['Microsoft Azure','AWS','Bicep','Terraform','Kubernetes','GitHub Actions','Windows Server','Linux','Networking','Backup and recovery'],'sameAs':[GITHUB,'https://www.linkedin.com/in/yossef-ali/']},{'@type':'WebSite','url':ORIGIN+'/','name':'Yossef Mohammed Ali | Infrastructure & DevOps','inLanguage':'en'}]},indent=2,ensure_ascii=False)

def build_page(route,active,label,title,description,fragment,social):
 nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if key==active else '')+f'>{icon(key)}{escape(text)}'+('<span class="nav-count">03</span>' if key=='projects' else '')+'</a>' for key,text,url in NAV)
 commands=[('Projects','/projects/','Selected work'),('Experience','/experience/','Career & training'),('Skills','/skills/','Engineering practice'),('Infrastructure','/infrastructure/','Delivery & lab diagrams'),('Download CV',CV,'PDF'),('GitHub',GITHUB,'External'),('Contact','/about/#contact','Email & LinkedIn'),('About','/about/','Background')]
 command_html=''.join(f'<li id="command-{i}" data-command><a href="{url}">{escape(text)}<span>{escape(hint)}</span></a></li>' for i,(text,url,hint) in enumerate(commands))
 body=(ROOT/'content'/fragment).read_text().replace('{{PROJECT_CARDS}}',project_cards()).replace('{{CV}}',CV).replace('{{ORIGIN}}',ORIGIN)
 body=re.sub(r'\{\{ICON:(\w+)\}\}',lambda m:icon(m[1]),body)
 schema=f'<script type="application/ld+json">{JSON_LD}</script>' if route=='/' else ''
 digest=base64.b64encode(hashlib.sha256(JSON_LD.encode()).digest()).decode()
 csp=("default-src 'none'; script-src 'self' 'sha256-"+digest+"'; script-src-attr 'none'; "
      "style-src 'self'; style-src-attr 'none'; img-src 'self' data:; font-src 'self'; "
      "connect-src 'none'; media-src 'none'; object-src 'none'; frame-src 'none'; "
      "worker-src 'none'; manifest-src 'self'; base-uri 'none'; form-action 'none'; "
      "upgrade-insecure-requests")
 values={'title':escape(title),'description':escape(description),'canonical':ORIGIN+route,'label':escape(label),'social':ORIGIN+'/assets/'+social,'social_alt':escape('Yossef Mohammed Ali — Cloud Infrastructure & DevOps Engineer' if social=='og-cover.png' else title.split(' | ')[0]+' — architecture and implementation'),'schema':schema,'nav':nav,'commands':command_html,'body':body,'cv':CV,'github':GITHUB,'csp':csp,'og_type':'article' if route.count('/')>2 else 'website','social_type':'image/png','social_width':'1200','social_height':'630'}
 template=(ROOT/'templates/page.html').read_text()
 for key,value in values.items():template=template.replace('{{'+key+'}}',value)
 if re.search(r'\{\{.+?\}\}',template):raise ValueError('Unresolved template token in '+route)
 return template

def outputs():
 result={}
 for page in PAGES:
  route=page[0];path=ROOT/route.lstrip('/')/'index.html' if route!='/' else ROOT/'index.html'
  result[path]=build_page(*page)
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{ORIGIN}{p[0]}</loc></url>\n' for p in PAGES)+'</urlset>\n'
 result[ROOT/'sitemap.xml']=sitemap
 result[ROOT/'Yossef_Mohammed_Ali_CV.pdf']=(ROOT/'assets/Yossef_Mohammed_Ali_CV.pdf').read_bytes()
 return result

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();out=outputs();stale=[]
 for path,value in out.items():
  if args.check:
   current=path.read_bytes() if isinstance(value,bytes) and path.exists() else path.read_text() if path.exists() else None
   if current!=value:stale.append(str(path.relative_to(ROOT)))
  else:
   path.parent.mkdir(parents=True,exist_ok=True)
   path.write_bytes(value) if isinstance(value,bytes) else path.write_text(value)
 if stale:raise SystemExit('Generated files differ. Run python3 scripts/build_site.py: '+', '.join(stale))
 print(('Verified' if args.check else 'Rendered')+f' {len(PAGES)} static pages, sitemap, meta CSP and root CV mirror.')
if __name__=='__main__':main()
