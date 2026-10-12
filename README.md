# NieR:Automata – Revisão da tradução pt-BR

Patch de revisão para a tradução em português do Brasil de **NieR:Automata – Game of the YoRHa Edition** (Steam) feita pela equipe **[Tribo Gamer Brasil](https://tribogamer.com/traducoes/486_traducao-do-nier-automata-game-of-the-yorha-edition-para-portugues-do-brasil.html)**.

A tradução da Tribo é a base de tudo aqui. Este projeto **não é uma tradução nova**: é uma revisão contextual que corrige sentido, gramática e consistência de termos sobre o trabalho deles.

> ⚠️ Este repositório **não contém arquivos do jogo nem da tradução da Tribo**. O patch só funciona sobre uma instalação do jogo original com a tradução da Tribo Gamer v1.00 já aplicada.

## O que a revisão corrige

Cerca de 4.200 textos em 211 arquivos:

| Área | Correções |
|---|---|
| Falas e diálogos (cenas, missões, NPCs) | 2.675 |
| Textos de missões, inimigos, arquivos e itens | 919 |
| Interface (menus, HUD, créditos) | 400 |
| Legendas de cenas | 187 |
| Novels visuais (Devola e Popola, Anemone, Adam, 9S, Plato) | 81 trechos |

Exemplos do que mudou:

- **Erros de sentido:** o servidor sob o Monte Ka'ala era "humano" em vez de "inimigo"; "Nines" virava "Nove"; *toothbrush* virava "pasta de dente"; *port* virava "portaria".
- **Consistência de termos:** YoRHa sempre no masculino ("do YoRHa"), "aldeia do Pascal", "invasão/invadir" na interface, "chip de ampliação", "Plato 1728", "descida". Veja o [GLOSSARIO.md](GLOSSARIO.md).
- **Português:** crase, concordância, hífens, números no formato brasileiro, aspas e trechos que estavam faltando.
- **Mod WAX:** o WAX substitui o script da "Mulher Estranha" do acampamento por uma cópia própria em inglês. O instalador gera a versão traduzida dela (veja abaixo).

## Requisitos

1. **NieR:Automata – Game of the YoRHa Edition** (Steam), original.
2. **Tradução da Tribo Gamer Brasil v1.00** (09/02/2023) instalada na pasta `data` do jogo.

O instalador confere cada arquivo antes de alterar qualquer coisa. Se algum arquivo não for exatamente o da Tribo v1.00, nada é modificado.

## Instalação

1. Baixe o `.zip` mais recente em [Releases](../../releases).
2. Extraia o `AplicarPatch-NieR-PTBR.exe` **na pasta do jogo** (onde fica o `NieRAutomata.exe`). Exemplo: `C:\Program Files (x86)\Steam\steamapps\common\NieRAutomata`.
3. Execute o `AplicarPatch-NieR-PTBR.exe`.

O instalador:

- confere se a tradução da Tribo v1.00 está instalada;
- guarda uma cópia dos arquivos originais em `data\_backup_revisao_ptbr`;
- aplica as correções;
- se você usa o mod **WAX**, gera o script traduzido da "Mulher Estranha" em `wax\mods\TraducaoPTBR\overrides`.

Pela linha de comando também dá para informar a pasta do jogo e usar opções:

```
AplicarPatch-NieR-PTBR.exe "C:\caminho\do\NieRAutomata" [--verificar] [--restaurar] [--sem-wax]
```

| Opção | O que faz |
|---|---|
| `--verificar` | Só confere os arquivos (originais da Tribo, já corrigidos ou diferentes), sem alterar nada. |
| `--restaurar` | Desfaz o patch, voltando os arquivos da Tribo a partir do backup. |
| `--sem-wax` | Não gera o arquivo para o mod WAX. |

### Sem o .exe (Python)

Com Python 3.8 ou superior (só a biblioteca padrão):

```
python aplicador/aplicar_patch.py "C:\caminho\do\NieRAutomata"
```

## Como o patch funciona

As correções ficam em texto puro em `patch/textos/*.jsonl`, uma por linha:

```json
{"arquivo": "st1/r110.dat", "membro": "r110_7a562cb9_scp.bin", "id": "M6090_S0091_G0000_300_hennawresi", "antes_sha1": "…", "texto": "Ei, você é do YoRHa, certo?"}
```

- `arquivo` e `membro`: o contêiner `.dat` do jogo e o arquivo interno.
- `id`: o identificador da fala ou mensagem.
- `antes_sha1`: uma assinatura do texto da Tribo, usada para conferir que o texto certo está sendo trocado. O texto anterior em si **não** fica no repositório.
- `texto`: o texto revisado.

O instalador lê os arquivos da sua instalação, troca só os textos listados e regrava os arquivos. Ele trata os formatos do jogo: DAT, scripts mruby, MCD, TMD, SMD e as novels em texto. O `patch/manifesto.json` guarda as assinaturas (SHA-256) dos arquivos da Tribo v1.00 e do resultado esperado.

## Contribuindo

Encontrou um erro? Abra uma *issue* com a fala, onde ela aparece e a sugestão.

Para propor a correção diretamente:

1. Gere a planilha de revisão (antes/depois) a partir da sua instalação:
   ```
   python ferramentas/exportar_revisao.py "C:\caminho\do\NieRAutomata" revisao.csv
   ```
2. Edite o campo `texto` da linha correspondente em `patch/textos/*.jsonl` e abra um *pull request*.
   Para corrigir uma fala que ainda não está no patch, adicione uma linha nova no mesmo formato.
3. Siga o [GLOSSARIO.md](GLOSSARIO.md).

Limitação importante: os textos de interface (`interface.jsonl`) só podem usar caracteres que existam na fonte daquele menu. Algumas fontes não têm, por exemplo, "Ê", "Õ", "í", "-" ou "(". O instalador avisa quando um caractere não existe.

## Como gerar o .exe

O executável é gerado automaticamente pelo GitHub Actions (`.github/workflows/release.yml`) quando uma *tag* `v*` é publicada, e anexado à página de Releases. Para gerar localmente no Windows:

```
pip install pyinstaller
pyinstaller --onefile --console --name AplicarPatch-NieR-PTBR --paths aplicador --add-data "patch;patch" aplicador/aplicar_patch.py
```

O executável fica em `dist\`.

## Créditos e direitos

**NieR:Automata** e todo o seu conteúdo (textos, imagens, áudio e marcas) são © **SQUARE ENIX CO., LTD.** Todos os direitos reservados. Este é um projeto de fãs, não oficial, sem fins lucrativos e sem vínculo com a Square Enix ou a PlatinumGames. Se algum detentor de direitos pedir, o projeto será retirado do ar.

**Tradução original — Tribo Gamer Brasil** (v1.00, 09/02/2023):

| Função | Equipe |
|---|---|
| Tradutores | Archenbaldt, Zexia, H3rdell, MJarcos, Ribacm, 0TARIO, RevolutionJTG, Julio Cesar, Alex_TR, Alves_TR |
| Revisores | Squall_TR, Archenbaldt |
| Testes | H3rdell, rhadamants, Squall_TR |
| Administração | H3rdell (admin), Squall_TR, Alex_TR, Archenbaldt (coadmins) |
| Instalador e ferramentas | H3rdell, TriboGamerBrasil |

Página da tradução: <https://tribogamer.com/traducoes/486_traducao-do-nier-automata-game-of-the-yorha-edition-para-portugues-do-brasil.html>

**Revisão:** Gustavo Perroni Mota, com auxílio do Claude (Anthropic).

## Licença

- **Código** (`aplicador/`, `ferramentas/`, workflows): [MIT](LICENSE).
- **Correções de texto** (`patch/`, `GLOSSARIO.md`): [CC BY-NC-SA 4.0](LICENSE-CONTEUDO.md), **apenas sobre as alterações feitas por este projeto**. Os textos do jogo pertencem à Square Enix e a tradução base é de autoria da Tribo Gamer Brasil; nenhum direito sobre essas obras é concedido por este repositório.
