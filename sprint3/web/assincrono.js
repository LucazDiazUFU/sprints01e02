function comCallback(callback){setTimeout(()=>callback("Operação concluída"),50);}
function comPromise(){return new Promise(resolve=>comCallback(resolve));}

async function consultar(url){
  const situacao=document.getElementById("situacao");
  const resultado=document.getElementById("resultado");
  const controle=new AbortController();const limite=setTimeout(()=>controle.abort(),10000);
  situacao.textContent="Consultando...";resultado.textContent="";
  try{
    await comPromise();
    const resposta=await fetch(url,{signal:controle.signal});
    if(!resposta.ok)throw new Error(`A consulta retornou HTTP ${resposta.status}.`);
    const dados=await resposta.json();
    resultado.textContent=JSON.stringify(dados,null,2);situacao.textContent="Consulta concluída.";
  }catch(erro){situacao.textContent=erro.name==="AbortError"?"A consulta excedeu o tempo de espera.":erro.message;}
  finally{clearTimeout(limite);}
}
document.getElementById("consultar-ativos").addEventListener("click",()=>consultar("/api/ativos"));
document.getElementById("consultar-publica").addEventListener("click",()=>consultar("https://servicodados.ibge.gov.br/api/v1/localidades/municipios/3170206"));
