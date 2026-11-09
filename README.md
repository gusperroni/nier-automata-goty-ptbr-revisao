<div align="center">

# NieR:Automata — Revisão da tradução pt-BR

**Patch de revisão para a tradução em português do Brasil de _NieR:Automata – Game of the YoRHa Edition_ (Steam), feita pela [Tribo Gamer Brasil](https://tribogamer.com/traducoes/486_traducao-do-nier-automata-game-of-the-yorha-edition-para-portugues-do-brasil.html).**

Correções de contexto, gramática e consistência de termos — sem distribuir nenhum arquivo do jogo ou da tradução original.

[![Release](https://img.shields.io/github/v/release/gusperroni/nier-automata-goty-ptbr-revisao?label=vers%C3%A3o&color=c8b78a)](../../releases/latest)
[![Downloads](https://img.shields.io/github/downloads/gusperroni/nier-automata-goty-ptbr-revisao/total?label=downloads&color=4c4a45)](../../releases)
[![Plataforma](https://img.shields.io/badge/plataforma-Windows%20%C2%B7%20Steam-4c4a45)](#-requisitos)
[![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-4c4a45)](LICENSE)
[![Conteúdo: CC BY-NC-SA 4.0](https://img.shields.io/badge/conte%C3%BAdo-CC%20BY--NC--SA%204.0-4c4a45)](LICENSE-CONTEUDO.md)

[**⬇️ Baixar**](../../releases/latest) · [Instalação](#-instalação) · [O que muda](#-o-que-a-revisão-corrige) · [Contribuir](CONTRIBUTING.md) · [Créditos](#-créditos-e-direitos)

</div>

---

> [!IMPORTANT]
> Este projeto **não é uma tradução nova** e **não contém arquivos do jogo nem da tradução da Tribo**. Ele é aplicado **por cima** da tradução da Tribo Gamer Brasil v1.00, que precisa estar instalada.

## Sumário

- [O que a revisão corrige](#-o-que-a-revisão-corrige)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Compatibilidade](#-compatibilidade)
- [Perguntas frequentes](#-perguntas-frequentes)
- [Como o patch funciona](#%EF%B8%8F-como-o-patch-funciona)
- [Contribuindo](#-contribuindo)
- [Créditos e direitos](#-créditos-e-direitos)
- [Licença](#-licença)

## ✨ O que a revisão corrige

Cerca de **4.200 textos** revisados em mais de 200 arquivos:

| Área | Correções |
|---|---:|
| Falas e diálogos (cenas, missões, NPCs) | 2.678 |
| Textos de missões, inimigos, arquivos e itens | 919 |
| Interface (menus, HUD, créditos) | 400 |
| Legendas de cenas | 187 |
| Novels visuais (Devola e Popola, Anemone, Adam, 9S, Plato) | 81 trechos |

<details>
<summary><b>Exemplos de correções</b></summary>

- **Erros de sentido:** o servidor sob o Monte Ka'ala era "humano" em vez de "inimigo"; "Nines" virava "Nove"; _toothbrush_ virava "pasta de dente"; _port_ virava "portaria".
- **Consistência de termos:** YoRHa sempre no masculino ("do YoRHa"), "aldeia do Pascal", "invasão/invadir" na interface, "chip de ampliação", "Plato 1728", "descida". Veja o [glossário](GLOSSARIO.md).
- **Português:** crase, concordância, hífens, números no formato brasileiro, aspas e trechos que estavam faltando.
- **Rodapé do menu principal:** apenas o copyright da Square Enix, traduzido.

</details>

## 📋 Requisitos

- **NieR:Automata – Game of the YoRHa Edition** original (Steam, Windows).
- **Tradução da Tribo Gamer Brasil v1.00** (09/02/2023) instalada na pasta `data` do jogo.
- Opcional: o mod **[WAX](https://www.nexusmods.com/nierautomata)** — veja [Compatibilidade](#-compatibilidade).

> [!NOTE]
> O instalador confere cada arquivo antes de alterar qualquer coisa. Se algum arquivo não for exatamente o da Tribo v1.00 (ou de uma versão anterior deste patch), **nada é modificado**.

## 🚀 Instalação

1. Instale a tradução da Tribo Gamer Brasil v1.00, se ainda não tiver.
2. Baixe o `.zip` da [versão mais recente](../../releases/latest).
3. Extraia o `AplicarPatch-NieR-PTBR.exe` **na pasta do jogo** (onde fica o `NieRAutomata.exe`), por exemplo:
   `C:\Program Files (x86)\Steam\steamapps\common\NieRAutomata`
4. Execute o `AplicarPatch-NieR-PTBR.exe` e aguarde a mensagem **"Pronto!"**.

O instalador guarda uma cópia dos arquivos da Tribo em `data\_backup_revisao_ptbr` antes de alterar qualquer coisa.

<details>
<summary><b>Opções de linha de comando</b></summary>

```
AplicarPatch-NieR-PTBR.exe "C:\caminho\do\NieRAutomata" [--verificar] [--restaurar] [--sem-wax]
```

| Opção | O que faz |
|---|---|
| `--verificar` | Só confere os arquivos (originais da Tribo, já corrigidos, de versão anterior ou diferentes), sem alterar nada. |
| `--restaurar` | Desfaz o patch, voltando os arquivos da Tribo a partir do backup. |
| `--sem-wax` | Não gera o arquivo para o mod WAX. |

</details>

<details>
<summary><b>Sem o .exe (Python)</b></summary>

Com Python 3.8 ou superior (só a biblioteca padrão):

```
python aplicador/aplicar_patch.py "C:\caminho\do\NieRAutomata"
```

</details>

### Atualizando o patch

Basta executar a versão nova do instalador. Ele reconhece os arquivos corrigidos por versões anteriores do patch e os atualiza a partir do backup.

## 🧩 Compatibilidade

| Item | Situação |
|---|---|
| Jogo original (antes de nov/2026) | ✅ Suportado |
| Atualização de nov/2026 (chinês simplificado/tradicional e coreano) | ✅ Suportado — os scripts de falas são reconstruídos a partir dos arquivos novos do jogo, mantendo as correções da atualização |
| Mod WAX 0.3.0-beta.6 ou superior | ✅ Suportado — o instalador gera a versão traduzida da "Mulher Estranha" |
| Outras traduções ou versões da Tribo | ❌ Não suportado |

> [!TIP]
> **Atualizou o jogo ou instalou o WAX depois do patch?** Execute o instalador de novo. Ele só refaz o que for necessário.

## ❓ Perguntas frequentes

<details>
<summary><b>O instalador diz que há arquivos "diferentes" e não altera nada.</b></summary>

Algum arquivo da pasta `data` não é o da tradução da Tribo v1.00 — por exemplo, por outra tradução, outro mod ou uma versão diferente. Reinstale a tradução da Tribo v1.00 e execute o instalador de novo. Use `--verificar` para ver a lista.

</details>

<details>
<summary><b>A "Mulher Estranha" do acampamento da Resistência aparece em inglês.</b></summary>

O mod WAX substitui o script dessa personagem por uma cópia própria, em inglês. Execute o instalador **depois** de instalar ou atualizar o WAX: ele gera a versão traduzida em `wax\mods\TraducaoPTBR\overrides`.

</details>

<details>
<summary><b>Como desinstalar?</b></summary>

Execute `AplicarPatch-NieR-PTBR.exe --restaurar`. Os arquivos voltam à versão da Tribo Gamer, e o arquivo do WAX é removido.

</details>

<details>
<summary><b>O antivírus reclamou do .exe.</b></summary>

O executável é gerado pelo PyInstaller no GitHub Actions a partir do código deste repositório, e alguns antivírus dão falso positivo nesse tipo de arquivo. Se preferir, rode direto pelo Python (veja [Instalação](#-instalação)) ou [gere o .exe você mesmo](CONTRIBUTING.md#gerando-o-exe).

</details>

## ⚙️ Como o patch funciona

As correções ficam em texto puro em [`patch/textos/*.jsonl`](patch/textos), uma por linha:

```json
{"arquivo": "st1/r110.dat", "membro": "r110_7a562cb9_scp.bin", "id": "M6090_S0091_G0000_300_hennawresi", "antes_sha1": "…", "texto": "Ei, você é do YoRHa, certo?"}
```

- **`arquivo` / `membro`:** o contêiner `.dat` do jogo e o arquivo interno.
- **`id`:** o identificador da fala ou mensagem.
- **`antes_sha1`:** uma assinatura do texto da Tribo, usada para conferir que o texto certo está sendo trocado. O texto anterior em si **não** fica no repositório.
- **`texto`:** o texto revisado.

O instalador lê os arquivos da sua instalação, troca só os textos listados e regrava os arquivos, tratando os formatos do jogo (DAT, scripts mruby, MCD, TMD, SMD, CPK e as novels em texto). Quando o jogo tem a atualização de novembro/2026, os scripts de falas são montados a partir das versões novas do jogo, com o português da Tribo e as correções deste patch. O [`patch/manifesto.json`](patch/manifesto.json) guarda as assinaturas (SHA-256) dos arquivos esperados e dos resultados.

## 🤝 Contribuindo

Encontrou um erro de tradução? **[Abra uma issue](../../issues/new/choose)** com a fala, onde ela aparece e a sua sugestão.

Para propor a correção diretamente, veja o [CONTRIBUTING.md](CONTRIBUTING.md) e siga o [glossário](GLOSSARIO.md).

## 🙏 Créditos e direitos

**_NieR:Automata_** e todo o seu conteúdo (textos, imagens, áudio e marcas) são © **SQUARE ENIX CO., LTD.** Todos os direitos reservados. Este é um projeto de fãs, não oficial, sem fins lucrativos e sem vínculo com a Square Enix, a PlatinumGames ou a Tribo Gamer Brasil. Se algum detentor de direitos pedir, o projeto será retirado do ar.

### Tradução original — Tribo Gamer Brasil (v1.00, 09/02/2023)

| Função | Equipe |
|---|---|
| Tradutores | Archenbaldt, Zexia, H3rdell, MJarcos, Ribacm, 0TARIO, RevolutionJTG, Julio Cesar, Alex_TR, Alves_TR |
| Revisores | Squall_TR, Archenbaldt |
| Testes | H3rdell, rhadamants, Squall_TR |
| Administração | H3rdell (admin), Squall_TR, Alex_TR, Archenbaldt (coadmins) |
| Instalador e ferramentas | H3rdell, TriboGamerBrasil |

Página da tradução: <https://tribogamer.com/traducoes/486_traducao-do-nier-automata-game-of-the-yorha-edition-para-portugues-do-brasil.html>

### Revisão

Gustavo Perroni Mota, com auxílio do Claude (Anthropic).

## 📄 Licença

| Parte | Licença |
|---|---|
| Código (`aplicador/`, `ferramentas/`, workflows) | [MIT](LICENSE) |
| Correções de texto (`patch/`, `GLOSSARIO.md`) | [CC BY-NC-SA 4.0](LICENSE-CONTEUDO.md), **apenas sobre as alterações feitas por este projeto** |

Os textos do jogo pertencem à Square Enix e a tradução base é de autoria da Tribo Gamer Brasil; nenhum direito sobre essas obras é concedido por este repositório.
