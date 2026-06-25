import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a chave da API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Erro: Chave da API não encontrada! Crie um arquivo .env com GEMINI_API_KEY=sua_chave")

# Inicializa o cliente do Gemini
client = genai.Client(api_key=api_key)  

# Modelo que vamos usar (gratuito e rápido)
MODELO = "gemini-2.5-flash"  

def ler_descricoes():
    """Lê todos os arquivos .txt da pasta 'input/'"""
    pasta_input = Path("input")
    
    if not pasta_input.exists():
        print("❌ Pasta 'input/' não encontrada! Criando...")
        pasta_input.mkdir()
        return []
    
    arquivos = list(pasta_input.glob("*.txt"))
    
    if not arquivos:
        print("⚠️ Nenhum arquivo .txt encontrado em 'input/'")
        return []
    
    descricoes = []
    for arquivo in arquivos:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
            if conteudo:
                descricoes.append({
                    'nome': arquivo.stem,
                    'conteudo': conteudo
                })
    
    return descricoes

def gerar_gherkin(descricao):
    """Chama o Gemini para gerar Gherkin a partir de uma descrição"""
    
    prompt = f"""
Você é um especialista em testes e requisitos de software.

Com base na descrição da funcionalidade abaixo, gere cenários de teste no formato Gherkin.

REGRAS IMPORTANTES:
1. Use português para as palavras-chave: Funcionalidade, Cenário, Dado, Quando, Então, E, Mas
2. Sempre inclua: Funcionalidade, pelo menos 3 cenários (sucesso, erro e borda)
3. Use a estrutura correta com indentação (2 ou 4 espaços)
4. Seja específico e realista nos exemplos

DESCRIÇÃO DA FUNCIONALIDADE:
{descricao}

GEREN OS CENÁRIOS GHERKIN ABAIXO:
"""
    
    try:
        # Chamada para o Gemini 
        resposta = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.7,  # Controla a criatividade
                max_output_tokens=1024  # Tamanho máximo da resposta 
            )
        )
        
        # Pega o texto gerado
        gherkin_gerado = resposta.text
        
        return gherkin_gerado
        
    except Exception as e:
        print(f"❌ Erro ao chamar o Gemini: {e}")
        return None

def salvar_feature(nome_arquivo, conteudo_gherkin):
    """Salva o conteúdo Gherkin em um arquivo .feature na pasta 'output/'"""
    
    pasta_output = Path("output")
    
    if not pasta_output.exists():
        pasta_output.mkdir()
    
    caminho_arquivo = pasta_output / f"{nome_arquivo}.feature"
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo_gherkin)
    
    print(f"✅ Arquivo salvo: {caminho_arquivo}")
    return caminho_arquivo

def main():
    """Função principal que executa todo o fluxo"""
    
    print("🚀 Iniciando gerador de Gherkin com Gemini...")
    print("-" * 50)
    
    descricoes = ler_descricoes()
    
    if not descricoes:
        print("❌ Nenhuma descrição encontrada. Adicione arquivos .txt em 'entradas/'")
        return
    
    print(f"📄 Encontradas {len(descricoes)} descrição(ões)")
    print("-" * 50)
    
    resultados = []
    
    for idx, desc in enumerate(descricoes, 1):
        nome = desc['nome']
        conteudo = desc['conteudo']
        
        print(f"\n📝 Processando [{idx}/{len(descricoes)}]: {nome}")
        print(f"   Descrição: {conteudo[:100]}...")
        
        gherkin = gerar_gherkin(conteudo)
        
        if gherkin:
            caminho = salvar_feature(nome, gherkin)
            resultados.append({'nome': nome, 'status': 'sucesso', 'arquivo': caminho})
        else:
            resultados.append({'nome': nome, 'status': 'falha'})
    
    print("\n" + "=" * 50)
    print("📊 RESUMO FINAL")
    print("=" * 50)
    
    sucessos = [r for r in resultados if r['status'] == 'sucesso']
    falhas = [r for r in resultados if r['status'] == 'falha']
    
    print(f"✅ Sucessos: {len(sucessos)}")
    for r in sucessos:
        print(f"   - {r['nome']}.feature -> {r['arquivo']}")
    
    if falhas:
        print(f"❌ Falhas: {len(falhas)}")
        for r in falhas:
            print(f"   - {r['nome']}")
    
    print("\n🎯 Processo concluído!")

if __name__ == "__main__":
    main()