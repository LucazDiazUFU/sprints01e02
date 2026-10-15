const tipos={1:"Notebook",2:"Servidor",3:"Roteador",4:"Aplicação web",5:"Banco de dados",6:"Estação de trabalho"};
const campo=id=>document.getElementById(id);
let ativos=[];
let id_edicao=null;
let id_ativo=null;
let id_vulnerabilidade=null;

async function requisitar(caminho,opcoes={}){
  const controle=new AbortController();
  const tempo=setTimeout(()=>controle.abort(),10000);
  const headers={Accept:"application/json",...(opcoes.body?{"Content-Type":"application/json"}:{})};
  if(campo("token").value)headers["X-Token"]=campo("token").value;
  try{
    const resposta=await fetch(caminho,{...opcoes,headers,signal:controle.signal});
    const dados=resposta.status===204?null:await resposta.json();
    if(!resposta.ok)throw new Error(dados?.erro||"Não foi possível concluir a operação.");
    return dados;
  }catch(erro){
    if(erro.name==="AbortError")throw new Error("A resposta demorou. Tente novamente.");
    if(erro instanceof TypeError)throw new Error("Não foi possível conectar. Confira se o programa está em execução.");
    throw erro;
  }finally{clearTimeout(tempo);}
}

function avisar(texto){campo("mensagem").textContent=texto;}
function elemento(tipo,texto,classe){const item=document.createElement(tipo);if(texto!==undefined)item.textContent=texto;if(classe)item.className=classe;return item;}
function botao(texto,acao,id){const item=elemento("button",texto);item.type="button";item.dataset.acao=acao;item.dataset.id=id;return item;}

function renderizar(){
  const busca=campo("busca").value.trim().toLocaleLowerCase("pt-BR");
  const tipo=campo("filtro-tipo").value;
  const status=campo("filtro-status").value;
  const filtrados=ativos.filter(ativo=>(!busca||ativo.nome.toLocaleLowerCase("pt-BR").includes(busca))&&(!tipo||ativo.tipo===Number(tipo))&&(!status||ativo.status===status));
  campo("linhas-ativos").replaceChildren(...filtrados.map(ativo=>{
    const linha=elemento("tr");
    const nome=elemento("td");nome.append(elemento("strong",ativo.nome),elemento("span",`ID ${ativo.id}`));
    const responsavel=elemento("td");responsavel.append(elemento("strong",ativo.responsavel),elemento("span",ativo.setor));
    const situacao=elemento("td");situacao.append(elemento("span",ativo.status.replaceAll("_"," "),"etiqueta"));
    const acoes=elemento("td");const grupo=elemento("div",undefined,"acoes");
    grupo.append(botao("Vulnerabilidades","vulnerabilidades",ativo.id),botao("Editar","editar",ativo.id),botao("Excluir","excluir",ativo.id));acoes.append(grupo);
    linha.append(nome,elemento("td",tipos[ativo.tipo]),responsavel,situacao,acoes);return linha;
  }));
  campo("vazio").hidden=filtrados.length>0;
  campo("total-ativos").textContent=ativos.length;
  campo("total-vulnerabilidades").textContent=ativos.reduce((total,ativo)=>total+ativo.vulnerabilidades.length,0);
  campo("total-manutencao").textContent=ativos.filter(ativo=>ativo.status==="MANUTENCAO").length;
  preencherDependencias();
}

async function carregar(){ativos=await requisitar("/api/ativos");renderizar();}

function abrirAtivo(ativo=null){
  campo("form-ativo").reset();id_edicao=ativo?.id??null;
  campo("titulo-ativo").textContent=ativo?"Editar ativo":"Novo ativo";
  campo("erro-ativo").textContent="";campo("id-ativo").disabled=Boolean(ativo);
  const ids={id:"id-ativo",nome:"nome",responsavel:"responsavel",setor:"setor",tipo:"tipo",status:"status",criticidade:"criticidade",descricao:"descricao-ativo"};
  if(ativo)for(const [nome,id]of Object.entries(ids))campo(id).value=ativo[nome];
  campo("dialog-ativo").showModal();
}

campo("form-ativo").addEventListener("submit",async evento=>{
  evento.preventDefault();const submit=evento.submitter;submit.disabled=true;
  const dados={nome:campo("nome").value.trim(),responsavel:campo("responsavel").value.trim(),setor:campo("setor").value.trim(),tipo:Number(campo("tipo").value),status:campo("status").value,criticidade:campo("criticidade").value,descricao:campo("descricao-ativo").value.trim()};
  if(id_edicao===null)dados.id=Number(campo("id-ativo").value);
  try{await requisitar(id_edicao===null?"/api/ativos":`/api/ativos/${id_edicao}`,{method:id_edicao===null?"POST":"PATCH",body:JSON.stringify(dados)});campo("dialog-ativo").close();await carregar();avisar("Ativo salvo.");}catch(erro){campo("erro-ativo").textContent=erro.message;}finally{submit.disabled=false;}
});

campo("linhas-ativos").addEventListener("click",async evento=>{
  const item=evento.target.closest("button[data-acao]");if(!item)return;
  const ativo=ativos.find(ativo=>ativo.id===Number(item.dataset.id));if(!ativo)return;
  try{
    if(item.dataset.acao==="editar")abrirAtivo(ativo);
    if(item.dataset.acao==="vulnerabilidades")await abrirVulnerabilidades(ativo);
    if(item.dataset.acao==="excluir"&&confirm(`Excluir ${ativo.nome} e suas vulnerabilidades?`)){
      await requisitar(`/api/ativos/${ativo.id}`,{method:"DELETE",body:JSON.stringify({confirmar:true})});await carregar();avisar("Ativo excluído.");
    }
  }catch(erro){avisar(erro.message);}
});

function limparVulnerabilidade(){campo("form-vulnerabilidade").reset();id_vulnerabilidade=null;campo("id-vulnerabilidade").disabled=false;campo("titulo-form-vulnerabilidade").textContent="Cadastrar vulnerabilidade";campo("erro-vulnerabilidade").textContent="";}

async function atualizarVulnerabilidades(){
  const itens=await requisitar(`/api/ativos/${id_ativo}/vulnerabilidades`);
  campo("lista-vulnerabilidades").replaceChildren(...itens.map(item=>{
    const linha=elemento("li");linha.append(elemento("strong",`${item.id} - ${item.descricao}`),elemento("p",`${item.severidade} | ${item.status.replaceAll("_"," ")}`),botao("Editar","editar",item.id),botao("Excluir","excluir",item.id));return linha;
  }));
  if(!itens.length)campo("lista-vulnerabilidades").append(elemento("li","Este ativo não possui vulnerabilidades registradas."));
}

async function abrirVulnerabilidades(ativo){id_ativo=ativo.id;limparVulnerabilidade();campo("titulo-vulnerabilidades").textContent=`Vulnerabilidades - ${ativo.nome}`;await atualizarVulnerabilidades();campo("dialog-vulnerabilidades").showModal();}

campo("form-vulnerabilidade").addEventListener("submit",async evento=>{
  evento.preventDefault();const submit=evento.submitter;submit.disabled=true;
  const dados={descricao:campo("descricao").value.trim(),categoria:campo("categoria").value.trim(),severidade:campo("severidade").value,status:campo("status-vulnerabilidade").value,cve:campo("cve").value.trim(),cvss:campo("cvss").value===""?null:Number(campo("cvss").value),referencia:campo("referencia").value.trim(),recomendacao:campo("recomendacao").value.trim()};
  if(id_vulnerabilidade===null)dados.id=Number(campo("id-vulnerabilidade").value);
  try{await requisitar(id_vulnerabilidade===null?`/api/ativos/${id_ativo}/vulnerabilidades`:`/api/vulnerabilidades/${id_vulnerabilidade}`,{method:id_vulnerabilidade===null?"POST":"PATCH",body:JSON.stringify(dados)});limparVulnerabilidade();await atualizarVulnerabilidades();await carregar();avisar("Vulnerabilidade salva.");}catch(erro){campo("erro-vulnerabilidade").textContent=erro.message;}finally{submit.disabled=false;}
});

campo("lista-vulnerabilidades").addEventListener("click",async evento=>{
  const item=evento.target.closest("button[data-acao]");if(!item)return;
  try{
    if(item.dataset.acao==="excluir"&&confirm("Excluir esta vulnerabilidade?")){await requisitar(`/api/vulnerabilidades/${item.dataset.id}`,{method:"DELETE",body:JSON.stringify({confirmar:true})});await atualizarVulnerabilidades();await carregar();}
    if(item.dataset.acao==="editar"){
      const dados=await requisitar(`/api/vulnerabilidades/${item.dataset.id}`);id_vulnerabilidade=dados.id;campo("id-vulnerabilidade").value=dados.id;campo("id-vulnerabilidade").disabled=true;
      for(const nome of["descricao","categoria","severidade","cve","cvss","referencia","recomendacao"])campo(nome).value=dados[nome]??"";
      campo("status-vulnerabilidade").value=dados.status;campo("titulo-form-vulnerabilidade").textContent="Editar vulnerabilidade";campo("descricao").focus();
    }
  }catch(erro){campo("erro-vulnerabilidade").textContent=erro.message;}
});

function preencherDependencias(){
  const origem=campo("origem").value;
  campo("origem").replaceChildren(...ativos.map(ativo=>{const option=elemento("option",`${ativo.id} - ${ativo.nome}`);option.value=ativo.id;return option;}));
  if(ativos.some(ativo=>String(ativo.id)===origem))campo("origem").value=origem;
  atualizarDestinos();
}

function atualizarDestinos(){
  const origem=Number(campo("origem").value);const ativo=ativos.find(item=>item.id===origem);
  campo("destino").replaceChildren(...ativos.filter(item=>item.id!==origem).map(item=>{const option=elemento("option",`${item.id} - ${item.nome}`);option.value=item.id;return option;}));
  campo("dependencias").replaceChildren(...Object.entries(ativo?.dependencias??{}).map(([id,peso])=>{const linha=elemento("li",`Depende de ${id}; fração ${peso}. `);linha.append(botao("Remover","remover",id));return linha;}));
}

campo("form-dependencia").addEventListener("submit",async evento=>{
  evento.preventDefault();try{await requisitar(`/api/ativos/${campo("origem").value}/dependencias/${campo("destino").value}`,{method:"PUT",body:JSON.stringify({peso:Number(campo("peso").value)})});await carregar();await carregarRiscos();avisar("Dependência salva.");}catch(erro){avisar(erro.message);}
});
campo("dependencias").addEventListener("click",async evento=>{const item=evento.target.closest("button");if(!item)return;try{await requisitar(`/api/ativos/${campo("origem").value}/dependencias/${item.dataset.id}`,{method:"DELETE"});await carregar();await carregarRiscos();avisar("Dependência removida.");}catch(erro){avisar(erro.message);}});

async function carregarRiscos(){
  const dados=await requisitar(`/api/riscos?ponderar=${campo("ponderar").checked}`);
  campo("linhas-riscos").replaceChildren(...dados.ativos.map(ativo=>{const linha=elemento("tr");linha.append(elemento("td",`${ativo.id} - ${ativo.nome}`),elemento("td",ativo.risco_proprio.toFixed(4)),elemento("td",ativo.risco_efetivo.toFixed(4)));return linha;}));
  campo("precisao").textContent=dados.aviso||`Cálculo concluído. Resíduo numérico: ${dados.residuo.toExponential(2)}.`;
}

document.querySelectorAll("[data-pagina]").forEach(item=>item.addEventListener("click",async()=>{
  const risco=item.dataset.pagina==="riscos";
  campo("pagina-ativos").hidden=risco;campo("pagina-riscos").hidden=!risco;campo("novo-ativo").hidden=risco;
  document.querySelector("h1").textContent=risco?"Análise de risco":"Ativos de TI";
  document.querySelectorAll("[data-pagina]").forEach(botao=>{botao.classList.toggle("selecionado",botao===item);if(botao===item)botao.setAttribute("aria-current","page");else botao.removeAttribute("aria-current");});
  if(risco)try{await carregarRiscos();}catch(erro){avisar(erro.message);}
}));
document.querySelectorAll("[data-fechar]").forEach(item=>item.addEventListener("click",()=>campo(item.dataset.fechar).close()));
campo("novo-ativo").addEventListener("click",()=>abrirAtivo());
campo("limpar-vulnerabilidade").addEventListener("click",limparVulnerabilidade);
campo("origem").addEventListener("change",atualizarDestinos);
for(const id of["busca","filtro-tipo","filtro-status"])campo(id).addEventListener("input",renderizar);
campo("recarregar").addEventListener("click",()=>carregar().then(()=>avisar("Lista atualizada.")).catch(erro=>avisar(erro.message)));
for(const id of["recalcular","ponderar"])campo(id).addEventListener(id==="ponderar"?"change":"click",()=>carregarRiscos().catch(erro=>avisar(erro.message)));
carregar().catch(erro=>avisar(erro.message));
