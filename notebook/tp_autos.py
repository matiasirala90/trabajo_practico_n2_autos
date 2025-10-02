from flask import Flask, render_template_string
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Conectar a SQLite
    conn = sqlite3.connect("autos.db")
    df = pd.read_sql_query("SELECT * FROM car_sales", conn)
    conn.close()

    # Convertir columnas a numéricas
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')
    df['year_of_manufacture'] = pd.to_numeric(df['year_of_manufacture'], errors='coerce')
    df['engine_size'] = pd.to_numeric(df['engine_size'], errors='coerce')

    # Eliminar filas con datos faltantes
    df = df.dropna(subset=['price','mileage','year_of_manufacture','manufacturer','fuel_type','model','engine_size'])

    # Lista de registros
    records = df.to_dict(orient='records')

    # Valores por defecto
    minAnio = int(df['year_of_manufacture'].min())
    maxAnio = int(df['year_of_manufacture'].max())
    minEngine = float(df['engine_size'].min())
    maxEngine = float(df['engine_size'].max())
    minPrice = float(df['price'].min())
    maxPrice = float(df['price'].max())

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Dashboard Autos</title>
        <script src="https://cdn.plot.ly/plotly-2.31.1.min.js"></script>
        <style>
            body { font-family: Arial; margin:20px; background:#f4f6f7; }
            h1 { text-align:center; color:#2c3e50; margin-bottom:30px; }
            .filtros { display:flex; flex-wrap:wrap; justify-content:center; gap:25px; margin-bottom:20px; }
            select, input { padding:6px 8px; border-radius:5px; border:1px solid #ccc; font-size:14px; }
            button { padding:6px 12px; border-radius:5px; border:none; background:#3498db; color:white; cursor:pointer; font-size:14px; }
            button:hover { background:#2980b9; }
            .grafico { margin:25px auto; width:95%; max-width:1200px; height:550px; background:white; border-radius:10px; box-shadow:0 3px 12px rgba(0,0,0,0.15); padding:15px; }
            .grafico h3 { margin-bottom:5px; color:#2c3e50; }
            .grafico p { margin-top:10px; color:#555; font-size:14px; }
            table { margin:30px auto; border-collapse:collapse; width:85%; background:white; border-radius:10px; overflow:hidden; box-shadow:0 3px 12px rgba(0,0,0,0.15); font-size:14px; }
            th, td { border:1px solid #ccc; padding:10px; text-align:center; }
            th { background:#2c3e50; color:white; }
            #msg { text-align:center; color:#c0392b; font-weight:bold; margin-bottom:15px; font-size:16px; }
        </style>
    </head>
    <body>
        <h1>Dashboard de Autos</h1>

        <div class="filtros">
            <div><label>Marca:</label><br><select id="filtro-marca"></select></div>
            <div><label>Combustible:</label><br><select id="filtro-combustible"></select></div>
            <div><label>Año:</label><br>
                <input type="number" id="anio-min" min="{{minAnio}}" max="{{maxAnio}}" value="{{minAnio}}"> -
                <input type="number" id="anio-max" min="{{minAnio}}" max="{{maxAnio}}" value="{{maxAnio}}">
            </div>
            <div><label>Cilindrada (L):</label><br>
                <input type="number" id="engine-min" min="{{minEngine}}" max="{{maxEngine}}" value="{{minEngine}}" step="0.1"> -
                <input type="number" id="engine-max" min="{{minEngine}}" max="{{maxEngine}}" value="{{maxEngine}}" step="0.1">
            </div>
            <div><label>Precio:</label><br>
                <input type="number" id="price-min" min="{{minPrice}}" max="{{maxPrice}}" value="{{minPrice}}" step="1000"> -
                <input type="number" id="price-max" min="{{minPrice}}" max="{{maxPrice}}" value="{{maxPrice}}" step="1000">
            </div>
            <div>
                <button id="btn-aplicar">Aplicar</button>
                <button id="btn-reset">Reset</button>
            </div>
        </div>

        <div class="filtros">
            <div><label>Ordenar tabla por:</label><br>
                <select id="orden-columna">
                    <option value="price">Precio Promedio</option>
                    <option value="mileage">Kilometraje Promedio</option>
                    <option value="manufacturer">Marca</option>
                    <option value="fuel_type">Combustible</option>
                </select>
            </div>
            <div><label>Dirección:</label><br>
                <select id="orden-direccion">
                    <option value="desc">Descendente</option>
                    <option value="asc">Ascendente</option>
                </select>
            </div>
        </div>

        <div id="msg"></div>

        <div class="grafico">
            <h3>Scatter: Precio vs Kilometraje</h3>
            <div id="grafico1"></div>
            <p>
                Cada punto representa un auto; el color indica el tipo de combustible. 
                El eje X muestra el kilometraje y el eje Y el precio.
                Permite identificar autos con bajo kilometraje y precios competitivos, y detectar si ciertos tipos de combustible mantienen mejor precio con el tiempo.
            </p>
        </div>

        <div class="grafico">
            <h3>Histograma de Precios</h3>
            <div id="grafico2"></div>
            <p>
                Altura de la barra = cantidad de autos en ese rango de precio, separado por tipo de combustible.
                Permite ver la distribución de precios por combustible, útil para fijar precios de venta competitivos o identificar segmentos del mercado.
            </p>
        </div>

        <div class="grafico">
            <h3>Boxplot por Marca</h3>
            <div id="grafico3"></div>
            <p>
                La caja muestra el rango de precios (mínimo, Q1, mediana, Q3, máximo) por marca.
                Ayuda a identificar marcas que tienden a mantener precios más altos o más estables, facilitando la comparación de riesgos y oportunidades al comprar o vender autos.
            </p>
        </div>

        <div id="tabla-resumen"></div>

        <script>
            var data = {{ records|tojson }};
            var minAnio = {{ minAnio }}, maxAnio = {{ maxAnio }};
            var minEngine = {{ minEngine }}, maxEngine = {{ maxEngine }};
            var minPrice = {{ minPrice }}, maxPrice = {{ maxPrice }};

            function unique(arr){
                var seen = {}; var out = [];
                for(var i=0;i<arr.length;i++){ var item = arr[i]; if(!seen[item]){ seen[item]=true; out.push(item); } }
                return out;
            }

            function groupBy(arr,key){
                var result = {};
                for(var i=0;i<arr.length;i++){
                    var k = arr[i][key] || "Unknown";
                    if(!result[k]) result[k]=[];
                    result[k].push(arr[i]);
                }
                return result;
            }

            function crearTablaResumen(filtrado){
                if(filtrado.length===0) return "<p>No hay datos para la tabla.</p>";
                
                var grupos = {};
                for(var i=0;i<filtrado.length;i++){
                    var m = filtrado[i].manufacturer;
                    var f = filtrado[i].fuel_type;
                    var key = m+"_"+f;
                    if(!grupos[key]) grupos[key]={manufacturer:m, fuel_type:f, price:[], mileage:[]};
                    grupos[key].price.push(filtrado[i].price);
                    grupos[key].mileage.push(filtrado[i].mileage);
                }

                var arrayResumen = [];
                for(var key in grupos){
                    var avgPrice = (grupos[key].price.reduce((a,b)=>a+b,0)/grupos[key].price.length).toFixed(2);
                    var avgMileage = (grupos[key].mileage.reduce((a,b)=>a+b,0)/grupos[key].mileage.length).toFixed(2);
                    arrayResumen.push({
                        manufacturer: grupos[key].manufacturer,
                        fuel_type: grupos[key].fuel_type,
                        price: parseFloat(avgPrice),
                        mileage: parseFloat(avgMileage)
                    });
                }

                var col = document.getElementById("orden-columna").value;
                var dir = document.getElementById("orden-direccion").value;
                arrayResumen.sort((a,b)=>{
                    if(dir==="asc") return (a[col] > b[col]) ? 1 : -1;
                    else return (a[col] < b[col]) ? 1 : -1;
                });

                var html="<table><tr><th>Marca</th><th>Combustible</th><th>Precio Promedio</th><th>Kilometraje Promedio</th></tr>";
                arrayResumen.forEach(r=>{
                    html += `<tr><td>${r.manufacturer}</td><td>${r.fuel_type}</td><td>$${r.price}</td><td>${r.mileage}</td></tr>`;
                });
                html += "</table>";
                return html;
            }

            var filtroMarca = document.getElementById("filtro-marca");
            var filtroComb = document.getElementById("filtro-combustible");
            var anioMinInput = document.getElementById("anio-min");
            var anioMaxInput = document.getElementById("anio-max");
            var engineMinInput = document.getElementById("engine-min");
            var engineMaxInput = document.getElementById("engine-max");
            var priceMinInput = document.getElementById("price-min");
            var priceMaxInput = document.getElementById("price-max");
            var btnAplicar = document.getElementById("btn-aplicar");
            var btnReset = document.getElementById("btn-reset");
            var msg = document.getElementById("msg");
            var tablaDiv = document.getElementById("tabla-resumen");

            var marcas = ["Todas"].concat(unique(data.map(d=>d.manufacturer))).sort();
            marcas.forEach(m=>filtroMarca.innerHTML += "<option>"+m+"</option>");
            var combustibles = ["Todos"].concat(unique(data.map(d=>d.fuel_type))).sort();
            combustibles.forEach(c=>filtroComb.innerHTML += "<option>"+c+"</option>");

            function actualizar(){
                msg.innerHTML="";
                var marca = filtroMarca.value;
                var comb = filtroComb.value;

                var amin = parseInt(anioMinInput.value) || minAnio;
                var amax = parseInt(anioMaxInput.value) || maxAnio;
                var emin = parseFloat(engineMinInput.value) || minEngine;
                var emax = parseFloat(engineMaxInput.value) || maxEngine;
                var pmin = parseFloat(priceMinInput.value) || minPrice;
                var pmax = parseFloat(priceMaxInput.value) || maxPrice;

                if(amin > amax){ [amin, amax] = [amax, amin]; msg.innerHTML="Año mínimo mayor que máximo, valores intercambiados."; anioMinInput.value=amin; anioMaxInput.value=amax; }
                if(emin > emax){ [emin, emax] = [emax, emin]; msg.innerHTML="Cilindrada mínima mayor que máxima, valores intercambiados."; engineMinInput.value=emin; engineMaxInput.value=emax; }
                if(pmin > pmax){ [pmin, pmax] = [pmax, pmin]; msg.innerHTML="Precio mínimo mayor que máximo, valores intercambiados."; priceMinInput.value=pmin; priceMaxInput.value=pmax; }

                var filtrado = data.filter(d=>{
                    return (marca==="Todas" || d.manufacturer===marca) &&
                           (comb==="Todos" || d.fuel_type===comb) &&
                           (d.year_of_manufacture>=amin && d.year_of_manufacture<=amax) &&
                           (d.engine_size>=emin && d.engine_size<=emax) &&
                           (d.price>=pmin && d.price<=pmax);
                });

                if(filtrado.length===0){
                    msg.innerHTML="No hay datos para los filtros seleccionados.";
                    Plotly.purge("grafico1"); Plotly.purge("grafico2"); Plotly.purge("grafico3");
                    tablaDiv.innerHTML="";
                    return;
                }

                var gruposFuel = groupBy(filtrado,"fuel_type");
                var scatterTraces = [];
                for(var ft in gruposFuel){
                    scatterTraces.push({
                        x: gruposFuel[ft].map(d=>d.mileage),
                        y: gruposFuel[ft].map(d=>d.price),
                        mode:"markers",
                        name: ft,
                        text: gruposFuel[ft].map(d=>d.manufacturer+" "+d.model+" ("+d.year_of_manufacture+") | Engine: "+d.engine_size+"L | Mileage: "+d.mileage+" | Price: $"+d.price),
                        type:"scatter"
                    });
                }
                Plotly.newPlot("grafico1", scatterTraces, {title:"Precio vs Kilometraje por tipo de combustible"});

                var histTraces = [];
                for(var ft in gruposFuel){
                    histTraces.push({
                        x: gruposFuel[ft].map(d=>d.price),
                        name: ft,
                        type:"histogram",
                        opacity:0.6,
                        hovertemplate: '$%{x}<br>Count: %{y}<extra></extra>'
                    });
                }
                Plotly.newPlot("grafico2", histTraces, {title:"Distribución de Precios por tipo de combustible", barmode:"overlay"});

                var gruposMarca = groupBy(filtrado,"manufacturer");
                var boxTraces = [];
                for(var br in gruposMarca){
                    boxTraces.push({
                        y: gruposMarca[br].map(d=>d.price),
                        name: br,
                        type:"box",
                        hovertemplate: '$%{y}<extra></extra>'
                    });
                }
                Plotly.newPlot("grafico3", boxTraces, {title:"Rango de precios por Marca"});

                tablaDiv.innerHTML = crearTablaResumen(filtrado);
            }

            btnAplicar.addEventListener("click", actualizar);
            btnReset.addEventListener("click", function(){
                filtroMarca.value="Todas";
                filtroComb.value="Todos";
                anioMinInput.value=minAnio;
                anioMaxInput.value=maxAnio;
                engineMinInput.value=minEngine;
                engineMaxInput.value=maxEngine;
                priceMinInput.value=minPrice;
                priceMaxInput.value=maxPrice;
                actualizar();
            });

            document.getElementById("orden-columna").addEventListener("change", actualizar);
            document.getElementById("orden-direccion").addEventListener("change", actualizar);

            actualizar();
        </script>
    </body>
    </html>
    """

    return render_template_string(html, minAnio=minAnio, maxAnio=maxAnio,
                                  minEngine=minEngine, maxEngine=maxEngine,
                                  minPrice=minPrice, maxPrice=maxPrice,
                                  records=records)

if __name__ == "__main__":
    app.run(debug=True)

