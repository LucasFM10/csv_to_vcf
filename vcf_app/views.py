# Dentro de vcf_app/views.py
from django.shortcuts import render
from django.http import HttpResponse # Para enviar o arquivo VCF
import csv
import io
from datetime import datetime # Para o campo REV no vCard

def gerador_vcf_view(request):
    context = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'analyze_csv':
            print("Requisição POST recebida para 'analyze_csv'")
            csv_file = request.FILES.get('csv_file')
            context['show_config_section'] = False # Default

            if csv_file:
                print(f"Arquivo '{csv_file.name}' recebido.")
                try:
                    # Armazena o conteúdo original do CSV na sessão
                    csv_data_bytes = csv_file.read()
                    request.session['csv_data_bytes_str'] = csv_data_bytes.decode('utf-8-sig') # Guarda como string
                    request.session['original_filename'] = csv_file.name

                    # Reabre para ler os headers (não consome o principal)
                    decoded_file_for_headers = csv_data_bytes.decode('utf-8-sig')
                    io_string_for_headers = io.StringIO(decoded_file_for_headers)
                    reader_for_headers = csv.reader(io_string_for_headers)
                    headers = next(reader_for_headers, None)

                    if headers:
                        cleaned_headers = [header.strip() for header in headers]
                        request.session['csv_headers'] = cleaned_headers # Guarda headers na sessão
                        
                        context['csv_headers'] = cleaned_headers
                        context['file_uploaded_name'] = csv_file.name
                        context['show_config_section'] = True
                        context['message'] = f"Arquivo '{csv_file.name}' analisado. Configure os campos abaixo."
                    else:
                        context['error_message'] = "Nenhuma coluna (cabeçalho) encontrada no arquivo CSV."
                except UnicodeDecodeError:
                    context['error_message'] = "Erro de decodificação. Verifique se o arquivo CSV está em UTF-8."
                except Exception as e:
                    context['error_message'] = f"Erro ao processar o arquivo CSV: {e}"
            else:
                context['error_message'] = "Nenhum arquivo CSV foi selecionado."
            
            return render(request, 'vcf_app/gerador_vcf.html', context)

        elif action == 'generate_vcf':
            print("Requisição POST recebida para 'generate_vcf'")
            # Recupera dados da sessão
            csv_data_str = request.session.get('csv_data_bytes_str')
            csv_headers_session = request.session.get('csv_headers')
            original_filename = request.session.get('original_filename', 'contatos')

            # Recupera dados do formulário
            name_format = request.POST.get('name_format')
            phone_column = request.POST.get('phone_column')

            # Prepara contexto para re-renderizar em caso de erro, mantendo a Seção 2
            context['csv_headers'] = csv_headers_session
            context['file_uploaded_name'] = original_filename
            context['show_config_section'] = True
            context['name_format_value'] = name_format # Para preencher o campo novamente
            context['phone_column_value'] = phone_column # Para preencher o select novamente

            if not csv_data_str or not csv_headers_session:
                context['error_message'] = "Dados do CSV não encontrados na sessão. Por favor, reenvie o arquivo."
                return render(request, 'vcf_app/gerador_vcf.html', context)

            if not name_format or not phone_column:
                context['error_message'] = "Formato do nome e coluna do telefone são obrigatórios."
                return render(request, 'vcf_app/gerador_vcf.html', context)

            vcard_list = []
            vcard_template = """BEGIN:VCARD
VERSION:3.0
PRODID:-//DjangoApp//VCFGenerator//PT
N:;{nome_contato};;;
FN:{nome_contato}
TEL;type=CELL;type=VOICE;type=pref:{telefone}
REV:{timestamp_rev}
END:VCARD"""
            timestamp_rev = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

            try:
                io_string = io.StringIO(csv_data_str)
                # Usar DictReader para facilitar o .format(**row)
                reader = csv.DictReader(io_string)
                
                if phone_column not in reader.fieldnames:
                    # Adiciona ao fieldnames se não estiver lá mas estiver nos headers da sessão
                    # Isto é uma salvaguarda, mas o DictReader deve pegar os fieldnames corretamente
                    # Se phone_column não estiver nos fieldnames do DictReader, dará erro abaixo
                     context['error_message'] = f"A coluna de telefone '{phone_column}' selecionada não foi encontrada nos cabeçalhos do CSV processado ({', '.join(reader.fieldnames)})."
                     return render(request, 'vcf_app/gerador_vcf.html', context)


                for i, row in enumerate(reader):
                    try:
                        nome_contato = name_format.format(**row)
                        telefone = str(row[phone_column]).strip()

                        if not telefone: # Pula se o telefone estiver vazio
                            continue
                        
                        vcard_list.append(vcard_template.format(
                            nome_contato=nome_contato,
                            telefone=telefone,
                            timestamp_rev=timestamp_rev
                        ))
                    except KeyError as e:
                        # Erro ao formatar nome (coluna não encontrada no .format)
                        # ou ao aceder row[phone_column] (embora já verificado acima)
                        context['error_message'] = f"Erro na linha {i+1} do CSV: Coluna '{str(e)}' não encontrada nos dados ou formato de nome incompatível. Verifique o formato do nome e as colunas disponíveis: {', '.join(row.keys())}"
                        return render(request, 'vcf_app/gerador_vcf.html', context)
                
                if not vcard_list:
                    context['error_message'] = "Nenhum contato válido foi gerado. Verifique se há telefones nas colunas selecionadas ou se o formato do nome é aplicável."
                    return render(request, 'vcf_app/gerador_vcf.html', context)

                # Sucesso: prepara o arquivo para download
                final_vcf_content = "\n".join(vcard_list)
                
                # Limpa a sessão após o sucesso
                request.session.pop('csv_data_bytes_str', None)
                request.session.pop('csv_headers', None)
                request.session.pop('original_filename', None)

                response = HttpResponse(final_vcf_content, content_type='text/vcard; charset=utf-8')
                vcf_filename_base = original_filename.replace('.csv', '').replace(' ', '_').lower()
                response['Content-Disposition'] = f'attachment; filename="contatos_{vcf_filename_base}.vcf"'
                return response

            except Exception as e:
                context['error_message'] = f"Erro inesperado ao gerar o VCF: {e}"
                return render(request, 'vcf_app/gerador_vcf.html', context)

    # Requisição GET (limpa a sessão para um novo começo)
    else:
        request.session.pop('csv_data_bytes_str', None)
        request.session.pop('csv_headers', None)
        request.session.pop('original_filename', None)
        context['show_config_section'] = False

    return render(request, 'vcf_app/gerador_vcf.html', context)