"""Render the portfolio from factual project copy and a small set of shared templates."""
from pathlib import Path
from html import escape
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://schaafconnor0-collab.github.io/ConnorSchaafPortfolio'
EMAIL = 'schaafconnor0@gmail.com'
CONTENT = json.loads((ROOT/'scripts/project_content.json').read_text(encoding='utf-8-sig'))
PROFILE = json.loads((ROOT/'scripts/profile_content.json').read_text(encoding='utf-8-sig'))
PROJECTS = {
    'locomotion': {'title':'Locomotion', 'image':'locomotion-keyart.webp', 'image_alt':'Locomotion team artwork', 'image_credit':'Artwork by the LOCOMotion team.', 'summary':'Locomotion is a party racing game where players receive obstacle items that can be placed permanently on the map. As players complete more laps, more obstacles are placed around the track for everyone to avoid.', 'status':'Alpha Development Stage', 'video':'locomotion-prototype.mp4', 'poster':'locomotion-whitebox.webp', 'document':'locomotion-gdd.pdf'},
    'project-hope': {'title':'Project: Hope', 'image':'hope-partners.png', 'image_alt':'Ukraine Volya Foundation and Lizzard Games logos', 'image_credit':'Ukraine Volya Foundation × Lizzard Games.', 'image_fit':'contain', 'summary':'A student-led project developed in tandem with the Ukraine Volya Foundation. Gamified mental health for children who have experienced major traumatic events.', 'status':'Early Production Stage', 'document':'hope-technical-proposal.pdf'},
    'mags-n-magic': {'title':'Mags & Magic', 'image':'mags-title.png', 'image_alt':'Mags and Magic title artwork with the game’s town environment', 'image_credit':'Project artwork by the P.D.C.U. team.', 'summary':'My first major team project. A fully functional multiplayer hero shooter created in under four months, with three selectable heroes and four purchasable guns.', 'home_byline':'Project Complete', 'video':'mags-gameplay.mp4', 'poster':'mags-action.webp'},
    'trials-of-the-arcane-academy': {'title':'The Trials of the Arcane Academy', 'image':'arcane-menu.png', 'image_alt':'Arcane Academy main menu with the academy at night', 'image_credit':'Main menu screen.', 'summary':'Built from a turn-based RPG template, this story-based wizarding game takes players through five trials.', 'home_byline':'Solo Project · Project Complete', 'youtube':'https://www.youtube.com/watch?v=CNJ26PIc7k0'},
}


def header(active):
    nav=[]
    for key,label,url in [('work','Projects','index.html'),('docs','Documents','documents.html'),('about','About','about.html'),('resume','Résumé','assets/resume/ConnorSchaafResume.pdf')]:
        current=' aria-current="page"' if key==active else ''
        nav.append(f'<a href="{url}"{current}>{label}</a>')
    return f'<a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><a class="identity" href="index.html"><strong>Connor Schaaf</strong><span>Technical Game Designer</span></a><nav class="main-nav" aria-label="Main navigation">{"".join(nav)}</nav></header>'


def footer():
    return '<footer class="wrap footer"><p>© <span data-year>2026</span> Connor Schaaf</p></footer>'


def render(filename,title,description,body,active='work',image='locomotion-keyart.webp'):
    text=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} | Connor Schaaf</title><meta name="description" content="{escape(description,quote=True)}"><meta property="og:title" content="{escape(title,quote=True)} | Connor Schaaf"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:image" content="{ORIGIN}/assets/site/{image}"><link rel="canonical" href="{ORIGIN}/{filename if filename!='index.html' else ''}"><meta name="theme-color" content="#ffffff"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="css/style.css"></head><body>{header(active)}<main class="wrap" id="main">{body}</main>{footer()}<script src="js/main.js" defer></script></body></html>'''
    (ROOT/filename).write_text(text,encoding='utf-8')


def link(url,label,new=False):
    extra=' target="_blank" rel="noopener"' if new else ''
    return f'<a href="{url}"{extra}>{label}</a>'


def switcher(slug):
    links=[]
    for key,meta in PROJECTS.items():
        current=' aria-current="page"' if key==slug else ''
        short='Arcane Academy' if key=='trials-of-the-arcane-academy' else meta['title']
        links.append(f'<a href="{key}.html"{current}>{escape(short)}</a>')
    return '<nav class="project-switcher" aria-label="Projects">'+''.join(links)+'</nav>'


def picture(meta):
    fit=' contain' if meta.get('image_fit')=='contain' else ''
    return f'<div><div class="project-picture{fit}"><img src="assets/site/{meta["image"]}" alt="{meta["image_alt"]}" width="780" height="439" loading="lazy"></div><p class="image-credit">{meta["image_credit"]}</p></div>'


introduction=''.join('<p>'+escape(p)+'</p>' for p in PROFILE['introduction'])
home='<section class="intro"><h1>Game projects</h1>'+introduction+'</section><section class="project-index" aria-label="Selected projects" id="work">'
for slug,meta in PROJECTS.items():
    item=CONTENT[slug]
    byline=meta.get('home_byline') or item['role']+' · '+meta['status']
    home+=f'<article class="project-row">{picture(meta)}<div><h2>{link(slug+".html",escape(meta["title"]))}</h2><p class="project-role">{escape(byline)}</p><p>{meta["summary"]}</p></div></article>'
home+='</section>'
render('index.html','Game Projects','Connor Schaaf’s game design projects, Unreal Blueprint work, gameplay videos, and design documentation.',home)


def media_block(slug):
    meta=PROJECTS[slug]
    if meta.get('video'):
        duration='This video shows the multiplayer system working with replication. One player is the server and the other is a client, and each can see the other moving on screen. This test map was made simply to demonstrate functional multiplayer systems.' if slug=='locomotion' else '1 minute 36 seconds. Team gameplay, including my Vampire and Fairy work.'
        return f'<figure class="project-media" id="gameplay"><video controls playsinline preload="metadata" poster="assets/site/{meta["poster"]}" aria-label="{escape(meta["title"],quote=True)} gameplay"><source src="assets/site/{meta["video"]}" type="video/mp4">{link("assets/site/"+meta["video"],"Download gameplay video")}</video><figcaption>{duration}</figcaption></figure>'
    if meta.get('document'):
        image = '<img class="document-image" src="assets/site/hope-technical-proposal.webp" alt="Preview of my technical proposal" width="600" height="338">'
        preview = link('assets/docs/'+meta['document'], image, True)
        caption = link('assets/docs/'+meta['document'], 'Read the technical requirements (PDF)', True)
        return f'<figure class="project-media">{preview}<figcaption>{caption} · October 29, 2026</figcaption></figure>'
    if meta.get('youtube'):
        image = '<img src="assets/site/arcane-environment.webp" alt="Arcane Academy project scene; open the video walkthrough" width="800" height="446">'
        preview = link(meta['youtube'], image, True)
        caption = link(meta['youtube'], 'Watch the project walkthrough on YouTube', True)
        return f'<figure class="project-media">{preview}<figcaption>{caption}</figcaption></figure>'
    return ''


def image_figure(filename,alt,caption):
    image = f'<img src="assets/site/{filename}" alt="{escape(alt,quote=True)}" loading="lazy">'
    preview = link('assets/site/'+filename, image, True)
    full = link('assets/site/'+filename, 'Open full-size image', True)
    return f'<figure class="evidence-image">{preview}<figcaption>{caption} {full}</figcaption></figure>'


for slug,meta in PROJECTS.items():
    item=CONTENT[slug]
    facts=[{'label':'My role','value':item['role']}]+[f for f in item['facts'] if f['label']!='Focus']
    overview=''.join('<p>'+escape(p)+'</p>' for p in item.get('overview_paragraphs',[item['overview']]))
    body=switcher(slug)+f'<header class="page-heading"><h1>{escape(meta["title"])}</h1>'+overview+'<div class="project-facts">'+''.join(f'<span><b>{escape(f["label"])}:</b> {escape(f["value"])}</span>' for f in facts)+'</div></header>'
    body+='<div class="project-summary">'+media_block(slug)+'<section class="contributions" id="contribution"><h2>My contribution</h2><ul>'+''.join('<li>'+escape(c)+'</li>' for c in item['contributions'])+'</ul></section></div><div class="project-body">'
    for section in item['sections']:
        body+=f'<section class="content-section" id="{section["id"]}"><h2>{escape(section["title"])}</h2>'+''.join('<p>'+escape(p)+'</p>' for p in section['paragraphs'])
        if slug=='locomotion' and section['id']=='documentation': body+='<div class="resource-links">'+link('assets/docs/locomotion-gdd.pdf','Read the full game design document (PDF)',True)+'</div>'
        if slug=='project-hope' and section['id']=='technical': body+='<div class="resource-links">'+link('assets/docs/hope-technical-proposal.pdf','Read the technical requirements (PDF)',True)+'</div>'
        if slug=='mags-n-magic' and section['id']=='leaderboard': body+=image_figure('mags-leaderboard.webp','Four-player leaderboard and bounty during Mags and Magic gameplay','The shared leaderboard and bounty shown during a recorded match.')
        body+='</section>'
    body+='</div>'
    if item.get('credits'): body+='<aside class="credits"><strong>Project credits and context</strong><p>'+escape(item['credits'])+'</p></aside>'
    render(slug+'.html',meta['title'],meta['summary'],body,image=meta.get('image','locomotion-keyart.webp'))


docs='<header class="page-heading"><h1>Design documents</h1><p>Samples of my game design and technical documentation.</p></header><div class="document-list">'
for title,file,thumb,description,note,project in [
('Locomotion — full game design document','locomotion-gdd.pdf','locomotion-gdd-cover.png','The full game design document covering the game concept, race systems, items, art direction, UI, controls, multiplayer, and project timeline.','23 pages.','locomotion'),
('Project: Hope — technical requirements','hope-technical-proposal.pdf','hope-technical-proposal.webp','My three-page proposal for device requirements, rendering scope, and initial performance targets.','October 29, 2026.','project-hope'),
('Revolution! — Game Design Document','revolution-gdd.pdf','revolution-gdd-cover.png','A historical-hero shooter concept covering scoring, character abilities, maps, UI, and multiplayer plans.','16 pages. Backfield Gaming.',None),
('Shift & Drift — Tutorial Level Design Document','shift-and-drift-level-design.pdf','shift-and-drift-cover.png','A driving tutorial plan covering low-grip handling, route choices, checkpoints, bumper-car combat, and momentum-based obstacles.','7 pages.',None),
('Shinden — Level Design Document','paper-design.pdf','paper-design-cover.png','An Overwatch-inspired deathmatch map concept exploring elevation, cover, sightlines, and a Japanese temple setting.','4 pages.',None),
('Position Weighted Item Boxes — Prototype Presentation','creative-brief.pdf','creative-brief-cover.png','A Mario Kart-inspired item-selection prototype explained through probability tables, Blueprint graphs, and implementation reflections.','11 pages.',None)]:
    project_link=link(project+'.html','Project details') if project else ''
    docs+=f'<article class="document-row"><a href="assets/docs/{file}" target="_blank" rel="noopener"><img src="assets/site/{thumb}" alt="Preview of {escape(title,quote=True)}" width="140" height="180" loading="lazy"></a><div><h2>{escape(title)}</h2><p>{description}</p><small>{note}</small><div class="resource-links">{link("assets/docs/"+file,"Open PDF",True)}{project_link}</div></div></article>'
docs+='</div>'
render('documents.html','Design Documents','Original game design and technical requirement samples by Connor Schaaf.',docs,'docs')

about=f'''<section class="about-layout"><img src="assets/site/headshot.webp" alt="Connor Schaaf" width="180" height="225"><div><h1>About me</h1>{introduction}<p>{escape(PROFILE['focus'])}</p><h2>Unreal Blueprints</h2><p>{escape(PROFILE['blueprints'])}</p><h2>Design documentation</h2><p>{escape(PROFILE['documentation'])}</p><p>{escape(PROFILE['contribution_statement'])}</p><h2>Contact me</h2><p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>'''
render('about.html','About','Connor Schaaf, a Purdue student focused on Unreal Blueprints and game design documentation.',about,'about','headshot.webp')

DIST=ROOT/'dist';DIST.mkdir(exist_ok=True)
pages=['index.html','documents.html','about.html']+[slug+'.html' for slug in PROJECTS]
for filename in pages:shutil.copy2(ROOT/filename,DIST/filename)
for folder in ['css','js','assets/site','assets/docs','assets/resume']:
    if (ROOT/folder).exists():shutil.copytree(ROOT/folder,DIST/folder,dirs_exist_ok=True)
shutil.copy2(ROOT/'assets/favicon.svg',DIST/'assets/favicon.svg')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
print(f'Built {len(pages)} portfolio pages.')
