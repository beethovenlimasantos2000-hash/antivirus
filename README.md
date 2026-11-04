# USB Guardian

Ferramenta de diagnóstico USB e triagem de arquivos para ChromeOS com ambiente Linux (Crostini), arquitetura x86-64.

## Recursos
- Lista dispositivos USB que o kernel Linux conseguiu enumerar (sysfs; lsusb como complemento).
- Exibe fabricante, produto, VID:PID, classe, barramento e porta quando disponíveis.
- Diagnóstico somente leitura: verifica acesso USB, ferramentas disponíveis e informações do dispositivo.
- Triagem de arquivos escolhidos pelo usuário; usa ClamAV se instalado e apresenta heurísticas simples caso contrário.
- Interface gráfica em português.

## Limitações importantes
Nenhum aplicativo pode detectar por software um dispositivo que não é enumerado pelo controlador/firmware/host. Em ChromeOS, conecte o dispositivo ao Linux em **Configurações > Desenvolvedores > Ambiente de desenvolvimento Linux > Gerenciar acesso USB** (o nome pode variar). Se não aparecer no Linux, investigue cabo, porta, alimentação, modo USB/bootloader e firmware.

O aplicativo não injeta software, não altera firmware, não remove arquivos automaticamente e não instala um antivírus dentro do dispositivo. Para analisar o sistema interno, é necessário que ele exponha armazenamento ou uma interface de diagnóstico documentada. Faça backup antes de qualquer reparo.

## Instalação
Baixe o artefato `.deb` da execução mais recente do GitHub Actions e instale no ambiente Linux:
```bash
sudo apt install ./usb-guardian_1.0.0_amd64.deb
```
Dependências: `python3`, `python3-tk`, `usbutils`, `udev`. ClamAV é opcional (`sudo apt install clamav`).

## Desenvolvimento
```bash
python3 src/usb_guardian.py
```

## Build
O GitHub Actions gera um pacote Debian amd64 em cada push na branch main. O pacote é publicado como artefato de workflow (não como release).
