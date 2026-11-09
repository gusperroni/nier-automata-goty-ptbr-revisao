# Contribuindo

Obrigado por ajudar a melhorar a tradução! Toda sugestão é bem-vinda, de um erro de digitação a uma fala inteira mal traduzida.

## Reportando um erro

Abra uma [issue de correção de tradução](../../issues/new?template=correcao.yml) com:

- o texto como aparece no jogo (uma captura de tela ajuda muito);
- onde ele aparece (missão, personagem, menu, cena);
- a sua sugestão de texto.

## Propondo a correção diretamente

1. Gere a planilha de revisão (antes/depois) a partir da sua instalação. O texto "antes" é lido da tradução da Tribo no seu computador, porque ele não fica no repositório:
   ```
   python ferramentas/exportar_revisao.py "C:\caminho\do\NieRAutomata" revisao.csv
   ```
2. Localize a linha em `patch/textos/*.jsonl` e edite o campo `texto`.
   - Para corrigir um texto que ainda não está no patch, adicione uma linha nova no mesmo formato. O `antes_sha1` são os 12 primeiros caracteres do SHA-1 (UTF-8) do texto atual da Tribo.
3. Teste aplicando o patch sobre uma cópia da pasta do jogo:
   ```
   python aplicador/aplicar_patch.py "C:\copia\do\NieRAutomata"
   ```
4. Abra um _pull request_ explicando o motivo da mudança.

### Regras de estilo

- Siga o [GLOSSARIO.md](GLOSSARIO.md). Se a correção mudar um termo do glossário, proponha a mudança no glossário também.
- Mantenha as marcações do jogo intactas: `<KC_…>`, `<ICON_…>`, `{8020:79}`, `⏎`/`\n` e afins.
- Textos de interface (`interface.jsonl`) só podem usar caracteres que existam na fonte daquele menu. Algumas fontes não têm, por exemplo, "Ê", "Õ", "í", "-" ou "(". O instalador avisa quando um caractere não existe.
- Legendas e menus têm espaço limitado: prefira redações curtas.

## Gerando o .exe

O executável é gerado automaticamente pelo GitHub Actions ([`release.yml`](.github/workflows/release.yml)) quando uma _tag_ `v*` é publicada, e anexado à página de Releases.

Para gerar localmente no Windows:

```
pip install pyinstaller
pyinstaller --onefile --console --name AplicarPatch-NieR-PTBR --paths aplicador --add-data "patch;patch" aplicador/aplicar_patch.py
```

O executável fica em `dist\`.

## Publicando uma versão (mantenedores)

1. Atualize `versao_patch` e as assinaturas de resultado em `patch/manifesto.json` e registre a versão anterior em `versoes_anteriores`, para que o instalador consiga atualizar quem já aplicou o patch.
2. Atualize o [CHANGELOG.md](CHANGELOG.md).
3. Crie e envie a _tag_: `git tag vX.Y.Z && git push origin vX.Y.Z`.
