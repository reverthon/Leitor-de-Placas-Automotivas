# Leitor-de-Placas-Automotivas

Este projeto é um leitor de placas veiculares em tempo real que usa OpenCV, EasyOCR e uma interface gráfica em Tkinter para capturar imagens da câmera, detectar a placa e consultar em um banco de dados SQLite.

Principais tecnologias usadas:
-------------------------------
- Python 3
- OpenCV
- EasyOCR
- Tkinter (para interface gráfica)
- SQLite3 (para banco de dados)

Como funciona:
--------------
1. O usuário clica no botão "Abrir Câmera" na interface.
2. A câmera é aberta e permite o posicionamento da placa.
3. Ao capturar a imagem, o OCR realiza a leitura da placa.
4. O sistema exibe o texto detectado na interface e oferece as opções:
   - Confirmar Consulta: realiza a busca no banco de dados.
   - Tentar Novamente: reabre a câmera para nova captura.
   - Cancelar: encerra o processo atual.
5. Se confirmada a consulta, os dados do veículo (placa, dono, situação) são exibidos.

Observações sobre desempenho:
------------------------------
⚠ Durante a execução você poderá ver no terminal a mensagem:
"Neither CUDA nor MPS are available - defaulting to CPU. Note: This module is much faster with a GPU."

Isso significa que o EasyOCR está sendo executado usando CPU (processador) e não GPU (placa gráfica). O uso da GPU aceleraria consideravelmente o processamento do OCR. No entanto, para este projeto e fins didáticos, optou-se por utilizar apenas a CPU, pois é mais acessível e compatível com a maioria dos ambientes.

Pré-requisitos:
---------------
- Python 3.x instalado
- Dependências instaladas:
  pip install opencv-python easyocr torch tkinter pillow

Como executar:
--------------
1. Clone este repositório:
   git clone https://github.com/seuusuario/leitor-de-placas.git

2. Navegue até o diretório:
   cd leitor-de-placas

3. Execute o script:
   python leitor_placas.py

Licença:
--------
Este projeto é fornecido sob a licença Apache 2.0.

Autor:
------
Reverthon Santos
