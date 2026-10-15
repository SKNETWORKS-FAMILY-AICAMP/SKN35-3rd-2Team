"""Small browser interactions; application state stays in Python."""
import streamlit as st

TECH_ICONS = {'LangChain': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A9E0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 .1l3-3a5 5 0 0 0-7-7l-2 2M14 11a5 5 0 0 0-7-.1l-3 3a5 5 0 0 0 7 7l2-2"/></svg>', 'LangGraph': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A9E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 6.5-5 10m8-10 5 10M7 19h10M12 7v6"/><circle cx="12" cy="4" r="3"/><circle cx="4" cy="19" r="3"/><circle cx="20" cy="19" r="3"/><circle cx="12" cy="14" r="2"/></svg>', 'MCP': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A9E0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 10 5-10 5L2 7l10-5ZM2 12l10 5 10-5M2 17l10 5 10-5"/></svg>'}


def tech_icon_uri(tech):
    """Use the reviewed technology marks in the existing muted gray."""
    from base64 import b64encode
    svg = TECH_ICONS[tech].replace("#00A9E0", "#64748B")
    return "data:image/svg+xml;base64," + b64encode(svg.encode()).decode()


_CARDS = st.components.v2.component(
    'codeclue_example_cards',
    html='<div class="cards" aria-label="예시 질문"></div>',
    css='''
    :host {font-family:Pretendard,"Malgun Gothic",sans-serif;color:#1E293B;}
    .cards {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:4px;}
    button {font:inherit;text-align:left;background:#fff;border:1px solid #E2E8F0;
      border-radius:16px;padding:20px;cursor:pointer;min-height:166px;transition:background .15s,border-color .15s,transform .15s;}
    button:hover {background:#FAFAFF;border-color:#A5B4FC;transform:translateY(-2px);}
    button:focus-visible {outline:3px solid #C7D2FE;outline-offset:2px;}
    .tech {display:flex;justify-content:space-between;color:#4F46E5;font-size:12px;margin-bottom:14px;}
    .tech {align-items:center;}
    .tech-label {display:inline-flex;align-items:center;gap:8px;}
    .tech-label img {width:24px;height:24px;}
    strong {display:block;font-size:14px;line-height:1.5;margin-bottom:8px;}
    p {font-size:12px;line-height:1.7;color:#64748B;margin:0;}
    @media(max-width:600px) {.cards {grid-template-columns:1fr;} button {min-height:120px;}}
    @media(prefers-reduced-motion:reduce) {button {transition:none;}}
    ''',
    js='''export default function({parentElement,data,setTriggerValue}) {
      const grid=parentElement.querySelector('.cards');grid.replaceChildren();
      data.forEach((item,index)=>{
        const button=document.createElement('button');button.type='button';
        const tech=document.createElement('span');tech.className='tech';
        const label=document.createElement('span');label.className='tech-label';
        const mark=document.createElement('img');mark.src=item[3];mark.alt='';
        const name=document.createElement('span');name.textContent=item[0];
        label.append(mark,name);
        const arrow=document.createElement('span');arrow.textContent='↗';arrow.setAttribute('aria-hidden','true');
        tech.append(label,arrow);
        const title=document.createElement('strong');title.textContent=item[1];
        const description=document.createElement('p');description.textContent=item[2];
        button.append(tech,title,description);button.onclick=()=>setTriggerValue('selected',index);
        grid.append(button);
      });
    }''',
)

_COPY = st.components.v2.component(
    'codeclue_copy_answer',
    html='<button type="button" aria-label="답변 복사">⧉ 답변 복사</button><span role="status" aria-live="polite"></span>',
    css='''
    button {font-family:Pretendard,"Malgun Gothic",sans-serif;font-size:12px;color:#64748B;
      background:transparent;border:1px solid transparent;border-radius:8px;padding:7px 10px;cursor:pointer;}
    button:hover {background:#EEF2FF;color:#4F46E5;}
    button:focus-visible {outline:2px solid #4F46E5;outline-offset:2px;}
    span {font-size:12px;color:#64748B;}
    ''',
    js='''export default function({parentElement,data}) {
      const button=parentElement.querySelector('button'),status=parentElement.querySelector('span');
      let timer;
      button.onclick=async()=>{
        try {
          await navigator.clipboard.writeText(data.text);
          button.textContent='✓ 복사됨';status.textContent='';
        } catch(error) {
          const field=document.createElement('textarea');field.value=data.text;
          field.style.position='fixed';field.style.opacity='0';parentElement.append(field);field.select();
          const copied=document.execCommand('copy');field.remove();
          button.textContent=copied?'✓ 복사됨':'⧉ 답변 복사';
          status.textContent=copied?'':'복사를 허용하거나 답변을 선택해 복사해 주세요.';
        }
        clearTimeout(timer);timer=setTimeout(()=>button.textContent='⧉ 답변 복사',1800);
      };
      return ()=>clearTimeout(timer);
    }''',
)

def example_cards(examples, *, on_selected_change):
    return _CARDS(data=[[*item[:3], tech_icon_uri(item[0])] for item in examples], key='welcome_cards',
                  on_selected_change=on_selected_change)

def copy_answer(text, *, key):
    return _COPY(data={'text':text}, key=key)
