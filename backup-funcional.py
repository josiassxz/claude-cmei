from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware

def read_api_key() -> str:
    """Lê a API key do arquivo key.txt na raiz do projeto"""
    try:
        with open('key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Arquivo key.txt não encontrado na raiz do projeto")
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo key.txt: {str(e)}")

app = FastAPI(
    title="Legal Petition Generator API",
    description="API for generating legal petitions using Claude 3 ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PetitionRequest(BaseModel):
    prompt: str
    child_name: str
    child_birth_date: str
    child_cpf: str
    mother_name: str
    mother_qualification: str
    mother_address: str
    mother_phone: str
    mother_email: str
    cmei_name: str

class PetitionResponse(BaseModel):
    petition: str
    stop_reason: str | None
    usage: dict | None
    


PETITION_TEMPLATE = """**AO JUIZADO DA INFÂNCIA E DA JUVENTUDE DA COMARCA DE GOIÂNIA -- GOIÁS**

**{child_name}, nascida em {child_birth_date}, inscrita no CPF sob o n° {child_cpf},** representada por sua genitora, **{mother_name}**, {mother_qualification}, endereço eletrônico {mother_email}, residente e domiciliada na {mother_address}, telefone/WhatsApp {mother_phone}, por intermédio da **DEFENSORIA PÚBLICA DO ESTADO DE GOIÁS**, vem, ajuizar

**AÇÃO DE OBRIGAÇÃO DE FAZER C/ DANOS MORAIS E PEDIDO DE TUTELA PROVISÓRIA DE URGÊNCIA**

em face do **MUNICÍPIO DE GOIÂNIA**, pessoa jurídica de direito público interno, inscrita no CNPJ sob o nº 01.612.092/0001-23, com sede na Avenida do Cerrado, nº 999, Park Lozandes, Goiânia-GO, CEP 74884-092, pelos fundamentos de fato e de direito a seguir expostos.

**1) DA GRATUIDADE DE JUSTIÇA**

A representante legal da autora afirma para os fins dos arts. 98 e seguintes do CPC, que não possui recursos suficientes para arcar com as custas do processo e honorários de advogado, sem prejuízo de seu próprio sustento e de sua família, pelo que indica para assistência judiciária a Defensoria Pública do Estado.

**2) DAS PRERROGATIVAS DOS MEMBROS DA DEFENSORIA PÚBLICA**

Conforme artigo 157, incisos I e IX, da LCE nº 130/2017, são prerrogativas dos Defensores Públicos Estaduais receber, inclusive quando necessário, mediante entrega dos autos com vista, intimação pessoal em qualquer processo e grau de jurisdição ou instância administrativa, contando-se-lhes em dobro todos os prazos, bem como representar a parte, em feito judicial, independentemente de mandato.

**3) DOS FATOS**

{facts}

**4) DO DIREITO**

O acesso à educação, caracterizado como um direito de todos e dever do Estado, é plenamente amparado pela Carta Magna. Tal direito social encontra especial proteção quando envolve crianças, já que são pessoas em desenvolvimento, que precisam do adequado preparo para o exercício da cidadania e qualificação para o trabalho, conforme artigo 53 e seguintes do Estatuto da Criança e do Adolescente. A propósito, a Lei nº 13.257/2016, que dispõe sobre **as políticas públicas para a primeira infância**, reforça a prioridade absoluta que os infantes possuem, determinando a expansão da educação infantil, a qual deverá ser feita de maneira a assegurar a qualidade da oferta (art. 16).

A Lei nº 9.394/96 (Lei de Diretrizes e Bases da Educação Nacional), por sua vez, estabeleceu no artigo 4º, inciso I, que o dever do Estado com a educação escolar pública será efetivado mediante a garantia de educação às crianças e adolescentes entre 04 (quatro) e 17 (dezessete) anos de idade, organizada entre pré escola, ensino fundamental e ensino médio.

Oportuno ressaltar que a garantia da absoluta prioridade prevista na Constituição da República de 1988 (art. 227) e no artigo 4º da Lei nº 8.069/90 compreende a preferência na formulação e na execução das políticas sociais públicas e a destinação privilegiada de recursos públicos nas áreas relacionadas com a proteção à infância e à juventude.

A jurisprudência pátria é uníssona ao aplicar o ativismo judicial quando há omissão do ente federativo, vejamos:

> APELAÇÃO CÍVEL. ECA. DIREITO À EDUCAÇÃO. FORNECIMENTO DE VAGA EM ESTABELECIMENTO DE ENSINO INFANTIL. TURNO INTEGRAL. **O fornecimento de vaga em estabelecimento de ensino infantil em turno integral é decorrência dos princípios constitucionais de proteção e desenvolvimento da infância, e deve ser assegurado às crianças, em especial as oriundas de famílias com poucas condições financeiras.** DERAM PROVIMENTO. UNÂNIME. (Apelação Cível Nº 70076079284, Oitava Câmara Cível, Tribunal de Justiça do RS, Relator: Luiz Felipe Brasil Santos, Julgado em 08/02/2018).

> REMESSA NECESSÁRIA. MANDADO DE SEGURANÇA. MATRÍCULA EM CMEI. EDUCAÇÃO INFANTIL. NECESSIDADE. OBRIGAÇÃO DE FAZER. DIREITO LÍQUIDO E CERTO COMPROVADO. 1. Nos termos da disposição contida no artigo 208 da Constituição Federal e no artigo 54, inciso IV, do Estatuto da Criança e do Adolescente, é dever do ente público municipal assegurar ao menor vaga em creche ou pré-escola, tendo em vista tratar-se de direito fundamental. 2. Incontestável o direito do menor, nos moldes pleiteados na ação mandamental, vez que devidamente amparado em preceitos constitucionais, cabendo ao Poder Público adotar medidas concretas, para viabilizar o atendimento educacional, independentemente de se provocar a jurisdição. 3. REMESSA NECESSÁRIA CONHECIDA E DESPROVIDA. (TJGO, Duplo Grau de Jurisdição, Processo nº 103852-33.2015.8.09.0052, 3ª Câmara Cível, Relator Des. Gerson Cintra Santana, Publicado em 20/03/17).

**5) DA VAGA EM ESCOLA PRÓXIMA A RESIDÊNCIA DA AUTORA**

O direito à educação não se limita à matrícula e frequência em creche ou escola, pois abrange também o **direito de estudar próximo de sua residência**. Tal direito encontra previsão expressa no ECA e na LDB:

Lei nº 8.069/1990.

> Art. 53. A criança e o adolescente têm direito à educação, visando ao pleno desenvolvimento de sua pessoa, preparo para o exercício da cidadania e qualificação para o trabalho, assegurando-se-lhes:
> 
> (...)V -- acesso à escola pública e gratuita, **próxima de sua residência**, garantindo-se vagas no mesmo estabelecimento a irmãos que frequentem a mesma etapa ou ciclo de ensino da educação básica. (Redação dada pela Lei nº 13.845, de 2019)
> 
> Lei nº 9.394/1996.
> 
> Art. 4º O dever do Estado com educação escolar pública será efetivado mediante a garantia de:
> 
> (...) X -- vaga na escola pública de educação infantil ou de ensino fundamental **mais próxima de sua residência** a toda criança a partir do dia em que completar 4 (quatro) anos de idade.

**6) DA INDENIZAÇÃO POR DANOS MORAIS**

No julgamento do Recurso Extraordinário (RE) 1008166, o plenário do Supremo Tribunal Federal avançou na fixação do **Tema 548 de repercussão geral,** definindo a seguinte tese:

> 1 - A educação básica em todas as suas fases, educação infantil, ensino fundamental e ensino médio, constitui direito fundamental de todas as crianças e jovens, assegurado por normas constitucionais de eficácia plena e aplicabilidade direta e imediata.
> 
> 2 - A educação infantil compreende creche, de 0 a 3 anos, e a pré-escola, de 4 a 5 anos. Sua oferta pelo poder público pode ser exigida individualmente, como no caso examinado neste processo.
> 
> 3 - O poder público tem o dever jurídico de dar efetividade integral às normas constitucionais sobre acesso à educação básica

Conforme restou reconhecido, a educação infantil é direito público subjetivo da criança, ao qual corresponde ao poder público o dever jurídico de dar efetividade integral às normas constitucionais sobre acesso à educação básica.

Assim, como é cediço, a responsabilidade civil do Estado consiste na obrigação de responder inclusive pelos danos causados por ação ou omissão de seus agentes (CF, art. 37, §6º). Em se tratando de preceito normativo autoaplicável, uma vez ocorrido o dano e estabelecido o nexo causal com a atuação da Administração ou dos seus agentes, exsurge a responsabilidade civil do Estado.

Especificamente em relação ao resultado da omissão estatal, ressalta-se ter o dano moral previsão constitucional (CF, art. 5º, V e X). De igual forma, o Código Civil de 2002 refere-se explicitamente ao dano moral: "Aquele que por ação ou omissão voluntária, negligência ou imprudência, violar direito e causar dano a outrem, ainda que exclusivamente moral, comete ato ilícito" (art. 186).

Presente esse contexto, sendo evidente o reconhecimento da responsabilidade civil do Estado, inclusive por danos morais, decorrente da insuficiência da oferta da educação obrigatória, consubstanciada na negativa de acesso ao sistema público de ensino, requer-se a condenação do requerido ao pagamento de indenização por danos morais à requerente no valor de R$10.000,00 (dez mil reais).

**7) DA TUTELA PROVISÓRIA DE URGÊNCIA**

No caso em epígrafe, conforme narrativa acima exposta, faz-se necessário, para fins de adequada prestação da tutela jurisdicional, a concessão de tutela provisória de urgência, com fulcro no art. 300 do CPC c/c art. 213, §1º, da lei nº 8.069/90.

A **probabilidade do direito** se comprova pelo documento impresso indicando a impossibilidade de matrícula da criança na escola pleiteada, indicando a situação da matrícula no CMEI como "Aguardando Vaga". O **perigo de dano ou o risco ao resultado útil do processo** decorre de que o ano letivo não pode ser prejudicado por uma nefasta omissão governamental. Se a Carta Magna e leis infraconstitucionais asseguram o direito subjetivo público à educação, o qual sequer pode ser relativizado pela cláusula da reserva do possível, aguardar o deslinde da ação judicial é perpetuar uma situação de inconstitucionalidade.

**8) DOS PEDIDOS**

Face o exposto requer:

a) A concessão do benefício da gratuidade de justiça, extensível a eventuais emolumentos cartorários;
 
b) A intimação pessoal, mediante entrega dos autos com vista e a contagem em dobro de todos os prazos, manifestação por cota e dispensa de mandato, nos termos do art. 157, incisos I e IX, da LCE nº 130/2017;
 
c) A prioridade na tramitação do processo, em atendimento ao 227 da CRFB/88 e ao art. 4º da Lei nº 8.069/90 -- ECA;

d) A concessão, em sede de tutela provisória de urgência, de mandado judicial determinando a imediata matrícula da criança, **em período integral**, no **{cmei_name}** ou instituição próxima a sua residência, sob pena de multa diária;

e) Subsidiariamente, caso não ocorra a disponibilização de vagas na(s) unidade(s) de ensino da rede pública indicada(s), requer seja concedido prazo para que a parte Autora apresente orçamento(s) de creche(s)/escola(s) particular(es), a fim de que seja realizado **bloqueio de verba pública** suficiente para a concretização do direito à educação na rede particular de ensino, o que desde já se requer;

f) A citação da parte ré;

g) A intimação do Ministério Público do Estado de Goiás;
 
h) No mérito:
 
h.1) A procedência do pedido em todos os seus termos, para conceder-se a garantia constitucional pleiteada, confirmando-se a liminar requerida e determinando que o Requerido promova a matrícula da infante na rede pública de ensino mais próxima à sua residência, em período integral, atualmente um dos CMEI's solicitados, sob pena de multa diária;

h.2) subsidiariamente, caso não ocorra a disponibilização de vagas na(s) unidade(s) de ensino da rede pública indicada(s), requer **bloqueio de verba pública para que o Requerido arque com todos os custos necessários ao pagamento da matrícula, mensalidade e manutenção da(s) criança(s) em instituição particular de ensino,** conforme solicitado na alínea "e" acima;
> 
h.3) A condenação do requerido ao pagamento de dano moral, de caráter punitivo e pedagógico, com acréscimo de juros e correção monetária, na forma da lei, ante a conduta omissiva estatal no fornecimento da vaga, no montante de R$10.000,00 (dez mil reais);
 
i) A condenação da parte demandada aos ônus da sucumbência, arbitrando-se honorários, no percentual de 20%, a serem revertidos ao Fundo da Defensoria Pública Estadual-FUNDEPEG, Caixa Econômica Federal, Agência 4204, Conta 00001446-9, operação 006, CNPJ 16628259/0001-11.

Dá-se à presente causa o valor de **R$ 17.880,42 (valor estimado de gasto anual por aluno, conforme Portaria Interministerial nº 07, de 29 de dezembro de 2022, publicada no D.O.U. em 29/12/2023, Edição nº 247-E, Seção 1 e dano moral).**

Nesses termos,
Solicita deferimento.

Goiânia, 30 de setembro de 2024.

**{defender_name}**
**Defensora Pública do Estado de Goiás**"""



class LegalPetitionGenerator:
    def __init__(self, api_key: str | None = None):
        try:
            self.client = anthropic.Anthropic(
                api_key=api_key or read_api_key()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize Anthropic client: {str(e)}")

    def generate_facts(self, prompt: str, cmei_name: str) -> str:
        """Gera apenas a seção dos fatos usando a IA"""
        try:
            system_message = """Você deve gerar apenas a seção de FATOS para uma petição judicial de vaga em CMEI. 
            A seção deve conter:
            1. Não pode faltar! Data do cadastro no padrao xxxx-xxx para ser preenchido
            2. Não pode faltar! Nome do CMEI solicitado q é {cmei_name} e seu Endereço {cmei_address}
            3. Situação da matrícula (sempre aguardando vaga)
            4. Situação específica familiar que justifica a necessidade da vaga
            5. Menção à impossibilidade financeira de pagar escola particular
            
            
            Importante:
            - Traga uma resposta o mais completa possivel que possa deixar os fatos mais explicativos possivel de forma juridica
            - Use linguagem formal e jurídica
            - Mencione explicitamente que foi negada a vaga e a criança está em lista de espera
            - Inclua uma conclusão mencionando que não houve alternativa além da via judicial
            - NÃO inclua nenhuma fundamentação legal ou jurisprudência
            - Foque apenas nos fatos concretos do caso"""

            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                # model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.7,
                system=system_message,
                messages=[
                    {
                        "role": "user",
                        "content": f"Gere a seção de fatos para uma petição de vaga em CMEI usando estas informações: {prompt}"
                    }
                ]
            )

            if hasattr(response, 'content') and response.content:
                content = response.content[0].text if isinstance(response.content, list) else response.content
                return content, response.stop_reason, self.convert_usage_to_dict(response.usage)
            else:
                raise HTTPException(status_code=500, detail="Empty response from Claude")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating facts: {str(e)}")

    def convert_usage_to_dict(self, usage) -> dict:
        """Converte o objeto Usage para um dicionário"""
        return {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens
        }

    async def gerar_peticao(self, request: PetitionRequest) -> tuple[str, str, dict]:
        try:
            # Gera apenas a seção dos fatos
            facts, stop_reason, usage = self.generate_facts(request.prompt, request.cmei_name)
            
            # Monta a petição completa usando o template
            petition = PETITION_TEMPLATE.format(
                child_name=request.child_name,
                child_birth_date=request.child_birth_date,
                child_cpf=request.child_cpf,
                mother_name=request.mother_name,
                mother_qualification=request.mother_qualification,
                mother_email=request.mother_email,
                mother_address=request.mother_address,
                mother_phone=request.mother_phone,
                cmei_name=request.cmei_name,
                facts=facts,
                defender_name="Teste Josias" 
            )
            
            return petition, stop_reason, usage

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating petition: {str(e)}")

generator = LegalPetitionGenerator()

@app.post("/generate-petition", response_model=PetitionResponse, tags=["Petition"])
async def generate_petition(request: PetitionRequest):
    """
    Generate a legal petition based on the provided data.
    
    The petition will follow a fixed template, with only the facts section being generated by AI.
    All other sections remain constant, with variables being filled from the request data.
    """
    if len(request.prompt) < 20:
        raise HTTPException(status_code=400, detail="Prompt must be at least 20 characters long")
    
    try:
        petition, stop_reason, usage = await generator.gerar_peticao(request)
        return PetitionResponse(
            petition=petition,
            stop_reason=stop_reason,
            usage=usage
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the Legal Petition Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)