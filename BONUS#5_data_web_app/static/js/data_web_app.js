// #______________________________________________________
// # Author: German Barboza                               |
// # email: germanbarboza@gmail.com                       |
// # github: germanicox                                   |
// # twitter: germanicox                                  |
// # linkedin: https://www.linkedin.com/in/gbarboza2020/  |
// #______________________________________________________

// # November - 2020
// # This script is inented to solve data collection and format for SPE-2020 Colombia Section Hackaton 
// # Details at: https://github.com/specolombiahackathon/202010/wiki


$(document).ready(function() { //To run code as soon as the document is ready to be manipulated
    $('#production_query').on('click', function(event) {
               
        // $('#image').prop("hidden", true)
        console.log('Click en production_query')

        $.ajax({
            data : { //JSON Data Type for data_web_app.py
                year_input :          $('#year_input').val(),
                departamento_input:   $('#departamento_input').val(),
                municipio_input:      $('#municipio_input').val(),
                operadora_input:      $('#operadora_input').val(),
                contrato_input:       $('#contrato_input').val(),
                campo_input:          $('#campo_input').val(),               
            }, 
            type : 'POST', 
            url : '/production_query'
        })
        .done(function(data) {          
            if (data.error){
              console.log("Not Found query in database, adjust your query ...")
              const table = document.getElementById("query_result");
                 table.innerHTML = "";
                $("#errorAlert").prop("hidden", false)
                $("#image").prop("hidden", true)

                //  document.getElementById("errorAlert").style.visibility = "visible";
            }
            else {
                
                $("#errorAlert").prop("hidden", true)
                 var empObj = JSON.parse(data); 

                //  $(#"query_result").remove();

                 const table = document.getElementById("query_result");
                 table.innerHTML = "";

                //  let row = table.insertRow();
                //  let ind = row.insertCell(0);
                //  ind.innerHTML = "Hola"
                //  let year = row.insertCell(1);
                //  year.innerHTML = "Mundo"

                // iterate over every row and populate column from left to right 

                d = new Date();
                $('#image').prop('src', "./static/grafico.png?"+d.getTime() );
                $("#image").prop("hidden", false)
                var how_many = Object.keys(empObj.index).length.toString();
                for (var i = 0; i< how_many; i++){
                    let row = table.insertRow();
                    // inserting index 
                    let ind = row.insertCell(0);
                    ind.innerHTML = empObj.index[i.toString()]
                    console.log(empObj.index[i.toString()] )
                    // inserting year
                    let y = row.insertCell(1);
                    y.innerHTML = empObj.YEAR[i.toString()]
                    console.log(empObj.YEAR[i.toString()] )
                    // inserting DEPARTAMENTO
                    let dpto = row.insertCell(2);
                    dpto.innerHTML = empObj.DEPARTAMENTO[i.toString()]
                    console.log(empObj.DEPARTAMENTO[i.toString()] )
                    // inserting MUNICIPIO
                    let mcpo = row.insertCell(3);
                    mcpo.innerHTML = empObj.MUNICIPIO[i.toString()]
                    console.log(empObj.MUNICIPIO[i.toString()] )
                    // inserting OPERADORA
                    let oper = row.insertCell(4);
                    oper.innerHTML = empObj.OPERADORA[i.toString()]
                    console.log(empObj.OPERADORA[i.toString()] )
                    // inserting CONTRATO
                    let cont = row.insertCell(5);
                    cont.innerHTML = empObj.CONTRATO[i.toString()]
                    console.log(empObj.CONTRATO[i.toString()] )
                    // inserting CAMPO
                    let cam = row.insertCell(6);
                    cam.innerHTML = empObj.CAMPO[i.toString()]
                    console.log(empObj.CAMPO[i.toString()] )
                    // inserting ENERO
                    let jan = row.insertCell(7);
                    jan.innerHTML = empObj.ENERO[i.toString()]
                    console.log(empObj.ENERO[i.toString()] )
                    // inserting FEBRERO
                    let feb = row.insertCell(8);
                    feb.innerHTML = empObj.FEBRERO[i.toString()]
                    console.log(empObj.FEBRERO[i.toString()] )
                    // inserting MARZO
                    let mar = row.insertCell(9);
                    mar.innerHTML = empObj.MARZO[i.toString()]
                    console.log(empObj.MARZO[i.toString()] )
                    // inserting ABRIL
                    let apr = row.insertCell(10);
                    apr.innerHTML = empObj.ABRIL[i.toString()]
                    console.log(empObj.ABRIL[i.toString()] )
                    // inserting MAYO
                    let may = row.insertCell(11);
                    may.innerHTML = empObj.MAYO[i.toString()]
                    console.log(empObj.MAYO[i.toString()] )
                    // inserting JUNIO
                    let jun = row.insertCell(12);
                    jun.innerHTML = empObj.JUNIO[i.toString()]
                    console.log(empObj.JUNIO[i.toString()] )
                    // inserting JULIO
                    let jul = row.insertCell(13);
                    jul.innerHTML = empObj.JULIO[i.toString()]
                    console.log(empObj.JULIO[i.toString()] )
                    // inserting AGOSTO
                    let aug = row.insertCell(14);
                    aug.innerHTML = empObj.AGOSTO[i.toString()]
                    console.log(empObj.AGOSTO[i.toString()] )
                    // inserting SEPTIEMBRE
                    let sep = row.insertCell(14);
                    sep.innerHTML = empObj.SEPTIEMBRE[i.toString()]
                    console.log(empObj.SEPTIEMBRE[i.toString()] )
                    // inserting OCTUBRE
                    let oct = row.insertCell(15);
                    oct.innerHTML = empObj.OCTUBRE[i.toString()]
                    console.log(empObj.OCTUBRE[i.toString()] )
                    // inserting NOVIEMBRE
                    let nov = row.insertCell(16);
                    nov.innerHTML = empObj.NOVIEMBRE[i.toString()]
                    console.log(empObj.NOVIEMBRE[i.toString()] )
                    // inserting DICIEMBRE
                    let dec = row.insertCell(17);
                    dec.innerHTML = empObj.DICIEMBRE[i.toString()]
                    console.log(empObj.DICIEMBRE[i.toString()] )
                    // end for iterate and populate table 
                }


            }
        });


    });

});