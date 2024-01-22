
  $(document).ready(function() {
    //Pega a atividade de todos os botões com os id's listados
    $('#geral, #aberto, #agendado, #finalizado, #andamento, #validacao, #esclarecimento').click(function() {
      
      //Botão que foi selecionado
      var statusSelected = $(this).attr('id');

      //Tabela de chamados
      var tableBody = $('#tableBody');
      tableBody.empty();

      //Input que esta no template de listar-chamado contendo o json dos chamados
      var inputElement = document.getElementById('jsonInput');
      var data = inputElement.value;

      // Troca os none da string para null e aspas simples '' para aspas duplas ""
      var cleanedString = data.replace(/None/g, 'null').replace(/'/g, '"');
      
      // Transforma string em json para manipulação
      data = JSON.parse(cleanedString)

      for (var i = 0; i < data.length; i++) {
        var item = data[i];
        var statusBagde = ''
        const currentURL = window.location.href;
        const urlToKeep = currentURL.substring(0, currentURL.length - 15);
        var href = urlToKeep + `editar_chamado/${item.id}`
        // Não dar console.log nesse href, pode ocasionar um problema

        // Executa a lógica de deixar os chamados com a cor vermelha ou não
        if(item.updated_at  == "passou") {
          style = "background-color: lightcoral; color: white;"
        } else {
          style = style=""
        }

        //Troca o número do status pelo nome
        if(item.status == 1) {
          status = '<td style="' + style + '"><span class="badge bg-success">Aberto</span></td>';

        } else if(item.status == 2) {
          status = '<td style="' + style + '"><span class="badge bg-danger">Finalizado</span></td>';
        
        } else if (item.status == 3) {
          status = '<td style="' + style + '"><span class="badge bg-warning">Em andamento</span></td>'; 
        
        } else if (item.status == 6) {
          status = '<td style="' + style + '"><span class="badge bg-secondary">Ag.Validação</span></td>'; 
        }

        //Troca a cor da bedge de acordo com a prioridade
        if (item.prioridade == 'alta') {
          prioridade = '<td style="' + style + '"><span class="badge bg-danger">Alta</span></td>';
        } else if (item.prioridade == 'media') {
          prioridade = '<td style="' + style + '"><span class="badge bg-warning">Media</span></td>';
        } else if (item.prioridade == 'baixa') {
          prioridade = '<td style="' + style + '"><span class="badge bg-success">Baixa</span></td>';
        }


        // Condições para listar de acordo com o status, apenas chamados abertos, finalizados...
        if(statusSelected == 'aberto') {
          if (item.status == 1){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }
        
        } else if (statusSelected == 'finalizado') {
          if (item.status == 2){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          } 

        } else if (statusSelected == 'andamento') {
          if (item.status == 3){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }

        } else if(statusSelected == 'validacao') {
          if (item.status == 6){
            var row = '<tr>' +
            '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
            '<td style="' + style + '">' + item.titulo + '</td>' +
            '<td style="' + style + '">' + item.problema + '</td>' +
            '<td style="' + style + '">' + item.setor_recebe + '</td>' +
            status +
            prioridade +
            '<td style="' + style + '">' + item.created_at + '</td>' +
            '<td style="' + style + '">' + item.m_sla + '</td>' +
            '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
          }

        } else if (statusSelected == 'geral') {
          var row = '<tr>' +
          '<td style="' + style + '"><a href="' + href + '">' + item.id + '</a></td>' +
          '<td style="' + style + '">' + item.titulo + '</td>' +
          '<td style="' + style + '">' + item.problema + '</td>' +
          '<td style="' + style + '">' + item.setor_recebe + '</td>' +
          status +
          prioridade +
          '<td style="' + style + '">' + item.created_at + '</td>' +
          '<td style="' + style + '">' + item.m_sla + '</td>' +
          '<td style="' + style + '">' + item.t_co + '</td>' +
            '</tr>';
          tableBody.append(row);
        }
      }
    });
  });